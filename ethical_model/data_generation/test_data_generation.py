import os
import pandas as pd
from random import choice, randint, seed
from time import time
from config import paths
from data_generation import job_titles

#TODO: rename file
#TODO: add file/script for generation of ethical test data or change this script
def generate_test_data(num_rows):
    if not os.path.exists(paths.path_prepared_training_data):
        print(f'{paths.path_prepared_training_data} does not exist.')
        return

    seed(time())

    # Define test data range
    age_range = (18, 70)
    genders = ['Male', 'Female', 'Other']
    education_levels = ["Bachelor's", "Master's", "PhD", "High School"]
    years_of_experience_range = (0, 50)

    new_rows = []

    # Create random combinations of attributes
    for _ in range(num_rows):
        base_age = randint(*age_range)
        base_education_level = choice(education_levels)
        base_job_title = choice(job_titles.job_titles)
        base_years_of_experience = randint(*years_of_experience_range)

        # Create dataset for every gender
        for gender in genders:
            new_row = {
                'Age': base_age,
                'Gender': gender,
                'Education Level': base_education_level,
                'Job Title': base_job_title,
                'Years of Experience': base_years_of_experience
            }
            new_rows.append(new_row)

    # Convert dictionary to DataFrame
    new_data = pd.DataFrame(new_rows)

    # Save test data to CSV
    new_data.to_csv(paths.path_test_data, index=False)
    print(f'{3 * num_rows} test data generated, including all genders.')
