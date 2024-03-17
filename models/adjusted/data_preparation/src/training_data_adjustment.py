import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config import paths
import logging
import numpy as np

# Log file configuration
logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def balance_genders(df):

    unique_genders = df['Gender'].unique()
    unique_jobs = df.groupby(['Education Level', 'Job Title', 'Years of Experience']).size().reset_index().drop(0, axis=1)


    def generate_synthetic_data(row, gender):
        synthetic_row = row.copy()
        synthetic_row['Gender'] = gender

        return synthetic_row

    balanced_df = pd.DataFrame()
    for _, job in unique_jobs.iterrows():
        job_mask = (df['Education Level'] == job['Education Level']) & \
                   (df['Job Title'] == job['Job Title']) & \
                   (df['Years of Experience'] == job['Years of Experience'])

        job_df = df[job_mask]
        max_count = job_df['Gender'].value_counts().max()


        for gender in unique_genders:
            gender_df = job_df[job_df['Gender'] == gender]

            if gender_df.empty:

                synthetic_data = generate_synthetic_data(job_df.iloc[0], gender)
                gender_df = pd.DataFrame([synthetic_data])


            resampled_gender_df = gender_df.sample(n=max_count, replace=True, random_state=42).reset_index(drop=True)
            balanced_df = pd.concat([balanced_df, resampled_gender_df], axis=0)

    logging.info('Dataset adjusted with synthetic data to ensure every gender is represented in each job equally.')
    return balanced_df.reset_index(drop=True)


def standardize_salaries(df):
    """
    Adjust salaries to ensure equal pay for equal work across all genders.
    """
    # Ermitteln Sie den allgemeinen Median des Gehalts für jede Jobkombination, unabhängig vom Geschlecht
    median_salary_mapping = df.groupby(['Education Level', 'Job Title', 'Years of Experience'])[
        'Salary'].median().reset_index(name='Fair Median Salary')

    # Verbinden Sie das ursprüngliche DataFrame mit dem Mapping, um den fairen Medianwert hinzuzufügen
    df = pd.merge(df, median_salary_mapping, on=['Education Level', 'Job Title', 'Years of Experience'], how='left')

    # Aktualisieren Sie das Gehalt auf den fairen Medianwert, um gleiche Bezahlung für gleiche Arbeit zu gewährleisten
    df['Salary'] = df['Fair Median Salary']
    df.drop(columns=['Fair Median Salary'], inplace=True)

    logging.info('Salaries adjusted for fairness across genders.')
    return df


def prepare_training_data():
    if not os.path.exists(paths.path_unprepared_training_data):
        logging.error(f'Unprepared training data file {paths.path_unprepared_training_data} does not exist.')
        print(f'{paths.path_unprepared_training_data} does not exist.')
        return

    logging.info('Starting the advanced preparation of the training data.')

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

    # Balance genders in the dataset
    df = balance_genders(df)

    # Standardize salaries across genders for equal work
    df = standardize_salaries(df)

    # Split the data
    train_data, eval_data = train_test_split(df, test_size=0.2, random_state=42)
    logging.info('Data split into training and evaluation datasets.')

    # Save the datasets
    train_data.to_csv(paths.path_prepared_training_data_adjusted, index=False)
    eval_data.to_csv(paths.path_evaluation_data_adjusted, index=False)
    logging.info('Training and evaluation datasets saved.')

    print(f'Training data saved at {paths.path_prepared_training_data_adjusted}.')
    print(f'Evaluation data saved at {paths.path_evaluation_data_adjusted}.')
