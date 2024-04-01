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
import logging
from config import paths

# Setup logging
logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model():
    logging.info('Training model started.')

    if not os.path.exists(paths.path_prepared_training_data_adjusted):
        logging.error(f'{paths.path_prepared_training_data_adjusted} does not exist.')
        print(f'{paths.path_prepared_training_data_adjusted} does not exist.')
        return

    # Load training data
    training_data = pd.read_csv(paths.path_prepared_training_data_adjusted)
    logging.info('Training data loaded.')

    x = training_data.drop('Salary', axis=1)
    y = training_data['Salary']

    # Split training and test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=60)
    logging.info('Training and test data split.')

    # Define categorical and numerical features
    categorical_features = ['Gender', 'Education Level', 'Job Title']
    numerical_features = ['Age', 'Years of Experience']

    # Create ColumnTransformer to process numerical and categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', RobustScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    logging.info('Preprocessor setup.')

    # Pipeline with preprocessor
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', GradientBoostingRegressor(random_state=42))])
    logging.info('Pipeline setup.')

    # Define GridSearchCV parameters
    param_grid = {
        'regressor__n_estimators': [100, 500, 1000],
        'regressor__learning_rate': [0.05, 0.1],
        'regressor__max_depth': [3, 6, 9],
        'regressor__min_samples_split': [2, 5],
        'regressor__subsample': [0.75, 1.0]
    }
    logging.info('GridSearchCV parameters defined.')
    logging.info(f'n_estimators: [100, 500, 1000]')
    logging.info(f'learning_rate: [0.05, 0.1]')
    logging.info(f'max_depth: [3, 6, 9]')
    logging.info(f'min_samples_split: [2, 5]')
    logging.info(f'subsample: [0.75, 1.0]')

    # Create GridSearchCV
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error', verbose=3, n_jobs=-1)
    logging.info('GridSearchCV setup.')
    logging.info(f'scoring=neg_mean_sqaured_error')
    logging.info(f'verbose=3')
    logging.info(f'n_jobs=-1')

    # Train model using GridSearchCV
    grid_search.fit(x_train, y_train)
    logging.info('Model training completed with GridSearchCV.')

    best_model = grid_search.best_estimator_
    logging.info(f'Best model determined: {grid_search.best_params_}')

    # Extract feature importances
    feature_importances = best_model.named_steps['regressor'].feature_importances_
    # Get feature names from the preprocessor
    feature_names = numerical_features + \
                    list(best_model.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features))

    # Combine feature names with their importances and sort descending
    features_importances_sorted = sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True)
    # Save detailed feature importances
    feature_importances_df = pd.DataFrame(features_importances_sorted, columns=['Feature', 'Importance'])
    feature_importances_df.to_csv(paths.path_feature_importances_detailed, index=False)
    logging.info('Feature importances extracted, sorted, and saved.')

    # Aggregate importances for categorical features
    aggregate_importances = {}
    for feature, importance in features_importances_sorted:
        category = next((cat for cat in categorical_features if feature.startswith(cat)), None)
        if category:
            aggregate_importances[category] = aggregate_importances.get(category, 0) + importance
        else:
            aggregate_importances[feature] = importance
    # Save aggregated importances
    aggregate_importances_df = pd.DataFrame(list(aggregate_importances.items()), columns=['Category/Feature', 'Importance'])
    aggregate_importances_df.to_csv(paths.path_feature_importances_category, index=False)
    logging.info('Aggregate feature importances extracted and saved.')

    # Evaluate and save model metrics
    y_pred = best_model.predict(x_test)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)  # Ensure predictions are not negative
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    average_salary = y_test.mean()
    rmse_ratio = rmse / average_salary

    metrics_output = (f'Best parameters: {grid_search.best_params_}\n'
                      f'R²: {r2}\n'
                      f'RMSE: {rmse}\n'
                      f'RMSE in relation to average income: {rmse_ratio}\n')

    print(metrics_output)
    print(f'Aggregate importances: {aggregate_importances_df}\n')

    with open(paths.path_training_metrics_adjusted, 'w') as file:
        file.write(metrics_output)

    logging.info(f'Metrics: {metrics_output}')
    logging.info('Model evaluation metrics calculated and saved.')

    # Save the model
    dump(best_model, paths.path_model_adjusted)
    logging.info('Model saved.')

    logging.info('Training model process completed.')

