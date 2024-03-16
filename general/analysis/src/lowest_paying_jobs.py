import os
import pandas as pd
import logging
from config import paths

# Setup basic configuration for logging
logging.basicConfig(filename=paths.path_log_analysis, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_lowest_paying_jobs(input_path, result_path):
    logging.info('Starting analysis of lowest paying jobs.')

    if not os.path.exists(input_path):
        logging.error(f'{input_path} does not exist. Exiting function.')
        print(f'{input_path} does not exist.')
        return
    else:
        logging.info(f'Input path {input_path} found. Proceeding with data loading.')

    data = pd.read_csv(input_path)
    logging.info('Data loaded successfully.')

    if 'Salary' not in data.columns or 'Gender' not in data.columns or 'Job Title' not in data.columns:
        logging.error("Required columns 'Salary', 'Job Title', or 'Gender' missing. Exiting function.")
        print("Required columns 'Salary', 'Job Title', or 'Gender' missing.")
        return

    filtered_data = data[data['Gender'].isin(['Male', 'Female'])]
    logging.info('Filtered data to include only Male and Female genders.')

    median_salaries = filtered_data.groupby('Job Title')['Salary'].median().sort_values()
    logging.info('Calculated median salaries and sorted them.')

    lowest_paying_jobs = median_salaries.head(10).index
    logging.info('Identified the 10 lowest paying jobs.')

    lowest_paying_jobs_data = filtered_data[filtered_data['Job Title'].isin(lowest_paying_jobs)]
    logging.info('Filtered data for the 10 lowest paying jobs.')

    total_gender_distribution = lowest_paying_jobs_data['Gender'].value_counts(normalize=True) * 100
    logging.info('Calculated total gender distribution for the 10 lowest paying jobs.')

    output = "Gender distribution across the 10 lowest paying jobs (excluding 'Other'):\n\n"
    output += "Total Gender Distribution (Male & Female only):\n" + total_gender_distribution.to_string() + "\n\n"

    for job in lowest_paying_jobs:
        job_data = lowest_paying_jobs_data[lowest_paying_jobs_data['Job Title'] == job]
        gender_distribution = job_data['Gender'].value_counts(normalize=True) * 100
        output += f"Job: {job}\nGender Distribution (Male & Female only):\n{gender_distribution.to_string()}\n\n"
        logging.info(f'Processed gender distribution for {job}.')

    os.makedirs(result_path, exist_ok=True)
    logging.info(f'Result path {result_path} created or already exists.')

    result_file_path = os.path.join(result_path, 'lowest_paying_jobs/lowest_paying_jobs.txt')
    with open(result_file_path, 'w') as file:
        file.write(output)
        logging.info(f'Results written to {result_file_path}.')

    logging.info("Analysis of lowest paying jobs completed successfully.")
    print("Analysis completed and saved.")
