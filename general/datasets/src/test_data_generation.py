import os
import pandas as pd
from random import choice, randint, seed
from time import time
from config import paths
from general.datasets.src.job_titles import job_titles

def generate_basic_test_data(num_rows):
    if not os.path.exists(paths.path_training_data_complete_prepared_basic):
        print(f'{paths.path_training_data_complete_prepared_basic} does not exist.')
        return

    seed(time())

    # Define data ranges for test data
    age_range = (18, 70)
    genders = ['Male', 'Female', 'Other']
    education_levels = ["Bachelor's", "Master's", "PhD", "High School"]
    years_of_experience_range = (0, 50)

    new_rows = []

    # Generate random values from defined ranges
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

    # Add data to file
    new_data = pd.DataFrame(new_rows)
    new_data.to_csv(paths.path_test_data_basic, index=False)

    print(f'{num_rows} test data generated.')

def expand_test_datas():
    original_csv_path = paths.path_test_data_basic
    expanded_csv_path = paths.path_test_data_expanded

    if not os.path.exists(original_csv_path):
        print(f'{original_csv_path} does not exist.')
        return

    original_data = pd.read_csv(original_csv_path)
    expanded_rows = []

    for index, row in original_data.iterrows():
        base_age = row['Age']
        base_education_level = row['Education Level']
        base_job_title = row['Job Title']
        base_years_of_experience = row['Years of Experience']

        # Expand every dataset for every gender
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

    print(f'Expanded test data generated and saved to {expanded_csv_path}.')

def remove_gender_age_and_age():
    basic_csv_path = paths.path_test_data_basic

    if not os.path.exists(basic_csv_path):
        print(f'{basic_csv_path} does not exist.')
        return

    basic_data = pd.read_csv(basic_csv_path)
    # Remove gender an age from dataset
    modified_data = basic_data.drop(columns=['Gender', 'Age'])

    # Save data to csv
    modified_data.to_csv(paths.path_test_data_without_gender, index=False)

    print(f'Modified test data saved to {paths.path_test_data_without_gender}.')
