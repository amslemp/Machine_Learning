import seaborn as sns
import matplotlib.pyplot as plt

# Visualize the top 10 TF-IDF scores for a specific question category
def visualize_top_terms(ax, tfidf_dataframe, category, top_n = 10):
    top_terms = (tfidf_dataframe
                     .loc[category]
                     .sort_values(ascending = False)
                     .head(top_n)
                 )
    sns.barplot(x = top_terms.values, y = top_terms.index, ax = ax)
    ax.set_title(f'Top {top_n} Terms For {category}')
    ax.set_xlabel('TF-IDF Score')
    ax.set_ylabel('')
