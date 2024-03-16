import os
import pandas as pd
from joblib import load
import logging
from config import paths

# Set up logging
logging.basicConfig(filename=paths.path_log_model_ethical, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prognose_automated():
    logging.info('Starting the automated prognose process.')

    if not os.path.exists(paths.path_test_data_basic):
        logging.error(f'{paths.path_test_data_basic} does not exist.')
        print(f'{paths.path_test_data_basic} does not exist.')
        return
    else:
        logging.info(f'Found test data at {paths.path_test_data_basic}.')

    if not os.path.exists(paths.path_model_ethical):
        logging.error(f'{paths.path_model_ethical} does not exist.')
        print(f'{paths.path_model_ethical} does not exist.')
        return
    else:
        logging.info(f'Found model at {paths.path_model_ethical}.')

    # Load model
    trained_model = load(paths.path_model_ethical)
    logging.info('Model loaded successfully.')

    # Load input data from CSV
    input_data = pd.read_csv(paths.path_test_data_basic)
    logging.info('Input data loaded successfully.')

    # Predict on input data
    predicted_salaries = trained_model.predict(input_data)
    logging.info('Predictions made on input data.')

    # Add the predictions to the test_data DataFrame
    input_data['Salary'] = predicted_salaries

    # Save the DataFrame with the predictions to a new CSV file
    input_data.to_csv(paths.path_prognosed_data_ethical, index=False)
    logging.info(f'Predictions saved at {paths.path_prognosed_data_ethical}.')
    print(f'Predictions saved at {paths.path_prognosed_data_ethical}.')
