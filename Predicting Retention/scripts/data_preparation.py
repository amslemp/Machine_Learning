import pandas as pd
import numpy as np

def load_and_prepare_data(data_path):
    
    """
    Returns dataframe ready for XGBoost model.

    Parameters:
        data_path (str): Path to cleaned dataframe from data preparation (enrolled_gpas_online_fafsa_hs).

    Returns:
        pd.Dataframe: Modifed dataframe set up for XGBoost model.
    """

    # Load data
    df = pd.read_csv(data_path)

    df = df[['enrolled', 'stype', 'gender', 'ethn_desc', 'resd', 'fully_online',
             'acd_std_desc', 'age', 'term_att_crhr', 'term_earn_crhr', 'term_gpa',
             'inst_gpa', 'inst_earned', 'no_pell', 'pell', 'subsidized', 'unsubsidized', 
             'summer_plus', 'kansas_promise', 'all_fafsa', 'hs_matriculation']]

    # Filter and encode data
    df['enrolled'] = [1 if i == 'Enrolled' else 0 for i in df['enrolled']]
    df = df[df['resd'] != 'Z']
    df['hs_matriculation'] = df['hs_matriculation'].fillna('Not From HS')
    df = df[(df['age'] <= 60) & (df['age'] >= 10)]
    df = df[df['ethn_desc'] != 'DO NOT USE - Hispanic']

    return df
