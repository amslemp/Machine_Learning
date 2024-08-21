<center>
# Executive Summary
</center>

**Side Note**

The PDF shared here is the report turned into the Dean and Faculty member over the course that was analyzed. They are the audience. Since this report was written for academics, the length and depth of the report is more extensive because that is what is appropriate in this academic setting. When I do analysis for others who are not looking for this level of analysis, the reports are much more brief and less technical. Moreover, when my work does not involve a causal analysis like this but rather is a ML model for deployment, usually I am the only one interested in the technical metrics. My end users simply want the model to work and be accurate in its recommendations or predictions.

********

For years now, a professor at the college and I have spoken about me conducting a proper analysis of PD 12x and its effects on student persistence over time. This is that analysis. To properly carry this out, propensity score matching (PSM) was used to create a control group for the treatment group, the treatment being students enrolled in PD 12x. PSM is the gold standard of observational studies that allows us to most closely replicate the conditions we have in Randomized Controlled Trials (RCTs). Moreover, PSM is a causal inference analysis, which allows us to declare at its conclusion whether it is reasonable or not to suggest that PD 12x does not have a causal relationship with student persistence. After the control group was matched to the treatment group, logistic regression was employed to examine the effects of the predictors on the binary response variable of “Persisted”/”Not Persisted.”

This analysis included the last five Fall and Spring semesters, examining students who persisted from Fall to Spring and Spring to Fall. When PD 12x is included in a multivariate analysis with other predictors like demographics, student type, age, credit hours attempted and earned, and GPA, PD 12x is found to have no statistically significant effect on student persistence (p = 0.564353). Additionally, a Likelihood Ratio Test (LRT) found that the inclusion of whether a student took PD 12x or not in the predictive model had absolutely no effect on the model’s ability to correctly identify students who would persist (p = 0.8972). Therefore, we can reasonably conclude that a student taking PD 12x does not have a causal relationship with student persistence. 

If we were to require PD 12x (or its new code, “PD 13x”) for all new students and provide it for free, it would conservatively amount to over $350,000 a year of credit free credit hours, not including the cost of salaries for the instructors. 

This analysis is a great cautionary tale of why we should not rely on simple heuristics where you isolate students who took PD 12x and then just look at the proportion who persist to the next semester against the proportion of non-PD 12x students who persist. This simple univariate analysis will never be as robust as a multivariate statistical analysis that utilizes propensity score matching and logistic regression.

# Outcome

As a result of this analysis, the college did not move forward on this proposal, which saved the college, conservatively, $350,000 annually.

