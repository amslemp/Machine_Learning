# Purpose

This was commissioned by the Vice President of Acdemics and marketing. The goal was to create an interactive map that allows both the AVP and the marketing team to be able to dig into where our students come from, who they are, what they take at the college, and what majors they pursue, among other things. Since student data has a mix of variable types (categorical and numeric), then I had to use the K-Prototype algorithm for part of this analysis. 

For the creation of the map, I created a K-Means Geospatial Algorithm. 

# Data

The data is pulled from the Banner DB using PL/SQL. Since it is student data, the raw data files cannot be shared due to FERPA laws. 

# Results

Not every modeling technique ends up driving insights. I include this precisely because of that. The K-Means did not draw out any significant insights beyond what I already know about the student body. However, the K-Means Geospatial Clustering coupled with the Haversine formula worked splendidly to do what I needed. I incorporated this model into an interactive map along with student characteristics and shipped it to the marketing team and VPA so that they could strategically deploy their resources. For instance, because of this map, we are able to host strategic enrollment events in those locations either where we see pockets of opportunity or from where we already know students come. 
