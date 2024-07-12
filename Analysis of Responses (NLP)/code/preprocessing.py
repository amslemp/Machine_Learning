
import pandas as pd
import numpy as np

def configure_dataframe(df):
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
    df (pd.DataFrame()): New_df. Has columns ['Timestamp', 'question_cat', 'question', 'value']
    col_name (string): Column or list of columns you want to group the data by.
    
    """
    average = (df[df['row_type'] == row_type]
                  .groupby(col_name)
                  .agg(mean=('value', 'mean'), stdev=('value', 'std'))
                  .reset_index()
                  .reset_index(drop = True)
              )
     
    return average

import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords

# Create function for couting the tokens in each category
def count_tokens_by_cat(df):
    
    # Create an empty dictionary to store token counts by category
    token_counts_by_cat = {}
    
    # Iterate over each unique category
    for cat in df['question_cat'].unique():
        # Filter the dataframe by category
        cat_df = df[df['question_cat'] == cat]
        
        # Flatten the list of lists of tokens for this category
        all_tokens = [token for sublist in cat_df['tokens'].tolist() for token in sublist]
        
        # Count tokens and store in the dictionary
        token_counts_by_cat[cat] = Counter(all_tokens)
    
    return token_counts_by_cat

def get_important_tokens(dictionary, question_cat, threshold):
    
    imp_tokens = (pd.DataFrame
                    .from_dict(dictionary.get(question_cat), orient = 'index')
                    .reset_index().rename(columns = {'index':'freq_words',
                                                     0:'count'})
                    .sort_values('count', ascending = False)
                    [lambda x: x['count'] >= threshold]
                    .reset_index(drop = True)
                 )
    
    imp_tokens['question_cat'] = question_cat
    
    imp_tokens = imp_tokens[['question_cat', 'freq_words', 'count']]
    
    return imp_tokens

# Load English stopwords
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords and punctuation
    filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in stop_words]
    # Re-join tokens into a string
    return ' '.join(filtered_tokens)

# Function to get top n terms with the highest TF-IDF scores for each question category
def top_terms_by_category(tfidf_dataframe, top_n = 5):
    """
    tfidf_dataframe: Dataframe of TF-IDF values.
    top_n (int): Defaults to 5. Can be changed to locate the top n values for the TF-IDF.
    
    """
    cat_dict = {}
    for category in tfidf_dataframe.index:
        cat_dict[category] = tfidf_dataframe.loc[category].sort_values(ascending=False).head(top_n)
    
    cat_df = (pd.DataFrame.from_dict(cat_dict, orient = 'columns')
                .fillna(0)
             )
    
    return cat_df

from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models import CoherenceModel
import re

def coherence_model(df, token_col, grouping_col, award_cat, num_of_topics):
    # Tokenize the processed text
    df['tokens'] = df[token_col].apply(word_tokenize)

    # Create a Gensim dictionary from the tokenized data
    tokenized_data = df[(df[grouping_col] == award_cat)]['tokens'].tolist()
    #tokenized_data = string_resp['tokens'].tolist()
    dictionary = corpora.Dictionary(tokenized_data)

    # Filter out extremes to remove very rare and very common words
    dictionary.filter_extremes(no_below=5, no_above=0.5)

    # Convert dictionary into a bag of words corpus
    corpus = [dictionary.doc2bow(text) for text in tokenized_data]

    # Number of topics
    num_topics = num_of_topics

    # Build LDA model
    lda_model = LdaModel(corpus = corpus,
                         id2word = dictionary,
                         num_topics = num_topics,
                         random_state = 101,
                         update_every = 1,
                         chunksize = 100,
                         passes = 10,
                         alpha = 'auto')
    
    # View the topics in LDA model
    lda_mod = {}
    for idx, topic in lda_model.print_topics(-1):
        lda_mod[idx] = topic
    
    # Extract the topic words from each topic identified within each question category
    topics = []
    for text in range(len(lda_mod)):
        # Use regex to extract all words within quotes
        words = re.findall(r'"(.*?)"', lda_mod.get(text))
        topics.append(words)
    
    # Compute Coherence Score for overall question category
    coherence_model_lda = CoherenceModel(model=lda_model, texts=tokenized_data, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    
    # Store the per topic coherency score
    coherence_per_topic = coherence_model_lda.get_coherence_per_topic()
    
    return lda_mod, coherence_lda, topics, coherence_per_topic
