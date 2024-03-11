# ML Problems

This repo focuses primarily on problems that I have addressed via machine learning (ML). Since this is data that is pulled in Higher Education, I am bound by FERPA laws and cannot share the data so that one can run the code. Instead, I can only share the code I have written and explain the outcomes and benefits that were derived as a result of the work. 

# Algorithms

In my work as a data scientist, I have worked with many different stakeholders, from marketing to sales (admissions/recruiters), retention specialists (academic advising), to department heads (Deans) and, of course, VPs over entire divisions (academics and enrollment management). In here you will see projects that apply k-prototype algorithms in conjunction with geolocation of students, classification models that accurately predict which students are most likely to persist from one semester to another and which are most likely to retain from Fall to Fall, time series forecasting for semester enrollments, regression analysis to predict revenue, all completed in both Baysian statistics and Frequentist statistics. 

One of the [more robust models I have created]{https://github.com/amslemp/Data_Science/tree/main/Predicting%20Retention} is the model for predicting retention. It required the incorporation of many sources of data, thoughtful feature engineering, and a combination of models. It ended in model deployment into a Power BI environment for the VPA to have immediate access. The impressive part of my retention model is that it was based on data we actually have available, rather than relying on factors that are only available some of the time. 

Over my decade of experience in Higher Ed, the biggest issue I have witnessed with almost any *real time* retention detection tool is that the people designing them have never worked in Academic Adivising, where many of these tools will be utilized the most. I have the fortune of having worked with nearly 18,000 students as an academic advisor and witnessed the roll out of numerous tools that failed spectacularly. The reason? They are trained on data that is not updated in real time! For instance, the most problematic data to train a model on <u>in higher education</u> is grades. I suspect (hope) it is better for K-12.

Faculty are notorious for not having grades updated in the system throughout the semester in a timely fashion. I have been on that side having taught in higher ed for seven years. It is difficult to get all the grades in every week when they should be; so I do not have judgment there. Some faculty are often weeks behind in their grading. Consequently, what good is it to train a *real time* retention model with grades as one of the indicators if you will not have timely access to those grades? 

I remember reaching out to students as an advisor with these tools indicating a student was in the red, meaning they were high risk for not persisting, only to have the student respond in shock as they were unaware they were failing since their professor (or professors) had not entered any grades yet for the semester (four weeks in)! Sure enough, when I went into the Canvas shells of the classes, the professor had not entered the grades yet, weeks behind. This created false positives, not a few, but enough that we scrapped that program after only one year of use. 

So my number one goal with my retention model was to build it on reliable data that we actually have access to, and it worked. It correctly identifies students who are most likely to not retain from Fall to Fall with 90.00% accuracy. 

# The Data

The data is pulled from Oracle's Banner DB using PL/SQL. Again, I can share the code but not the data.
