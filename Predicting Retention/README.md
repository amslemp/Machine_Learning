# Predicting Retention

This modeling was done in conjunction with the VP of Academics. He wanted to know if I could create a model based on the data we captured that could accurately predict the students who were at the highest risk of not reenrolling for the next Fall semester. In colleges, retention is defined as Fall to Fall reenrollment, meaning students who were enrolled in the previous Fall semester who are enrolled in the *current* Fall semester. 

## Data

The data was pulled directly from Oracle's BannerDB using PL/SQL. I wrote the queries that pulled the data so that I could then import it into R and Python. Python was primarily used for feature engineering and comgining of the dataframes. R was used for almost all statistical analysis and model building, with the exception of XGBoost. That model runs more efficiently in Python, in my opinion. 

## Results

I compared several models to see which one was best for this task and dataset. Ultimately XGBoost won out. What was most important in this dataset was *specificity* rather than just pure accuracy, because it was more costly to misclassify students who do not reenroll than students who do reenroll. I was proud to discover that several of the features that I engineered were actually the best predictors for identifying students who are most likely to not enroll for the next Fall semester. In fact, the top predictor for identifying which student will not enroll the following Fall was a non-native feature that I created. The final XGBoost model was built with a gridsearch for tuning the hyperparameters. 

## Model Deployment

After the model was built, I created a dashboard in Power BI for the VP of Academics. Speicifically, he wanted a dashboard that integrated the model and allowed him to conduct "what-ifs" on the data. For instance, if the enrollment increased with a certain demographic, how would it impact credit hour enrollment and ultimately, revenue generation. This kind of model and dashboard in the hands of any C-suite or excecutive is invaluable, a model that predicts the impact of retaining additional customers on revenue. 
