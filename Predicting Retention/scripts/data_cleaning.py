import pandas as pd
import numpy as np

import os
import sys
from pathlib import Path

# Include 'code' folder in path
CODE_FOLDER = Path.cwd().parent / 'code'
sys.path.insert(0, str(CODE_FOLDER))

# Import custom modules
from processing import select_sem, find_enrolled, count_online_classes

def load_csv_files(folder_path):
    """
    Load multiple CSV files and combine them into a single DataFrame.

    Parameters:
        file_paths (list): List of file paths to load.
        lowercase_columns (bool): Whether to lowercase column names

    Returns:
        pd.DataFrame: Combined dataframe.

    """
    all_dfs = []
    for file_name in os.listdir(folder_path):
        # Only process files with .csv extention
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = (pd.read_csv(file_path)
                    .rename(columns = str.lower)
                 )
            all_dfs.append(df)

    # Combine all dfs
    combined_df = (pd.concat(all_dfs, ignore_index = True)
                     .reset_index(drop = True)
                  )

    # Check for special column heading from gpa dataframe or pell dataframe
    if all(col in combined_df.columns for col in ['studentid', 'gpatrm']):
        combined_df = (combined_df.rename(columns = {'studentid':'id', 'gpatrm':'term'})
                                  .sort_values('term', ascending = True)
                      )
    elif 'loan_grant_term' in list(combined_df.columns):
        combined_df = (combined_df.rename(columns = {'loan_grant_term':'term'})
                                  .sort_values(['term', 'id'], ascending = True)
                      )
    elif all(col in combined_df.columns for col in ['stdtid', 'termentered']):
        combined_df = (combined_df.rename(columns = {'stdtid':'id', 'termentered':'term'})
                                  .rename(columns = str.lower)
                      )
    else:
        combined_df = combined_df
    
    return combined_df

def remove_missing_gpa(gpa_df):
    """
    Remove rows with missing GPA values and check for distribution changes.

    Parameters:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: DataFrame without missing GPA values.

    """
    all_gpas = gpa_df[gpa_df['term'].isna() == False]

    all_gpas['term'] = all_gpas['term'].astype(int)

    return all_gpas
    
def record_retention(all_sem_stud_data, semesters, years):
    """
    Identifies students who retained from Fall to Fall

    Parameters:
        all_sem_stud_data (pd.DataFrame): Student enrollment dataframe.
        semesters (int): List of six digit semester codes saved as string.
        years (int): List of two digit integers indicating the year.

    Returns:
        pd.DataFrame: Dataframe with new "enrolled" column created.
        
    """
    
    # Loop through each semester to compare them to one another and 
    # record who enrolled from one semester to the next.
    perc_enrolled = []
    all_enrolled = []
    
    for i in range(1, 5, 1):
        temp_perc = find_enrolled(select_sem(all_sem_stud_data, int(semesters[i-1])), 
                             select_sem(all_sem_stud_data, int(semesters[i])), 
                             years[i - 1], years[i])[0]
        temp_enrolled = find_enrolled(select_sem(all_sem_stud_data, int(semesters[i-1])), 
                             select_sem(all_sem_stud_data, int(semesters[i])), 
                             years[i - 1], years[i])[1]
        perc_enrolled.append(temp_perc)
        all_enrolled.append(temp_enrolled)

    # Combine the all semesters of with the enrolled/unenrolled students in it
    all_enrolled_df = (pd.concat(all_enrolled)
                         .reset_index(drop = True)
                      )

    return all_enrolled_df

