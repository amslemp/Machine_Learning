# Purpose

This is an application of a Mixed Effects Model to synthetic data I made up for a young researcher I met while diving in Roatan. As my wife and I spoke with her, she mentioned she was conducting research on the fish populations at different dive sites and continuing the research of pervious researchers. She was considering what kind of model to use to evaluate her data asked me if a Mixed Effects Model was appropriate. Since we were there to dive, I did not directly address it while we were there. Consequently, when I returned home, I created a synthetic dataset based both on some data I could retrieve from the internet and from my experience as a SCUBA diver. 

After creating the data, I compared three different models, Mixed Effects, Multiple Linear Regression, and a Generalized Additive Model. Each step along the way, I explained what I did and why, what I am looking for and what the results tell me. The researcher had access to R so she was able to run my code and see what to what I was referring. 

# The Data

As I mentioned, the dataset is a sythetic dataset to try to model what I would expect to see in Fish species' size and counts based on different depths. Then I also considered the temperature of the water year-round as well as the temperature at different depths. Obviously as you dive further down, the temperature will vary, though not dramatically for the depths that divers will be observing fish. Counts of fish also tend to be much higher at shallower depths and fewer at deeper depths. 

# Results

After evaluating all the models using MSE and $R^2$, the MEM, for my synthetic data, was the better performer. Again, the goal was to show this new researcher how I would approach the data and evaluating various modeling techniques. I also gave her some suggestions on other models that might be more appropriate depending on the characteristics of her data. 

Happily, I can report that this analysis assisted her in the development and analysis of her research. Unfortunately, it is not yet ready for publication. 
