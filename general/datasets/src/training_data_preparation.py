import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config import paths
import logging


def prepare_training_data_basic():
    # Log-Datei konfigurieren
    logging.basicConfig(filename=paths.logging_path, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    if not os.path.exists(paths.path_unprepared_training_data):
        logging.info(f'{paths.path_unprepared_training_data} does not exist.')
        print(f'{paths.path_unprepared_training_data} does not exist.')
        return

    logging.info('Starting data preparation.')

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(paths.path_unprepared_training_data)

    # Protokollieren, welche Zeilen wegen fehlender Daten entfernt werden
    missing_data_info = df[df.isnull().any(axis=1)]
    if not missing_data_info.empty:
        logging.info(f'Removing rows due to missing data: \n{missing_data_info}')

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

    # Clean the DataFrame by removing rows with any missing values
    df = df.dropna(how='any')

    # Remove decimal places
    df['Salary'] = df['Salary'].astype(int)
    df['Years of Experience'] = df['Years of Experience'].astype(int)
    df['Age'] = df['Age'].astype(int)

    # Split the data into training and evaluation datasets (80% training, 20% evaluation)
    train_data, eval_data = train_test_split(df, test_size=0.2, random_state=42)
    logging.info(f'Training data and evaluation data splitted.')

    # Write the training data to a new CSV file
    train_data.to_csv(paths.path_prepared_training_data_original, index=False)

    # Write the evaluation data to a separate CSV file
    eval_data.to_csv(paths.path_evaluation_data, index=False)

    # Log what was done
    logging.info(f'Training data prepared and saved at {paths.path_prepared_training_data_original}.')
    logging.info(f'Evaluation data prepared and saved at {paths.path_evaluation_data}.')

    print(f'Training data saved at {paths.path_prepared_training_data_original}.')
    print(f'Evaluation data saved at {paths.path_evaluation_data}.')

