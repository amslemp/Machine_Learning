import pandas as pd
import numpy as np

# convert csv to parquet
def convert_csv_to_parquet(csv_file: str, new_name: str):
    """
    Converts a CSV file to a parquet file.
    
    Parameters:
        csv_file: File path to access csv_file.
        new_name: Name you will store the parquet file under.
    """
    # Read CSV file
    census_file = (pd.read_csv(csv_file)
                     .rename(columns = str.lower)
                  )
    
    # Write to parquet
    census_file.to_parquet(f'Files/{new_name}.parquet', engine = 'pyarrow')

def isolate_fall_spring_persistence(persistence_dict, headcount_df, semester_filt):
    """
    Parameters:
        persistence_dict (dict): Dictionary of persistence calculations for new and transfer students 
                                 that are in the enrollment coach majors.
        headcount_df (pd.DataFrame): Dataframe of headcount derived from 20th Day IR data.
        semester_filt (str): Can be a string of "Fall" or "Spring".

    Return:
        pd.DataFrame: Dataframe of the persistence of each term sorted by their respective semesters (i.e. Fall or
                      Spring)
    """
    return (pd.concat(persistence_dict)
               .reset_index(drop = True)
               .groupby(['term'], as_index = False)['id'].count()
               .rename(columns = {'id':'persistence'}
            ).merge(
                   (headcount_df
                       .groupby(['term'], as_index = False)['id'].nunique()
                       .rename(columns = {'id':'tot_hc'})),
                   on = 'term', how = 'left')
               .assign(persist_percent = lambda df: df['persistence'] / df['tot_hc'])
               .assign(semester = lambda df: ['Fall' if "80" in term else "Spring" for term in df['term'].astype(str)])
               .query("semester == @semester_filt")
               .reset_index(drop = True)
            )
    
def create_crhr_range(census_df, col_name):
    """
    Add credit range to census_file

    Parameters: 
        census_df (pd.DataFrame): Dataframe of 20th day data (census data, census_file).
        col_name (str): Column name to be referenced in the if/then statement ('totcr')

    returns:
        pd.DataFrame: Dataframe of census data with credit hour range column added.
        
    """
    credit_range = []
    
    for cr in census_df[col_name]:
        if cr > 0 and cr < 6:
            credit_range.append('0 - 5')
        elif cr >= 6 and cr < 9:
            credit_range.append('6 - 8')
        elif cr >= 9 and cr < 12:
            credit_range.append('9 - 11')
        elif cr >= 12 and cr < 15:
            credit_range.append('12 - 14')
        elif cr >= 15 and cr < 18:
            credit_range.append('15 - 17')
        elif cr >= 18 and cr < 21:
            credit_range.append('18 - 20')
        elif cr >= 21 and cr < 24:
            credit_range.append('21 - 23')
        elif cr >= 24 and cr < 27:
            credit_range.append('24 - 26')
        else:
            credit_range.append('>= 27')
    
    census_df['credit_range'] = credit_range

    return census_df