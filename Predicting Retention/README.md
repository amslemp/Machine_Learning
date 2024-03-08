# Predicting Retention

This modeling was done in conjunction with the VP of Academics. He wanted to know if I could create a model based on the data we captured that could accurately predict the students who were at the highest risk of not reenrolling for the next Fall semester. In colleges, retention is defined as Fall to Fall reenrollment, meaning students who were enrolled in the previous Fall semester who are enrolled in the *current* Fall semester. 

## Data

The data was pulled directly from Oracle's BannerDB using PL/SQL. I wrote the queries that pulled the data so that I could then import it into R and Python. Python was primarily used for feature engineering and cleaning the data. R was used for almost all statistical analysis and model building, with the exception of XGBoost. That model runs more efficiently in Python, in my opinion. 

## Results

I compared several models to see which one was best for this task and dataset. Ultimately XGBoost won out. What was most important in this dataset was *specificity* rather than just pure accuracy, because it was more costly to misclassify students who do not reenroll than students who do reenroll. I was proud to discover that several of the features that I engineered were actually the best predictors for identifying students who are most likely to not enroll for the next Fall semester. In fact, the top predictor for identifying which students will not enroll the following Fall was a non-native feature that I created. The final XGBoost model was built with a gridsearch that tuned the hyperparameters. 

**Comparison of Model Performance**

|**Model**|**Accuracy**|**Specificity**|**AUC-ROC**|
|:--------|-----------:|--------------:|----------:|
|LR       |      0.6930|         0.8421|     0.6510|
|CV-LLR   |      0.6408|         0.7985|     0.6470|
|SVM      |      0.7296|         0.9067|     0.6880|
|RF       |      0.7501|         0.8699|     0.7321|
|GBM      |      0.7420|         0.8836|     0.7126|
|NB       |      0.6225|         0.6565|     0.6160|
|k-NN     |      0.7103|         0.8725|     0.6825|
|CART     |      0.7065|         0.8939|     0.6771|
|NN       |      0.7506|         0.8287|     0.7324|
|XGBoost  |      0.7686|         0.8810|     0.7354|

XGBoost had better accuracy and only negligible difference in specificity compared to SVM, GBM, and CART. In fact, when using MCCV, this difference falls within the variance of the model performance, which is why I built the final predictive model with XGBoost. 

## Model Deployment

After the XGBoost model was built a second regression model was built to predict semester credit hour enrollment. Credit hour enrollment, for those outside of education, is akin to units of sales. The value of each credit hour differs based on whether the student is in-state or out-of-state, in county or out of county, and international student or not. The first model was to identify students who were most likely to *not retain* from Fall to Fall. This second model takes those students identified as most likely to not retain and projects how the credit hours would shift if different percentages of these students were retained, which also allows for revenue projections if those students were to retain at a higher level. 

These models were deployed into a Power BI dashboard for the Vice President of Academics (VPA) so that he could make strategic enrollment decisions. The retention model is currently being used by the academic advising office for targeted intervention. Two cohorts were particularly important $ - $ students right out of high school and students who have completed a larger number of credit hours *earned*. For instance, the probability a student will be enrolled the following Fall if they have completed 45 credits is 40.54%, which is an 18.00% increase over students who have completed 30 credits and a 43.00% increase over students who have only completed 15 credits. 
