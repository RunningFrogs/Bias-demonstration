import os
import pandas as pd
from joblib import load
import logging
from config import paths

# Set up logging
logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prognose_automated():
    logging.info('Starting the automated prognosis process.')

    # Check if file paths exist
    if not os.path.exists(paths.path_test_data_expanded):
        logging.error(f'{paths.path_test_data_expanded} does not exist.')
        print(f'{paths.path_test_data_expanded} does not exist.')
        return
    else:
        logging.info(f'Found test data at {paths.path_test_data_expanded}.')

    if not os.path.exists(paths.path_model_adjusted):
        logging.error(f'{paths.path_model_adjusted} does not exist.')
        print(f'{paths.path_model_adjusted} does not exist.')
        return
    else:
        logging.info(f'Found model at {paths.path_model_adjusted}.')

    # Load model
    trained_model = load(paths.path_model_adjusted)
    logging.info('Model loaded successfully.')

    # Load input data from CSV
    input_data = pd.read_csv(paths.path_test_data_expanded)
    logging.info(f'Input data loaded successfully. {input_data.shape[0]} rows with {input_data.shape[1]} attributes.')
    print(f'Input data loaded successfully. {input_data.shape[0]} rows with {input_data.shape[1]} attributes.')

    # Check for missing values in input data
    if input_data.isnull().values.any():
        missing_values_count = input_data.isnull().sum().sum()
        logging.warning(f'Input data contains {missing_values_count} missing values. These may affect the predictions.')

    # Predict on input data
    predicted_salaries = trained_model.predict(input_data)
    logging.info('Predictions made on input data.')

    # Log summary of predictions
    avg_salary = predicted_salaries.mean()
    min_salary = predicted_salaries.min()
    max_salary = predicted_salaries.max()
    logging.info(f'Summary of predictions - Avg: {avg_salary:.2f}, Min: {min_salary}, Max: {max_salary}')
    print(f'Summary of predictions - Avg: {avg_salary:.2f}, Min: {min_salary}, Max: {max_salary}')
    # Add the predictions to the test_data DataFrame
    input_data['Salary'] = predicted_salaries

    # Save the DataFrame with the predictions to a new CSV file
    input_data.to_csv(paths.path_prognosed_data_adjusted, index=False)
    logging.info(f'Predictions saved at {paths.path_prognosed_data_adjusted}.')
    print(f'Predictions saved at {paths.path_prognosed_data_adjusted}.')
