# Purpose

One of our executives (a Dean) wanted to know if an intervention we started in Fall 2024 to bring in more customers (students) impacted student persistence (i.e. reenrolling from Fall to Spring). These *treated* students were tracked and analyzed to see if their persistence was, indeed, statistically significantly different than their peers.

# Methods

Difference-in-Differences (DiD) is a common way to carry out causal inference analysis on interventions such as these. Consequently, I carried out a DiD to ascertain whether there was a statistically significant difference in between the treatment and control groups' persistence. The actual jupyter notebook shows the entire analysis in detail so I will not belabor it here. I normally write up a written report to the stakeholder after I do these types of analysis. For this one, however, I submitted the jupyter notebook in HTML format so that the methods could be evaluated more thoroughly if anyone in the exec council wished to do so. 

# Results

Based on a robust Difference-in-Differences analysis with a large sample size, there is no statistically significant evidence that the intervention from the ECs had any effect on student persistence. The results hold across multiple significance thresholds ($\alpha$ = 0.01, $\alpha$ = 0.05, $\alpha$ = 0.10), and parallel trends were confirmed before and after treatment. Additionally, variance inflation factor (VIF) analysis did not indicate significant multicollinearity or confounding. Given these findings, the most likely explanation is that the intervention simply did not have a measurable impact on student persistence. This analysis was handed off to the executive council so that they have a robust analysis to make future decisions on. Given this analysis was recently completed, I cannot yet report how the executive team has chosen to use this analysis.
