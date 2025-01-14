# Student Retention Model
This project predicts student enrollment behavior using an XGBoost model. The pipeline includes data cleaning, model training, and making predictions on new data.

## File Flow

### Data Cleaning

The base of the pipeline is `data_cleaning.py`. Subsequent scripts depend on this step to provide imputed, formatted, feature engineered, and restructured data.

- **`data_cleaning.py`**
  - The main script that orchestrates the data cleaning process.
  - Cleans and wrangles data from Enrollment, GPA and Crhrs, Pell and Loan, Location, and High School Enrollment.
    - After cleaning, combines all of the elements, engineered features, and imputed data into one dataframe.
  - **Used by**:
    - `pipeline_steps.py`: Contains modular functions for specific pipeline operations.
    - `main_pipeline.py`: Pipeline that executes all of the cleaning/wrangling code.

### Model Development

Data cleaning feeds into the model training phase, where the cleaned data is preped, the model is trained, and the results are saved.

- **`main_pipeline.py`**
  - **Used by**:
      - `data_preparation.py`: Formats data for the XGBoost model.
      - **Used by**:
        - `model_training.py`: Trains model and tunes hyperparameters.
          - Trains the XGBoost model using prepared data.
          - **Used by**:
            - `run_training.py`: Runs the full model training pipelineand saves the model to specified folder as a .pkl file.

---

### Prediction

Once the model is trained and saved, it is used to make predictions on the new, unseen data.

- **`prediction.py`**
  - Loads the trained model and generates predictions on new, unseen data.
  - Saves predictions to specified folder for use in Power BI dashboard.

---
