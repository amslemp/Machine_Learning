# Forecasting Model

This model is the primary driver of daily revenues for the organization and has been in production for five years now. It is batch updated daily to show previous day's revenue and projected revenue for the following five days. In the presentation, it compares the previous five years of revenues by day of the year (not date). 

## Pipeline Dependencies

`utlities.py`: This module holds the csv opening script. It is utilized in the `dashboard_pipeline.py` module. 
`preprocess.py`: Module that sets up all of the data. This module does the heavy lifting. 
    | `dashboard_pipeline.py`: Module creates the pipeline that is executed. 
        | `run_pipeline.py`: Module that executes pipeline in production.

This is just the first step of the daily revenues model.
