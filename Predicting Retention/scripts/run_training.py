
from pathlib import Path
import joblib
from data_preparation import load_and_prepare_data
from model_training import train_xgboost_model

if __name__ == "__main__":
    # Paths
    DATA_PATH = f'{Path.cwd()}/data/processed/FA19 - FA23 Demographic Cleaned Dataset.csv'
    MODEL_PATH = Path.cwd()/'models/xgb_retention_model.pkl'

    # load and prepare data
    data = load_and_prepare_data(DATA_PATH)

    # Define model params
    params = {
                        'max_depth': [3, 4, 5],
                        'learning_rate': [0.1, 0.01, 0.001],
                        'n_estimators': [100, 500, 1000],
                        'colsample_bytree': [0.7, 0.8, 0.9],
                        'subsample': [0.7, 0.8, 0.9]
                    }

    # Train model
    best_model, best_params = train_xgboost_model(data, response = 'enrolled', params = params)

    # Save trained model
    MODEL_PATH.parent.mkdir(parents = True, exist_ok = True)
    joblib.dump(best_model, MODEL_PATH)
    
