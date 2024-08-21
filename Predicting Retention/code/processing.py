import pandas as pd
import numpy as np

# Create function to select semesters
def select_sem(df, semester):
    """
    df (pd.DataFrame): "all_sems" dataframe that has the last five Fall semesters.
    semester (int): Six digit integer that designates the semester to isolate.
    """
    df_mask1 = df['term'] == semester
    semester_df = df[df_mask1].reset_index(drop = True)
    
    return semester_df

# To comply with future changes for the fillna() method
pd.set_option('future.no_silent_downcasting', True)

# Create function that compares the semesters and identifies their enrollment
def find_enrolled(prev_term, curr_term, sem_0, sem_1):
    
    # Create column for current term that shows all the students enrolled
    curr_term['enrolled'] = 'Enrolled'
    
    # Merge the previous term and current term, only keeping the 'enrolled' column we just created
    # filling the NaN values with 'Not Enrolled'
    prev_curr = (prev_term.merge(curr_term[['id', 'enrolled']], how = 'left', on = 'id')
                         .fillna('Not Enrolled')
                         .infer_objects(copy=False)
                         .reset_index(drop = True)
                )

    # Create dataframe of the count of students from the previous semester enrolled in current
    # semester
    prev_curr_cnt = (pd.DataFrame(prev_curr.groupby('enrolled')['id'].count())
                       .reset_index()
                       .rename(columns = {'id':'cnt'})
                    )

    # Create column that shows the percent of students who enrolled for curr_term 
    # from prev_term
    prev_curr_cnt['percent'] = prev_curr_cnt['cnt'] / prev_curr_cnt['cnt'].sum()
    
    # Record the terms
    prev_curr_cnt['terms'] = 'fa' + str(sem_0) + '_' + 'fa' + str(sem_1)
    
    # Reorganize the dataframe
    prev_curr_cnt = prev_curr_cnt[['terms', 'enrolled', 'cnt', 'percent']]

    return prev_curr_cnt, prev_curr

# Create function for looping through semesters and counting all online classes for 
# each student
def count_online_classes(df, term):
    """
    df (pd.DataFrame): Datafrme of CrHr enrollment for the previous four Fall or Spring Semesters, 
                       taken from IR data. Pulled Day-1, 20th-Day, and EOT, eliminated duplicates by
                       term, id, and crn.
    term (int): Six digit integer designating the semester you wish to isolate (i.e. 201980, 202080, etc.)
    
    """
    
    # fiFilter the dataframe by the semester
    temporary_df = df[df['term'] == term]
    
    # Create dictionary for each id and the count of classes
    # as well as the percent of those classes that are online
    all_online = {}
    
    for i in temporary_df['id'].unique():
        temp = temporary_df[temporary_df['id'] == i]
        online = 0
        for j in temp['loc']:
            if j == 'V':
                online += 1
            else:
                online += 0
        all_online[i] = [len(temp), online, online/len(temp)]
    
    # Make all_online dictionary into a dataframe
    online_df = (pd.DataFrame.from_dict(all_online).T
                   .reset_index()
                   .rename(columns = {'index':'id',
                                      0:'num_of_classes',
                                      1:'num_online',
                                      2:'perc_online'})
                )

    # Label the students who are fully online verses those that aare not
    online_df['fully_online'] = ['Fully Online' if i == 1.0 else 'Not Fully Online' for i in online_df['perc_online']]
    
    # Label the term
    online_df['term'] = term
    
    # Reorganize the dataframe
    online_df = online_df[['id', 'term', 'num_of_classes', 'num_online', 'perc_online', 'fully_online']]
    
    return online_df
