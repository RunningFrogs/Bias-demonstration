import os
import pandas as pd
from joblib import load
from config import paths
import logging

# Setup logging
logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def prognose_interactive():
    logging.info('Starting interactive prognosis.')

    if not os.path.exists(paths.path_model_adjusted):
        logging.error(f'Model file {paths.path_model_adjusted} does not exist.')
        print(f'{paths.path_model_adjusted} does not exist.')
        return
    else:
        logging.info('Model file found.')

    # Load model
    trained_model = load(paths.path_model_adjusted)
    logging.info('Model loaded successfully.')

    # Query input data
    logging.info('Querying for input data.')
    age = float(input("Age: "))
    logging.info(f'Input Age: {age}')

    gender = input("Gender (Male/Female): ")
    logging.info(f'Input Gender: {gender}')

    education_level = input("Education Level (High School, Bachelor's, Master's, PhD): ")
    logging.info(f'Input Education Level: {education_level}')

    job_title = input("Job Title: ")
    logging.info(f'Input Job Title: {job_title}')

    years_of_experience = float(input("Years of Experience: "))
    logging.info(f'Input Years of Experience: {years_of_experience}')

    logging.info('Input data collected.')

    # Create a DataFrame from the input data
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'Education Level': [education_level],
        'Job Title': [job_title],
        'Years of Experience': [years_of_experience]
    })
    logging.info('DataFrame created from input data.')

    # Predict on input data
    predicted_salary = trained_model.predict(input_data)

    # Print predicted income
    predicted_income_msg = f'Predicted Income: ₹{predicted_salary[0]:,.0f}'
    print(predicted_income_msg)
    logging.info(f'Prognosed income: {predicted_income_msg}')
