import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from joblib import dump
from config import paths

def train_model():
    if not os.path.exists(paths.path_prepared_training_data_no_gender):
        print(f'{paths.path_prepared_training_data_no_gender} does not exist.')
        return

    # Load training data
    training_data = pd.read_csv(paths.path_prepared_training_data_no_gender)

    x = training_data.drop('Salary', axis=1)
    y = training_data['Salary']

    # Split training and test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=60)

    # Define categorical and numerical features
    categorical_features = ['Education Level', 'Job Title']
    numerical_features = ['Years of Experience']

    # Create ColumnTransformer to process numerical and categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', RobustScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # Pipeline with preprocessor
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', GradientBoostingRegressor(random_state=42))])

    # Define GridSearchCV parameters
    param_grid = {
        'regressor__n_estimators': [100, 500, 1000],
        'regressor__learning_rate': [0.05, 0.1],
        'regressor__max_depth': [3, 6, 9],
        'regressor__min_samples_split': [2, 5],
        'regressor__subsample': [0.75, 1.0]
    }

    # Create GridSearchCV
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error', verbose=3, n_jobs=-1)

    # Train model using GridSearchCV
    grid_search.fit(x_train, y_train)

    best_model = grid_search.best_estimator_

    # Evaluate model
    y_pred = best_model.predict(x_test)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)  # Ensure predicted values are not negative

    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    average_salary = y_test.mean()
    rmse_ratio = rmse / average_salary

    # Print metrics and best parameters
    print(f'Best parameters: {grid_search.best_params_}')
    print(f'R²: {r2}')
    print(f'RMSE: {rmse}')
    print(f'RMSE in relation to average income: {rmse_ratio}')

    # Save metrics in text file
    with open(paths.path_training_metrics_no_gender, 'w') as file:
        file.write(f'Best parameters: {grid_search.best_params_}\n')
        file.write(f'R²: {r2}\n')
        file.write(f'RMSE: {rmse}\n')
        file.write(f'RMSE in relation to average income: {rmse_ratio}\n')

    # Save model
    dump(best_model, paths.path_model_no_gender)
