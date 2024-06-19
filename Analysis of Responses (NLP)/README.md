# Teaching Excellence Award

The Teaching Excellence Award is an award that is given to one professor a year at the community college with which I work. It is bestowed in partnership with The League For Innovation In The Community College. Professors are nominated by students (or even other faculty members) for this award. Over the last ten years, the Faculty Development Team that evaluates the responses from nominators and selects the award recipient has not reexamined the questions used in the nomination process. There has been widespread suspicion among the FDT that some of the question categories are less well understood by the students selecting faculty for the award. This analysis was conducted for the purpose of identifying what themes bubble to the surface from student responses to each question category. 

This was a one-off, ad hoc analysis. Consequently, there was no dashboard created and the code here is not written for model deployment. A report was written up based on the findings from these models and EDA and given to the Director of FDT, his Assistant Director, and the FDT members on the subcommittee that is rewriting the questions for the Teaching Excellence Award.

# The Data

The director of FDT was able to locate most of the years of nominations going back to 2014 but not all. Since this still involves student data and responses, the raw data files cannot be shared due to the federal FERPA law.

There are two parts to the data: one is the actual rankings that nominators gave to professors based on the question category; the other is the long form responses the provided by the nominator about the nominee. 

Professors are evaluated based on five question categories--TEACH, TECH, CARE, INNOVATION, and LEADERSHIP. 

# EDA

I first explore the numeric rankings for each question category. One of the first revelations that the FDT had already discussed is how these rankings may not be particularly helpful because, by definition, the nominees would be *great* at their jobs. The whole reason for their nomination is the fact that they are exceptional teachers. Therefore, there should be a coniderable amount of selection bias in the data, which would render these rankings largely useless. Sure enough, just over 90% of all rankings over the years fell within one standard deviation of the mean for each question category. Every question category had a mean above 9.0 on a scale of 1 to 10. 

A TukeyHSD test was applied both to the rankings and to the mean of the long form answers for each question category. Each test generated different considerations.

Violin plots were applied to visually examine the distribution of the number of words per response for each category.

# Model Development

## Keyword Frequency Analysis (KFA)

The initial model applied was a simple KFA to uncover any obvious patterns or topics in the responses for each question category using the *nltk* library. This initial analysis actually ended up generating some of the most insightful observations about the questions and how they could be improved.

## Term Frequency-Inverse Document Frequency (TF-IDF)

This analysis digs a little deeper as TF-IDF helps identify themes and topics respondents talk about while also diminishing the weight of terms that occur frequently across the answers to specific questions. This is accomplished by including a calcuation term that controls for the uniqueness of the word. The report delves into the details.

## Latent Dirichlet Allocation Model (LDA)

This model is an unsupervised learning algorithm that helps identify topics present across the corpus. If responses to certain question categories consistently cluster around unrelated topics, it might be an indication that the question is not well understood. This model is more robust as it calculates a coherence score to determine the semantic similarity between high scoring words within each question category, which provides a metric for understanding how important and interpretable certain topics are. Here also, the number of topics before the max coherency score is attained might inform us about how well understood a question category is. If the max coherency score occurs after three clusters of topics, it might be an indication that the qeustion is not well understood. 

# Results

As alluded to above, the initial KFA actually produced some of the best insights and refinement of questions. LEADERSHIP is not a well understood topic for students to respond to about their professors. This was evident through the Tukey HSD test of the rankings as well as the LDA model that showed there were six clusters of topics before the best coherence score was achieved. CARE also had a high number of topics before the max coherence score is achieved, highlighting the fact that the definition of CARE and perception of it from students is heavily nuanced. Not surprisingly, TEACH and INNOVATION are well understood and center around only one or two topics in the LDA. 

As a consequence of this analysis, questions were restructured around what students actually understood and reworded to increase their engagement. Indeed, engagement increased by 18% after new implementation. 