def combine_enrolled_and_gpa(all_enrolled_df, all_gpas):
    """
    Combines the enrollment data with the gpa data.

    Parameters:
        all_ernolled_df (pd.DataFrame): Student enrollment dataframe with "enrolled" column created.
        all_gpas (pd.DataFrame): GPA dataframe that has been cleaned of missing values.

    Returns:
        pd.DataFrame: Returns 
    """
    combined_dfs = all_enrolled_df.merge(all_gpas, how = 'left', on = ['id', 'term'])

    # Reorganize the columns to 
    combined_dfs = combined_dfs[['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                                   'degcode', 'majr_desc1', 'gender', 'mrtl', 'ethn_desc', 'cnty_desc1',
                                   'styp', 'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 
                                   'term_gpa', 'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa',
                                   'enrolled']]
    
    # Remove NaN values
    combined_dfs = combined_dfs[combined_dfs['overall_gpa'].isna() == False].reset_index(drop = True)

    return combined_dfs
    
def clean_demographic_data(combined_dfs):
    """
    Handle missing and erroneous values in demographic columns.

    Parameters:
        combined_dfs (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.

    """
    cleaned_combined_dfs = combined_dfs.drop(columns = ['mrtl'], errors = 'ignore') 
    cleaned_combined_dfs = cleaned_combined_dfs[combined_dfs['gender'] != 'Not Enrolled']
    cleaned_combined_dfs = cleaned_combined_dfs[combined_dfs['cnty_desc1'] != 'Not Enrolled']
    cleaned_combined_dfs['ethn_desc'] = cleaned_combined_dfs['ethn_desc'].replace('Not Enrolled', 'Missing')

    return cleaned_combined_dfs

def online_classes(crhr_df, cleaned_combined_dfs):
    """
    Returns online student information combined with enrollment and gpa dataframe

    Parameters:
        crhr_df (pd.DataFrame): This is a .csv file of combined credit hour data from the IR database
                                for the previous four Fall semesters.
        combined_dfs (pd.DataFrame): This is the combined dataframe of cleaned enrolled and gpa data.

    Returns:
        pd.DataFrame: Dataframe of integrated online status of students with gpa and enrollment data.
        
    """    

    # Loop through all the previous Fall semesters and
    # use the count_online_classes() function
    all_sems_online = []
    
    for i in crhr_df['term'].unique():
        temp = count_online_classes(crhr_df, i)
        all_sems_online.append(temp)

    # Pull together all semesters' fully online data
    fully_online = (pd.concat(all_sems_online).reset_index(drop = True)
                      [['id', 'term', 'fully_online']]
                   )
    
    # Merge enrolled_gpas and fully_online datasets
    enrolled_gpas_online = (cleaned_combined_dfs.merge(fully_online, how = 'left', on = ['id', 'term'])
                               [['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                                'degcode', 'majr_desc1', 'gender', 'ethn_desc', 'cnty_desc1', 'styp',
                                'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 'term_gpa',
                                'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa', 'fully_online',
                                'enrolled']]
                           )
    
    return enrolled_gpas_online    

