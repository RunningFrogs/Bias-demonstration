import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config import paths
import logging

# Log file configuration
logging.basicConfig(filename=paths.path_log_model_original, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prepare_training_data_basic():
    if not os.path.exists(paths.path_unprepared_training_data):
        logging.error(f'Unprepared training data file {paths.path_unprepared_training_data} does not exist.')
        print(f'{paths.path_unprepared_training_data} does not exist.')
        return

    logging.info('Starting the preparation of the training data.')

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(paths.path_unprepared_training_data)
    logging.info('Unprepared training data loaded successfully.')

    # Log information about rows with missing data before removal
    missing_data_info = df[df.isnull().any(axis=1)]
    if not missing_data_info.empty:
        logging.info(f'Removing rows due to missing data. Rows affected: {len(missing_data_info)}')

    # Clean and format the DataFrame
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
    logging.info('Education level strings formatted.')

    # Remove rows with any missing values
    df = df.dropna(how='any')

    # Convert numerical fields to integers
    df['Salary'] = df['Salary'].astype(int)
    df['Years of Experience'] = df['Years of Experience'].astype(int)
    df['Age'] = df['Age'].astype(int)
    logging.info('Numerical fields formatted and rows with missing values removed.')

    # Split the data
    train_data, eval_data = train_test_split(df, test_size=0.2, random_state=42)
    logging.info('Data split into training and evaluation datasets.')

    # Save the datasets
    train_data.to_csv(paths.path_prepared_training_data_original, index=False)
    eval_data.to_csv(paths.path_evaluation_data, index=False)
    logging.info('Training and evaluation datasets saved.')

    print(f'Training data saved at {paths.path_prepared_training_data_original}.')
    print(f'Evaluation data saved at {paths.path_evaluation_data}.')
