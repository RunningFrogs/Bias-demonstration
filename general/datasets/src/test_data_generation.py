import os
import pandas as pd
from random import choice, randint, seed
from time import time
from config import paths
from general.datasets.src.job_titles import job_titles
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_basic_test_data(num_rows):
    logging.info(f'Starting to generate {num_rows} rows of basic test data.')

    if not os.path.exists(paths.path_prepared_training_data_original):
        logging.error(f'{paths.path_prepared_training_data_original} does not exist.')
        print(f'{paths.path_prepared_training_data_original} does not exist.')
        return

    seed(time())

    age_range = (18, 70)
    genders = ['Male', 'Female', 'Other']
    education_levels = ["Bachelor's", "Master's", "PhD", "High School"]
    years_of_experience_range = (0, 50)

    new_rows = []

    for _ in range(num_rows):
        base_age = randint(*age_range)
        base_gender = choice(genders)
        base_education_level = choice(education_levels)
        base_job_title = choice(job_titles)
        base_years_of_experience = randint(*years_of_experience_range)

        new_row = {
            'Age': base_age,
            'Gender': base_gender,
            'Education Level': base_education_level,
            'Job Title': base_job_title,
            'Years of Experience': base_years_of_experience
        }
        new_rows.append(new_row)

    new_data = pd.DataFrame(new_rows)
    new_data.to_csv(paths.path_test_data_basic, index=False)

    logging.info(f'Basic test data generated and saved to {paths.path_test_data_basic}.')
    print(f'{num_rows} test data generated.')

def expand_test_datas():
    logging.info('Starting to expand test data.')

    original_csv_path = paths.path_test_data_basic
    expanded_csv_path = paths.path_test_data_expanded

    if not os.path.exists(original_csv_path):
        logging.error(f'{original_csv_path} does not exist.')
        print(f'{original_csv_path} does not exist.')
        return

    original_data = pd.read_csv(original_csv_path)
    expanded_rows = []

    for index, row in original_data.iterrows():
        base_age = row['Age']
        base_education_level = row['Education Level']
        base_job_title = row['Job Title']
        base_years_of_experience = row['Years of Experience']

        for gender in ['Male', 'Female', 'Other']:
            new_row = {
                'Age': base_age,
                'Gender': gender,
                'Education Level': base_education_level,
                'Job Title': base_job_title,
                'Years of Experience': base_years_of_experience
            }
            expanded_rows.append(new_row)

    expanded_data = pd.DataFrame(expanded_rows)
    expanded_data.to_csv(expanded_csv_path, index=False)

    logging.info(f'Expanded test data generated and saved to {expanded_csv_path}.')
    print(f'Expanded test data generated and saved to {expanded_csv_path}.')

def remove_gender_age_and_age():
    logging.info('Starting to remove "Gender" and "Age" columns from basic test data.')

    basic_csv_path = paths.path_test_data_basic

    if not os.path.exists(basic_csv_path):
        logging.error(f'{basic_csv_path} does not exist.')
        print(f'{basic_csv_path} does not exist.')
        return

    basic_data = pd.read_csv(basic_csv_path)
    modified_data = basic_data.drop(columns=['Gender', 'Age'])

    modified_data.to_csv(paths.path_test_data_without_gender, index=False)

    logging.info(f'Modified test data (without "Gender" and "Age") saved to {paths.path_test_data_without_gender}.')
    print(f'Modified test data saved to {paths.path_test_data_without_gender}.')