def pell_grant_cleansing(pell, enrolled_gpas_online):
    """
    Returns a dataframe that combines the enrollment data, GPA data, online data, and FAFSA data.

    Parameters:
        pell_df (pd.DataFrame): Dataframe of FAFSA data pulled using PL/SQL from Oracle's Banner DB.
        enrolled_gpas_online (pd.DataFrame): Dataframe of combined enrollment, GPA< and online data.

    Returns:
        pd.DataFrame: Dataframe with combined data.
        
    """
    # Fill all null values in 'accepted_amt' with zeros
    pell['accept_amt'] = pell['accept_amt'].fillna(0).astype(int)
    
    # Filter only those monies that had a pay out date
    pell_mask1 = pell['paid_date'].isna() == False
    
    # Filter only those that had a monetary payout
    pell_mask2 = pell['accept_amt'] != 0.00
    
    # Use filters to create the accepted FAFSA
    pell_accepted = pell[pell_mask1 & pell_mask2].reset_index(drop = True)

    # Create dummy variables for each level of the pell_nopell column
    dummies = []
    
    for i in pell_accepted['term'].unique():
        # Create temporary DF for each term
        temp = pell_accepted[pell_accepted['term'] == i]
        
        # Convert each semester's 'pell_nopell' column to indicator variables
        temp_dummies = pd.get_dummies(temp['pell_nopell'])
        
        # Combine the id and term with the dummy variables
        temp_final = pd.concat([temp[['id', 'term']], temp_dummies], axis = 1)
        
        # Groupby 'id' and 'term' and sum
        grouped_by_id_term = temp_final.groupby(['id', 'term']).sum().reset_index()
        
        # Do the summing process and last time with the groupby function
        temp_final = grouped_by_id_term.groupby('id').sum().reset_index()
        
        # Save the temp_final to dummies list
        dummies.append(temp_final)
        
    # Concatenate dummies list
    final_pell = pd.concat(dummies).fillna(0)

    # Convert Summer Plus and Kansas Promise to integers
    final_pell['Summer Plus'], final_pell['Kansas Promise'] = final_pell['Summer Plus'].astype(int), final_pell['Kansas Promise'].astype(int)
    
    # Create a column that totals all the aid offered (note this is not accepted and received FinAid, just offered FA)
    cols_to_sum = ['NO PELL', 'PELL', 'Subsidized', 'Unsubsidized', 'Summer Plus', 'Kansas Promise']
    
    # Sum all accepted FAFSA money for each ID each semester
    final_pell['all_fafsa'] = final_pell[cols_to_sum].sum(axis = 1)

    # Convert all the 'NO PELL' values in the column to either 1 or 0
    final_pell['NO PELL'] = [1 if i >= 1 else 0 for i in final_pell['NO PELL']]
    
    # View final pell
    final_pell = final_pell.reset_index(drop = True)

    # Merge fafsa dataframe with enrolled_gpas_online dataframe
    enrolled_gpas_online_fafsa = (enrolled_gpas_online.merge(final_pell, how = 'left', on = ['id', 'term'])
                                      .rename(columns = {
                                          'Summer Plus':'summer_plus',
                                          'Kansas Promise':'kansas_promise',
                                          'NO PELL':'no_pell',
                                          'Subsidized':'subsidized',
                                          'PELL':'pell',
                                          'Unsubsidized':'unsubsidized'
                                      })
                                 )
    
    # Loop thrugh the FAFSA columns and fill all NaN values with 0 and make 
    # column into integer
    fafsa_cols = list(enrolled_gpas_online_fafsa.columns[25:])
    
    for i in fafsa_cols:
        enrolled_gpas_online_fafsa[i] = enrolled_gpas_online_fafsa[i].fillna(0).astype(int)

    # Reorganize dataframe
    enrolled_gpas_online_fafsa = enrolled_gpas_online_fafsa[['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                                   'degcode', 'majr_desc1', 'gender', 'ethn_desc', 'cnty_desc1', 'styp',
                                   'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 'term_gpa',
                                   'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa',
                                   'fully_online', 'no_pell', 'pell', 'subsidized',
                                   'unsubsidized', 'summer_plus', 'kansas_promise', 'all_fafsa', 'enrolled']]

    return enrolled_gpas_online_fafsa

