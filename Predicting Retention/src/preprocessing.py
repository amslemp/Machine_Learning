from typing import List, Tuple, Optional, Union
from pathlib import Path

import pandas as pd
import numpy as np
import fire

from src.paths import DATA_DIR
from src.logger import get_console_logger

logger = get_console_logger ()

def transform_to_features_and_response(path_to_enrollment, path_to_gpa, path_to_finaid, path_to_hs) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Transforms data and engineers features as well as generates the response variable for
    training supervised ML models.
    
    """
    # Choose semesters
    semesters = ['201980', '202080', '202180', '202280', '202380']
    fin_sem = ['FA19 - FA23']
    
    # Load data
    def load_enrollment(enrollment_path):
        all_sems = []
        for sem in semesters:
            temp = (pd.read_csv(enrollment_path + f'/{sem} Enrollment.csv')
                      .rename(columns = str.lower))
            all_sems.append(temp)
        
        return pd.concat(all_sems).reset_index(drop = True)
        
    def load_gpas(gpa_path):
        all_gpas = []
        for sem in semesters[:4]:
            temp = (pd.read_csv(gpa_path + f'/{sem} GPA and CrHrs.csv').rename(columns = str.lower))
            all_gpas.append(temp)
        
        return (pd.concat(all_gpas)
                  .reset_index(drop = True)
                  .rename(columns = {'studentid':'id',
                                     'gpatrm':'term'})
               )
    
    def load_finaid(finaid_path):
        pell = (pd.read_csv(finaid_path + f'/Pell and Load {fin_sem[0]}.csv')
                  .rename(columns = {'LOAD_GRANT_TERM':'term'})
                  .rename(columns = str.lower)
                  .sort_values(['term', 'id']))
        
        return pell
    
    def load_hs(high_school_path):
        all_sems = []
        for sem in semesters:
            temp_hs = pd.read_csv(high_school_path + f'/{sem} Demographic Info.csv')
            all_sems.append(temp_hs)
        
        return (pd.concat(all_sems)
                  .reset_index(drop = True)
                  .rename(columns = {'STDTID':'ID',
                                     'TERMENTERED':'TERM'})
                  .rename(columns = str.lower)
               )
    
    # Load all dataframes
    all_sems = load_enrollment(path_to_enrollment)
    all_gpas = load_gpas(path_to_gpa)
    pell = load_finaid(path_to_finaid)
    online = (pd.read_csv(path_to_enrollment / 'FA19 - FA22 CrHr Enrollment.csv')
                .rename(str.lower))
    all_hs = load_hs(path_to_hs)
    
    # Create function that compares the semeseters and identifies student enrollment
    def find_enrolled(prev_term, curr_term, sem_0, sem_1):
        
        # Create column for current term that shows all the students enrolled
        curr_term['enrolled'] = 'enrolled'
        
        # Merge the previous term and the current term, only keeping the 'enrolled' column,
        # filling the NaN values with 'Not Enrolled'
        prev_curr = (prev_term.merge(curr_term[['id', 'enrolled']], how = 'left', on = 'id')
                         .fillna('Not Enrolled')
                         .reset_index(drop = True)
                    )
        
        # Create dataframe of the count of students from the previous semester enrolled in current
        # semester
        prev_curr_cnt = (pd.DataFrame(prev_curr.groupby('enrolled')['id'].count())
                           .reset_index()
                           .rename(columns = {'id', 'cnt'})
                        )
        
        # Create column that shows the percent of students who enrolled for curr_term
        # from prev_term
        prev_curr_cnt['percent'] = prev_curr_cnt['cnt'] / prev_curr_cnt['cnt'].sum()
        
        # Record the terms
        prev_curr_cnt['terms'] = 'fa' + str(sem_0) + '_' + 'fa' + str(sem_1)
        
        # Reorganize the dataframe
        prev_curr_cnt = prev_curr_cnt[['terms', 'enrolled', 'cnt', 'percent']]
        
        return prev_curr_cnt, prev_curr
    
    def identify_retention(all_sems_df, semester_list):
        sems_filt = [19, 20, 21, 22, 23]
        
        # Loop through each semester to identify customers who retained from Fall to Fall
        perc_enrolled = []
        all_enrolled = []
        
        for i in range(1, 5, 1):
            # Isolate previous term
            previous_term = all_sems[all_sems_df['term'] == semester_list[i - 1]]
            # Isolate current term
            current_term = all_sems[all_sems_df['term'] == semester_list[i]]
            # Identify retained students
            temp_perc = find_enrolled(previous_term, current_term, sems_filt[i - 1], sems_filt[i])[0]
            temp_enrolled = find_enrolled(previous_term, current_term, sems_filt[i - 1], sems_filt[i])[1]
            # Save results
            perc_enrolled.append(temp_perc)
            all_enrolled.append(temp_enrolled)
        
        return (
            pd.concat(all_enrolled)
              .reset_index(drop = True)
        )
    
    # Run retention dataframe
    all_enrolled_df = identify_retention(all_sems, semester)
    
    # Combine the df with the customer data and retention status along 
    # with the gpas and credit hour data
    enrolled_gpas = all_enrolled_df.merge(all_gpas, how = 'left' on = ['id', 'term'])
    
    # Create final dataset for evaluation
    ## Reorganize the columns
    enrolled_gpas = enrolled_gpas[['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                               'degcode', 'majr_desc1', 'gender', 'mrtl', 'ethn_desc', 'cnty_desc1',
                               'styp', 'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 
                               'term_gpa', 'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa',
                               'enrolled']]
    
    ## Deal with missing values
    ### Remove 'mrtl' column as there are too many missing values, over half. Imputing would not
    ### help but rather would skew the data.
    enrolled_gpas = enrolled_gpas[['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                               'degcode', 'majr_desc1', 'gender', 'ethn_desc', 'cnty_desc1',
                               'styp', 'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 
                               'term_gpa', 'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa',
                               'enrolled']]
    
    ### Remove missing 'gender' and 'cnty_desc1' values
    enrolled_gpas = enrolled_gpas[enrolled_gpas['gender'] != 'Not Enrolled']
    enrolled_gpas = enrolled_gpas[enrolled_gpas['cnty_desc1'] != 'Not Enrolled']
    
    ### Impute missing values in 'ethn_desc' with the attribute 'Missing'
    enrolled_gpas['ethn_desc'] = enrolled_gpas['ethn_desc'].replace('Not Enrolled', 'Missing')
    
    # Create function for looping through semesters and counting all online classes for 
    # each student
    def count_online_classes(df, term):
        """
        df (pd.DataFrame): Datafrme of CrHr enrollment for the previous four Fall or Spring Semesters, 
                       taken from IR data. Pulled Day-1, 20th-Day, and EOT, eliminated duplicates by
                       term, id, and crn.
        term (int): Six digit integer designating the semester you wish to isolate (i.e. 201980, 202080, etc.)
    
        """
        
        # Filter the dataframe by the semester
        temporary_df = df[df['term'] == term]
        
        # Create dictionary for each id and the count of classes
        # as well as the percent of those classes that are online 
        all_online = {}
        
        for ids in temporary_df['id'].unique():
            temp_id = temporary_df[temporary_df['id'] == ids]
            online = 0
            for j in temp_id['loc']:
                if j == 'V':
                    online += 1
                else:
                    online += 0
            all_online[i] = [len(temp_id), online, online/len(temp_id)]
        
        # Make all_online dict into dataframe
        online_df = (pd.DataFrame.from_dict(all_online).T
                       .reset_index()
                       .rename(columns = {'index':'id',
                                          0: 'num_of_classes',
                                          1: 'num_online',
                                          2: 'perc_online'})
                    )
        
        # label the students who are fully online verses those that are not
        online_df['fully_online'] = ['Fully Online' if i == 1.0 else 'Not Fully Online' for i in online_df['perc_online']]
        
        # Label the term
        online_df['term'] = term
        
        # Reorganize teh dataframe
        online_df = online_df[['id', 'term', 'num_of_classes', 'num_online', 'perc_online', 'fully_online']]
        
        return online_df
    
    # Loop through all previous Fall semesters and use the count_online_classes() function
    all_sems_online = []
    
    for i in [201980, 202080, 202180, 202280]:
        temp = count_online_classes(online, i)
        all_sems_online.append(temp)
        
    # Make dataframe of the terms with their counts of fully online/not fully online
    fully_online_cnts = (pd.DataFrame(pd.concat(all_sems_online)
                           .reset_index(drop = True)
                           .groupby(['term', 'fully_online'])['id'].count())
                           .reset_index()
                           .rename(columns = {'id', 'count'})
                        )
    
    # Pull together all semesters' fully online data
    fully_online = pd.concat(all_sems_online).reset_index(drop = True)

    # Isolatejust the columns I need
    fully_online = fully_online[['id', 'term', 'fully_online']]

    # Merge enrolled_gpas and fully_online datasets
    enrolled_gpas_online = enrolled_gpas.merge(fully_online, how = 'left', on = ['id', 'term'])\
                           [['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                            'degcode', 'majr_desc1', 'gender', 'ethn_desc', 'cnty_desc1', 'styp',
                            'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 'term_gpa',
                            'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa', 'fully_online',
                            'enrolled']]
    
    def create_pell_df(pell_df):
        # Engineer pell and scholarship features
        pell['accept_amt'] = pell['accept_amt'].fillna(0).astype(int)

        # Filter only those that had a pay out date
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

            # Convert each semester's 'pell_nopell' to indicator var
            temp_dummies = pd.get_dummies(temp['pell_nopell'])

            # Combine the id and term with the dummy vars
            temp_final = pd.concat([temp[['id', 'term']], temp_dummies], axis = 1)

            # Groupby 'id' and 'term' and sum
            grouped_by_id_term = temp_final.groupby(['id', 'term']).sum().reset_index()

            # Sum one last time with the groupby function
            temp_final = grouped_by_id_term.groupby('id').sum().reset_index()

            # Save the temp_final to dummies list
            dummies.append(temp_final)

        final_pell = pd.concat(dummies).fillna(0)

        # Convert summer plus and kansas promise to integers
        final_pell['Summer Plus'], final_pell['Kansas Promise'] = final_pell['Summer Plus'].astype(int), final_pell['Kansas Promise'].astype(int)

        # Create a column that totals all the aid offered (note this is not 
        # accepted and received FinAid, just offered FA)
        cols_to_sum = ['NO PELL', 'PELL', 'Subsidized', 'Unsubsidized', 'Summer Plus', 'Kansas Promise']

        # Sum all accepted FAFSA money for each ID each semester
        final_pell['all_fafsa'] = final_pell[cols_to_sum].sum(axis = 1)

        # Convert all the 'NO PELL' values in the column to either 1 or 0
        final_pell['NO PELL'] = [1 if i >= 1 else 0 for i in final_pell['NO PELL']]

        # View final pell
        final_pell = final_pell.reset_index(drop = True)
        
        return final_pell
    
    # Create fafsa df
    final_pell = create_pell_df(pell)
    
    # Merge fafsa dataframe with enrolled_gpas_online_dataframe
    enrolled_gpas_online_fafsa = (enrolled_gpas_online.merge(final_pell, how = 'left', on = ['id', 'term'])
                                      .rename(columns = {'Summer Plus':'summer_plus',
                                                         'Kansas Promise':'kansas_promise',
                                                         'NO PELL':'no_pell'})
                                 )
    
    # Loop thrugh the FAFSA columns and fill all NaN values with 0 and make 
    # column into integer
    fafsa_cols = list(enrolled_gpas_online_fafsa.columns[25:])

    for i in fafsa_cols:
        enrolled_gpas_online_fafsa[i] = enrolled_gpas_online_fafsa[i].fillna(0).astype(int)
    
    enrolled_gpas_online_fafsa = enrolled_gpas_online_fafsa[['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                                   'degcode', 'majr_desc1', 'gender', 'ethn_desc', 'cnty_desc1', 'styp',
                                   'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 'term_gpa',
                                   'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa',
                                   'fully_online', 'no_pell', 'PELL', 'Subsidized',
                                   'Unsubsidized', 'summer_plus', 'kansas_promise', 'all_fafsa', 'enrolled']]
    
    # Engineer high school features
    all_hs['hsgraddte'] = pd.to_datetime(all_hs['hsgraddte'])
    
    # Make year column for hs grad date
    all_hs['hs_grad_yr'] = all_hs['hsgraddte'].dt.year.fillna(0).astype(int)
    
    # Convert term to string to extract term_year
    all_hs['term'] = all_hs['term'].astype(str)
    
    all_hs['term_year'] = [all_hs['term'][i][:4] for i in range(len(all_hs))]
    
    all_hs['term_year'] = all_hs['term_year'].astype(int)
    
    # Identify which students enrolled in the Fall right after HS Grad
    all_hs['hs_matriculation'] = ['From HS' if i == j else 'Not From HS' for i, j in zip(all_hs['term_year'], all_hs['hs_grad_yr'])]
    
    hs_matriculation = (pd.DataFrame(all_hs.groupby(['term', 'hs_matriculation'])['id'].count())
                          .reset_index(drop = False)
                          .rename(columns = {'id', 'cnt'})
                       )
    
    # Merge enrolled_gpas_online_fafsa with all_hs[['id', 'term', 'hs_matriculation']]
    all_hs_for_merge = all_hs[['id', 'term', 'hs_matriculation']]
    all_hs_for_merge['term'] = all_hs_for_merge['term'].astype(int)

    enrolled_gpas_online_fafsa_hs = (enrolled_gpas_online_fafsa.merge(all_hs_for_merge, how = 'left', on = ['id', 'term'])
                                        .drop_duplicates(subset = ['id', 'term'])
                                    )
    
    # Reorient columns
    enrolled_gpas_online_fafsa_hs = enrolled_gpas_online_fafsa_hs[['term', 'pidm', 'age', 'id', 'totcr', 'status', 'stype', 'resd_desc',
                                       'degcode', 'majr_desc1', 'gender', 'ethn_desc', 'cnty_desc1', 'styp',
                                       'resd', 'acd_std_desc', 'term_att_crhr', 'term_earn_crhr', 'term_gpa',
                                       'inst_gpa', 'inst_earned', 'inst_hrs_att', 'overall_gpa',
                                       'fully_online', 'no_pell', 'pell', 'subsidized', 'unsubsidized',
                                       'summer_plus', 'kansas_promise', 'all_fafsa', 'hs_matriculation', 'enrolled']]

    return enrolled_gpas_online_fafsa_hs.drop(columns = ['enrolled']), enrolled_gpas_online_fafsa_hs['enrolled']

if __name__ == '__main__':
    features, response = fire.Fire(transform_to_features_and_response)
    
