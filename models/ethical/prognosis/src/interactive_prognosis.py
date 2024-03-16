import os
import pandas as pd
from joblib import load
from config import paths
import logging

# Set up logging
logging.basicConfig(filename=paths.path_log_model_ethical, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prognose_interactive():
    logging.info('Starting the interactive prognose process.')

    if not os.path.exists(paths.path_model_ethical):
        logging.error(f'{paths.path_model_ethical} does not exist.')
        print(f'{paths.path_model_ethical} does not exist.')
        return
    else:
        logging.info(f'Found model at {paths.path_model_ethical}.')

    # Load model
    trained_model = load(paths.path_model_ethical)
    logging.info('Model loaded successfully.')

    # Query input data
    logging.info('Querying for input data.')
    education_level = input("Education Level (High School, Bachelor's, Master's, PhD): ")
    job_title = input("Job Title: ")
    years_of_experience = float(input("Years of Experience: "))

    # Create a DataFrame from the input data
    input_data = pd.DataFrame({
        'Education Level': [education_level],
        'Job Title': [job_title],
        'Years of Experience': [years_of_experience]
    })
    logging.info('Input data collected and DataFrame created.')

    # Predict on input data
    predicted_salary = trained_model.predict(input_data)
    logging.info('Prediction made on input data.')

    # Print predicted income
    print(f'Predicted Income: ₹{predicted_salary[0]:,.0f}')
    logging.info(f'Predicted Income: ₹{predicted_salary[0]:,.0f}')