def hs_matriculation_feature(high_school_df, enrolled_gpas_online_fafsa):
    """
    Returns a dataframe with all combined engineered features.

    Parameters:
        high_school_df (pd.DataFrame): Dataframe pulled from Argos demographic report. The primary feature engineered here is
            generated by isolating the year a student graduated and if that student started the Fall semester immediately following
            their HS graduation. If they did, then they matriculated directly from HS.
        enrolled_gpas_online_fafsa (pd.DataFrame): Combined dataframe of the pipeline up through this point.

    Returns:
        pd.DataFrame: Dataframe with hs_matriculation feature added in.
        
    """
    # Make hsgraddte into datetime object
    high_school_df['hsgraddte'] = pd.to_datetime(high_school_df['hsgraddte'])
    
    # Make year column for hs grad date
    high_school_df['hs_grad_yr'] = high_school_df['hsgraddte'].dt.year.fillna(0).astype(int)
    
    # Convert term to string to extract term_year
    high_school_df['term'] = high_school_df['term'].astype(str)
    
    high_school_df['term_year'] = [high_school_df['term'][i][:4] for i in range(len(high_school_df))]
    
    high_school_df['term_year'] = high_school_df['term_year'].astype(int)
    
    # Identify which students enrolled in the Fall right after HS Graduation
    high_school_df['hs_matriculation'] = ['From HS' if  i == j else 'Not From HS' for i, j in zip(high_school_df['term_year'], high_school_df['hs_grad_yr'])]
    
    # Merge enrolled_gpas_online_fafsa with all_hs[['id', 'term', 'hs_matriculation']]
    all_hs_for_merge = high_school_df[['id', 'term', 'hs_matriculation']]
    all_hs_for_merge['term'] = all_hs_for_merge['term'].astype(int)
    
    enrolled_gpas_online_fafsa_hs = (enrolled_gpas_online_fafsa.merge(all_hs_for_merge, how = 'left', on = ['id', 'term'])
                                        .drop_duplicates(subset = ['id', 'term'])
                                    )

    # Validate data integrity
    df1 = enrolled_gpas_online_fafsa[['term', 'id']]
    df2 = enrolled_gpas_online_fafsa_hs[['term', 'id']]
    df1_sorted = df1.sort_values(by=['term', 'id']).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=['term', 'id']).reset_index(drop=True)
    
    # Raise an exception if the DataFrames are not identical
    if not df1_sorted.equals(df2_sorted):
        raise ValueError("The DataFrames are different after the merge. Check the merging logic.")

    # Reorient columns
    enrolled_gpas_online_fafsa_hs = enrolled_gpas_online_fafsa_hs[['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                                       'degcode', 'majr_desc1', 'gender', 'ethn_desc', 'cnty_desc1', 'styp',
                                       'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 'term_gpa',
                                       'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa',
                                       'fully_online', 'no_pell', 'pell', 'subsidized', 'unsubsidized',
                                       'summer_plus', 'kansas_promise', 'all_fafsa', 'hs_matriculation', 'enrolled']]

    return enrolled_gpas_online_fafsa_hs

if __name__ == "__main__":
    # Create folder pathways
    enrollment_folder_path = Path.cwd().parent / 'Files/Enrollment'
    gpa_folder_path = Path.cwd().parent / 'Files/GPA and CrHrs' 
    pell_folder_path = Path.cwd().parent / 'Files/Pell and Loan'
    online_folder_path = Path.cwd().parent / 'Files/Location'
    high_school_folder_path = Path.cwd().parents[1] / 'Enrollments/High School Enrollments/Files'
    
    # Load data
    combined_enrollment_data = load_csv_files(enrollment_folder_path)
    combined_gpa_data = load_csv_files(gpa_folder_path)
    combined_online_data = load_csv_files(online_folder_path)
    combined_pell_data = load_csv_files(pell_folder_path)
    combined_hs_matriculation = load_csv_files(high_school_folder_path)
    
    # Modify Data
    enrolled_cleaned_data = record_retention(combined_enrollment_data, semesters = ['201980', '202080', '202180', '202280', '202380'],
                                            years = [19, 20, 21, 22, 23])
    gpa_cleaned_data = remove_missing_gpa(combined_gpa_data)
    
    # Combine Dataframes
    enrolled_gpas_combined = combine_enrolled_and_gpa(enrolled_cleaned_data, gpa_cleaned_data)
    demographic_cleaned_data = clean_demographic_data(enrolled_gpas_combined)
    enrolled_gpas_online = online_classes(combined_online_data, demographic_cleaned_data)
    enrolled_gpas_online_fafsa = pell_grant_cleansing(combined_pell_data, enrolled_gpas_online)
    enrolled_gpas_online_fafsa_hs = hs_matriculation_feature(combined_hs_matriculation, enrolled_gpas_online_fafsa)
