from pathlib import Path
import joblib
from data_preparation import load_and_prepare_data
from model_training import train_xgboost_model

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
        data_path = f'{Path.cwd()}/data/processed/FA19 - FA23 Demographic Cleaned Dataset.csv'
    if model_path is None:
        model_path = Path.cwd() / 'models/xgb_retention_model.pkl'

    # Load and prepare data
    print(f"Loading and preparing data from {data_path}...")
    data = load_and_prepare_data(data_path)

    # Define model params
    params = {
        'max_depth': [3, 4, 5],
        'learning_rate': [0.1, 0.01, 0.001],
        'n_estimators': [100, 500, 1000],
        'colsample_bytree': [0.7, 0.8, 0.9],
        'subsample': [0.7, 0.8, 0.9]
    }

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

