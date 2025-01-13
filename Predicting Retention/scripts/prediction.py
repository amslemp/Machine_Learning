import pandas as pd
from pathlib import Path
import joblib
from sklearn.preprocessing import LabelEncoder

def preprocess_data(input_data, model_features, categorical_features):
    """
    Preprocesses new input data for the trained model.

    Parameteres:
        input_data (pd.DataFrame): New data to run predictions on.
        model_features (list): The list of features used during training.
        categorical_features (list): The list of categorical features that need encoding.

    Returns:
        Pd.DataFrame: Preprocessed data ready for prediction.
    """
    # Select only the features used for training
    input_data = input_data[model_features]

    # Encode categorical variables
    le = LabelEncoder()
    for col in categorical_features:
        if col in input_data.columns:
            input_data[col] = le.fit_transform(input_data[col].astype(str))

    return input_data

def load_model(model_path):
    """
    Loads the trained model from a pickle file.

    Parameters:
        model_path (str): Path to pickle file.

    Returns:
        Trained model

    """
    return joblib.load(model_path)

def predict(model, preprocessed_data):
    """
    Uses the trained model to make predictions on the new data.

    Parameters:
        model: The trained model.
        preprocessed_data (pd.DataFrame): Preprocessed data ready for prediction.

    Returns:
        np.ndarray: Predictions made by the model.

    """
    return model.predict(preprocessed_data)

if __name__ == "__main__":
    MODEL_PATH = Path.cwd() / 'models/xgb_retention_model.pkl'
    INPUT_DATA_PATH = Path.cwd() / 'data/new_data/new_cleaned_data.csv'
    OUTPUT_PATH = Path.cwd() / 'data/predictions/predictions.csv'

    # Load the model
    model = load_model(MODEL_PATH)

    # Load new data
    new_data = pd.read_csv(INPUT_DATA_PATH)

    # Define features
    model_features = ['stype', 'gender', 'ethn_desc', 'resd', 'fully_online', 'acd_std_desc', 'age', 
                      'term_att_crhr', 'term_earn_crhr', 'term_gpa', 'inst_gpa', 'inst_earned', 'no_pell',
                      'pell', 'subsidized', 'unsubsidized', 'summer_plus', 'kansas_promise', 'all_fafsa', 
                      'hs_matriculation']

    # Isolate categorical features
    cat_features = ['stype', 'gender', 'ethn_desc', 'resd', 'fully_online', 'acd_std_desc', 'hs_matriculation']

    # Preporcess new data
    preprocessed_data = preprocess_data(new_data, model_features, cat_features)

    # Generate predictions
    predictions = predict(model, preprocessed_data)

    # Save predictions
    output = new_data.copy()
    output['predicted_enrollment'] = predictions
    OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
    output.to_csv(OUTPUT_PATH, index = False)
