import os
import pandas as pd
from joblib import load
import logging
from config import paths

# Set up logging
logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add exact logging, prognosis data inputs, outputs etc.

def prognose_automated():
    logging.info('Starting the automated prognose process.')

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
    logging.info('Input data loaded successfully.')

    # Predict on input data
    predicted_salaries = trained_model.predict(input_data)
    logging.info('Predictions made on input data.')

    # Add the predictions to the test_data DataFrame
    input_data['Salary'] = predicted_salaries

    # Save the DataFrame with the predictions to a new CSV file
    input_data.to_csv(paths.path_prognosed_data_adjusted, index=False)
    logging.info(f'Predictions saved at {paths.path_prognosed_data_adjusted}.')
    print(f'Predictions saved at {paths.path_prognosed_data_adjusted}.')
