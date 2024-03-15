# Dateiname: generate_test_data.py

import os
import pandas as pd
from random import choice, randint, seed
from time import time
from config import paths
from data_generation import job_titles

def generate_base_test_data(num_rows):
    if not os.path.exists(paths.path_prepared_training_data):
        print(f'{paths.path_prepared_training_data} does not exist.')
        return

    seed(time())

    # Define test data range
    age_range = (18, 70)
    education_levels = ["Bachelor's", "Master's", "PhD", "High School"]
    years_of_experience_range = (0, 50)

    new_rows = []

    # Create random combinations of attributes, excluding gender
    for _ in range(num_rows):
        base_age = randint(*age_range)
        base_education_level = choice(education_levels)
        base_job_title = choice(job_titles.job_titles)
        base_years_of_experience = randint(*years_of_experience_range)

        new_row = {
            'Age': base_age,
            'Education Level': base_education_level,
            'Job Title': base_job_title,
            'Years of Experience': base_years_of_experience
        }
        new_rows.append(new_row)

    # Convert dictionary to DataFrame
    new_data = pd.DataFrame(new_rows)

    # Save test data to CSV
    new_data.to_csv(paths.path_base_test_data, index=False)
    print(f'{num_rows} base test data rows generated.')


def add_gender_to_test_data():
    try:
        base_data = pd.read_csv(paths.path_base_test_data)
    except FileNotFoundError:
        print(f'{paths.path_base_test_data} does not exist.')
        return

    genders = ['Male', 'Female', 'Other']
    new_rows = []

    for _, row in base_data.iterrows():
        for gender in genders:
            new_row = row.to_dict()
            new_row['Gender'] = gender
            new_rows.append(new_row)

    # Convert list of dicts to DataFrame
    new_data = pd.DataFrame(new_rows)

    # Save test data with gender to CSV
    new_data.to_csv(paths.path_test_data, index=False)
    print(f'{len(new_data)} test data rows generated, including all genders.')
