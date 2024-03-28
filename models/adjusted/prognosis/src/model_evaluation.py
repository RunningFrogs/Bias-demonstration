import pandas as pd
from joblib import load
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from config import paths
import logging

# Setup logging
logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def evaluate_model():
    logging.info('Starting model evaluation.')

    # Load model
    try:
        model = load(paths.path_model_adjusted)
        logging.info('Model loaded successfully.')
    except FileNotFoundError:
        logging.error(f'Model file {paths.path_model_adjusted} not found.')
        print(f'Model file {paths.path_model_adjusted} not found.')
        return

    # Load evaluation data
    try:
        data = pd.read_csv(paths.path_evaluation_data_adjusted)
        logging.info('Evaluation data loaded successfully.')
    except FileNotFoundError:
        logging.error(f'Evaluation data file {paths.path_evaluation_data_adjusted} not found.')
        return

    X_test = data.drop(columns=['Salary'])
    y_true = data['Salary']

    # Prognose salaries
    y_pred = model.predict(X_test)
    logging.info('Predictions made on evaluation data.')

    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    average_salary = y_true.mean()
    rmse_ratio = rmse / average_salary
    logging.info('Metrics calculated.')

    metrics_output = (f'R²: {r2}\n'
                      f'RMSE: {rmse}\n'
                      f'RMSE in relation to average income: {rmse_ratio}\n')

    logging.info(f'Evaluation metrics: {metrics_output}')
    print(metrics_output)

    with open(paths.path_evaluation_metrics_adjusted, 'w') as file:
        file.write(metrics_output)

    logging.info(f'Metrics saved to {paths.path_evaluation_metrics_adjusted}.')
