import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from data_preparation import load_and_prepare_data

def train_xgboost_model(prepped_xgb, response, params):
    """
    Parameters:
        prepped_xgb (pd.DataFrame): Dataframe prepped for XGBoost.
        response (str): String of response variable name.
        params (dict): Parameters for GridSearch.
        
    Returns:
        XGBoost Model: Returns best xgboost model
        grid_search.best_params_: Returns ideal parameters for model

    """
    # Split data
    X = prepped_xgb.drop(response, axis = 1)
    y = prepped_xgb[response]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 101)

    # Encode categorical vars
    le = LabelEncoder()
    for col in X_train.columns:
        if X_train[col].dtype == 'object':
            X_train[col] = le.fit_transform(X_train[col].astype(str))
            X_test[col] = le.transform(X_test[col].astype(str))

    # Initialize and tune model
    xgb_clf = xgb.XGBClassifier(objective = 'binary:logistic', seed = 101)
    grid_search = GridSearchCV(
        xgb_clf, param_grid = params, cv = 5, n_jobs = -1, scoring = 'accuracy'
    )
    grid_search.fit(X_train, y_train)

    # Evaluate model
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    print('Best Parameters:', grid_search.best_params_)
    print('Accuracy:', accuracy_score(y_test, y_pred))
    print('Classification Report:\n', classification_report(y_test, y_pred))

    return best_model, grid_search.best_params_
    
