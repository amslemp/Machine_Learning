# Gridsearch for xgboost model training
PARAMS = {
    'max_depth': [3, 4, 5],
    'learning_rate': [0.1, 0.01, 0.001],
    'n_estimators': [100, 500, 1000],
    'colsample_bytree': [0.7, 0.8, 0.9],
    'subsample': [0.7, 0.8, 0.9]
}

# Path to data
DATA_PATH = f'{Path.cwd()}/data/processed/FA19 - FA23 Demographic Cleaned Dataset.csv'

# Path to trained model
MODEL_PATH = Path.cwd()/'models/xgb_retention_model.pkl'
