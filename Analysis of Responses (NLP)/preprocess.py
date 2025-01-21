import pandas as pd
import numpy as np

def configure_dataframe(df):
    """
    Parameters:
        df (pd.DataFrame): Dataframe of individual years loaded up and processed.

    Returns:
        pd.DataFrame: Returns cleaned, organized, and standardized dataframe.
        
    """
    # Create key words for new category column
    award_cats = ['TEACH', 'TECH', 'CARE', 'INNOVATION', 'LEADERSHIP']

    # Create new dataframe with reorganized data
    df_slices = []

    for col in df.columns:

        # Check if the column name contains any of the award_cats
        for cat in award_cats:
            if cat in col:
                if 'Timestamp' in list(df.columns):
                    # Create a new dataframe slice for the current cat
                    df_slice = df[['Timestamp', col]].copy()
                    df_slice['question_cat'] = cat
                    df_slice['question'] = col

                    # Rename values column
                    df_slice.rename(columns = {col:'value'}, inplace = True)

                    # Add the slice to list
                    df_slices.append(df_slice)
                else:
                    # Create a new dataframe slice for the current cat
                    df_slice = df[['Start time', col]].copy()
                    df_slice['question_cat'] = cat
                    df_slice['question'] = col

                    # Rename values column
                    df_slice.rename(columns = {col:'value'}, inplace = True)

                    # Add the slice to list
                    df_slices.append(df_slice)
    
    # If 'Timestamp' is in column headings, save new_df, else save it with the other headings
    if 'Timestamp' in list(df.columns):
        new_df = (pd.concat(df_slices, ignore_index = True)[['Timestamp', 'question_cat', 'question', 'value']]
                    .sort_values(['Timestamp', 'question_cat'])
                    .reset_index(drop = True)
                 )
    else:
        new_df = (pd.concat(df_slices, ignore_index = True)[['Start time', 'question_cat', 'question', 'value']]
                    .sort_values(['Start time', 'question_cat'])
                    .reset_index(drop = True)
                 )

    # Add in a filter that allows me to filter by data type (string/integer)
    new_df['row_type'] = ['Int' if isinstance(i, int) else 'String' for i in new_df['value']]
    
    return new_df

# Create function for calculating averages
def collect_avg(df, col_name, row_type):
    """
    Parameters:
        df (pd.DataFrame()): New_df. Has columns ['Timestamp', 'question_cat', 'question', 'value']
        col_name (str): Column or list of columns you want to group the data by.
        row_type (str): Names the type of data that is in the column. i.e. int, str, bool, etc.

    Returns:
        pd.DataFrame: Dataframe of averages and standard deviations of word occurances.
    
    """
    average = (df[df['row_type'] == row_type]
                  .groupby(col_name)
                  .agg(mean=('value', 'mean'), stdev=('value', 'std'))
                  .reset_index()
                  .reset_index(drop = True)
              )
     
    return average

# Function to get top n terms with the highest TF-IDF scores for each question category
def top_terms_by_category(tfidf_dataframe, top_n = 5):
    """
    Parameters:
        tfidf_dataframe: Dataframe of TF-IDF values.
        top_n (int): Defaults to 5. Can be changed to locate the top n values for the TF-IDF.

    Returns:
        pd.DataFrame: Dataframe of tfidf categories.
    
    """
    cat_dict = {}
    for category in tfidf_dataframe.index:
        cat_dict[category] = (tfidf_dataframe
                                  .loc[category]
                                  .sort_values(ascending = False)
                                  .head(top_n)
                             )
    
    cat_df = (pd.DataFrame
                .from_dict(cat_dict, orient = 'columns')
                .fillna(0)
             )
    
    return cat_df
