import os
import pandas as pd
import logging
from config import paths

# Konfiguration des Loggings
logging.basicConfig(filename=paths.path_log_analysis, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def generate_average_values(input_path, result_path):
    logging.info('Starting to generate average values.')
    if not os.path.exists(input_path):
        logging.error(f'{input_path} does not exist.')
        return

    data = pd.read_csv(input_path)
    genders = ['Gesamt', 'Male', 'Female', 'Other']
    columns = ['Age', 'Years of Experience', 'Salary']
    output = ""

    for column in columns:
        logging.info(f'Processing column: {column}')
        if column in data.columns:
            output += f"{column}:\n"
            stats = data[column].agg(['mean', 'median', 'std', 'min', 'max'])
            output += (
                f"  Summary:\n"
                f"      Average: {stats['mean']:.2f}\n"
                f"      Median: {stats['median']:.2f}\n"
                f"      Standard deviation: {stats['std']:.2f}\n"
                f"      Range: from {stats['min']} to {stats['max']}\n"
            )

            for gender in genders[1:]:
                gender_data = data[data['Gender'] == gender]
                if not gender_data.empty:
                    logging.info(f'Processing gender: {gender} for column: {column}')
                    stats = gender_data[column].agg(['mean', 'median', 'std', 'min', 'max'])
                    output += (
                        f"  {gender}:\n"
                        f"      Average: {stats['mean']:.2f}\n"
                        f"      Median: {stats['median']:.2f}\n"
                        f"      Standard deviation: {stats['std']:.2f}\n"
                        f"      Range: from {stats['min']} to {stats['max']}\n"
                    )
            output += "\n"

    logging.info('Finished generating average values.')
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    filepath = os.path.join(result_path, 'average_values/average_values.txt')
    with open(filepath, 'w') as file:
        file.write(output)
    logging.info(f'Average values saved to {filepath}.')


def generate_average_salaries(input_path, result_path):
    logging.info('Starting to generate average salaries.')
    if not os.path.exists(input_path):
        logging.error(f'{input_path} does not exist.')
        return

    data = pd.read_csv(input_path)
    genders = ['Male', 'Female', 'Other']

    if 'Salary' not in data.columns or 'Job Title' not in data.columns or 'Gender' not in data.columns:
        logging.error("Required columns 'Salary', 'Job Title', or 'Gender' missing.")
        return

    logging.info('Processing average salaries by job and gender.')
    job_statistics = {}
    for job in data['Job Title'].unique():
        job_data = data[data['Job Title'] == job]
        if not job_data.empty:
            avg_salary = job_data['Salary'].mean()
            median_salary = job_data['Salary'].median()
            gender_stats = {}
            for gender in genders:
                gender_data = job_data[job_data['Gender'] == gender]
                if not gender_data.empty:
                    gender_avg_salary = gender_data['Salary'].mean()
                    gender_median_salary = gender_data['Salary'].median()
                    gender_stats[gender] = (gender_avg_salary, gender_median_salary)
            job_statistics[job] = (avg_salary, median_salary, gender_stats)

    logging.info('Finished processing average salaries.')
    output = "Average and median salaries by job (descending order of average salary), including gender breakdown:\n"
    for job, (avg_salary, median_salary, gender_stats) in sorted(job_statistics.items(), key=lambda item: item[1][0],
                                                                 reverse=True):
        output += f"  {job}:\n"
        output += f"      Average salary: {avg_salary:.2f}\n"
        output += f"      Median salary: {median_salary:.2f}\n"
        for gender, (g_avg_salary, g_median_salary) in gender_stats.items():
            output += (f"      {gender} Average: {g_avg_salary:.2f}\n"
                       f"      {gender} Median: {g_median_salary:.2f}\n")

    logging.info('Saving average salaries data.')
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    salaries_filepath = os.path.join(result_path, 'average_values/average_salaries.txt')
    with open(salaries_filepath, 'w') as file:
        file.write(output)
    logging.info(f'Average salaries data saved to {salaries_filepath}.')


def analyze_gender_pay_gap(input_path, result_path):
    logging.info('Starting gender pay gap analysis.')
    if not os.path.exists(input_path):
        logging.error(f'{input_path} does not exist.')
        return

    data = pd.read_csv(input_path)
    if not all(column in data.columns for column in ['Salary', 'Job Title', 'Gender']):
        logging.error("Required columns 'Salary', 'Job Title', or 'Gender' missing.")
        return

    logging.info('Processing gender pay gaps by job.')
    job_gender_gaps = {}
    overall_gaps = {'Female': [], 'Other': []}

    for job in data['Job Title'].unique():
        job_data = data[data['Job Title'] == job]
        male_median_salary = job_data[job_data['Gender'] == 'Male']['Salary'].median()

        for gender in ['Female', 'Other']:
            gender_data = job_data[job_data['Gender'] == gender]
            if not gender_data.empty:
                gender_median_salary = gender_data['Salary'].median()
                if male_median_salary > 0:
                    gap_percentage = ((gender_median_salary - male_median_salary) / male_median_salary) * 100
                    job_gender_gaps[f"{job} {gender}"] = gap_percentage
                    overall_gaps[gender].append(gap_percentage)

    logging.info('Finished processing gender pay gaps.')
    output = "Gender pay gap analysis (percentage difference):\n"
    for job_gender, gap_percentage in job_gender_gaps.items():
        output += f"{job_gender}: {gap_percentage:.2f}%\n"

    logging.info('Saving gender pay gap analysis.')
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    gap_analysis_filepath = os.path.join(result_path, 'average_values/gender_pay_gap.txt')
    with open(gap_analysis_filepath, 'w') as file:
        file.write(output)
    logging.info(f'Gender pay gap analysis saved to {gap_analysis_filepath}.')
