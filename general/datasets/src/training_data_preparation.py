import os
import pandas as pd
from config import paths

def prepare_training_data_basic():
    if not os.path.exists(paths.path_unprepared_training_data):
        print(f'{paths.path_unprepared_training_data} does not exist.')
        return

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(paths.path_unprepared_training_data)

    missing_data_info = df[df.isnull().any(axis=1)]
    if not missing_data_info.empty:
        print(f'Removing rows due to missing data. Rows affected: {len(missing_data_info)}')

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

    # Remove rows with any missing values
    df = df.dropna(how='any')

    # Convert numerical fields to integers
    df['Salary'] = df['Salary'].astype(int)
    df['Years of Experience'] = df['Years of Experience'].astype(int)
    df['Age'] = df['Age'].astype(int)

    # Save the cleaned datasets
    df.to_csv(paths.path_training_data_complete_prepared_basic, index=False)

    print(f'Cleaned training data saved at {paths.path_training_data_complete_prepared_basic}.')
