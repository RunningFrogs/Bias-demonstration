import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config import paths
import logging

# Konfiguriere das Logging
logging.basicConfig(filename=paths.path_log_model_no_gender, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def prepare_etical_data():
    logging.info('Starting to prepare ethical data.')

    if not os.path.exists(paths.path_unprepared_training_data):
        logging.error(f'{paths.path_unprepared_training_data} does not exist.')
        print(f'{paths.path_unprepared_training_data} does not exist.')
        return
    else:
        logging.info(f'Found unprepared training data at {paths.path_unprepared_training_data}.')

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(paths.path_unprepared_training_data)
    logging.info('Unprepared training data loaded successfully.')

    # Remove the 'Gender' and 'Age' columns
    df = df.drop(columns=['Gender', 'Age'])
    logging.info("Removed attributes 'Gender' and 'Age' from the data.")

    # Format education strings in the DataFrame
    df = df.replace({
        "Bachelor['’]?s? Degree": "Bachelor",
        "Bachelor['’]?s?": "Bachelor",
        "Master['’]?s? Degree": "Master",
        "Master['’]?s?": "Master",
        "[Pp][Hh][Dd]": "PhD",
        "Doctorate": "PhD",
        "High School Diploma": "High School",
        "High School": "High School"
    }, regex=True)
    logging.info('Education level strings formatted successfully.')

    # Clean the DataFrame by removing rows with any missing values
    df = df.dropna(how='any')
    logging.info('Removed rows with missing values.')

    # Remove decimal places from 'Salary' and convert 'Years of Experience' to integers
    df['Salary'] = df['Salary'].astype(int)
    df['Years of Experience'] = df['Years of Experience'].astype(int)
    logging.info("Formatted 'Salary' and 'Years of Experience' columns.")

    # Split the data into training and evaluation datasets (80% training, 20% evaluation)
    train_data, eval_data = train_test_split(df, test_size=0.2, random_state=42)
    logging.info('Split data into training and evaluation datasets.')

    # Write the training data to a new CSV file
    train_data.to_csv(paths.path_prepared_training_data_no_gender, index=False)
    logging.info(f'Training data saved at {paths.path_prepared_training_data_no_gender}.')

    # Write the evaluation data to a separate CSV file
    eval_data.to_csv(paths.path_evaluation_data_no_gender, index=False)
    logging.info(f'Evaluation data saved at {paths.path_evaluation_data_no_gender}.')
