from pathlib import Path
import joblib
from data_preparation import load_and_prepare_data
from model_training import train_xgboost_model
from model_parameters import (
    PARAMS,
    DATA_PATH,
    MODEL_PATH
)

def run_pipeline(data_path=None, model_path=None):
    """
    Runs the training pipeline.

    Parameters:
    - data_path (str or Path, optional): Path to the dataset file. Defaults to a predefined path.
    - model_path (str or Path, optional): Path to save the trained model. Defaults to a predefined path.

    Returns:
    - best_model: The trained model.
    - best_params: The parameters of the best model.
    """
    # Define default paths if not provided
    if data_path is None:
        data_path = DATA_PATH
    if model_path is None:
        model_path = MODEL_PATH

    # Load and prepare data
    print(f"Loading and preparing data from {data_path}...")
    data = load_and_prepare_data(data_path)

    # Define model params
    params = PARAMS

    # Train the model
    print("Training the model...")
    best_model, best_params = train_xgboost_model(data, response='enrolled', params=params)

    # Save the trained model
    model_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving the trained model to {model_path}...")
    joblib.dump(best_model, model_path)

    print("Training pipeline completed successfully!")
    return best_model, best_params

if __name__ == "__main__":
    run_pipeline()

