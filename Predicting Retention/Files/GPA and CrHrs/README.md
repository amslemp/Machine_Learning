# GPA and CrHr Data

Data is pulled from Oracle's Banner DB using Argos, and internal tool for pulling the data. The data is pulled using ZALLGPA and stored in the format `202080 GPA and Crhrs.csv`. The folder should always have the previous **four** Fall semesters but exclude the current Fall semester. This is because the model is training retention from one Fall to the next. The current Fall semester's retention cannot be calculated because it is based on the proportion of students from the current Fall that will enroll in the next Fall semester. 
