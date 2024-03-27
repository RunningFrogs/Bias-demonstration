import os
import pandas as pd

def analyze_lowest_paying_jobs(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    # Load the data from the CSV file
    data = pd.read_csv(input_path)

    # Ensure the required columns are present in the data
    if 'Salary' not in data.columns or 'Gender' not in data.columns or 'Job Title' not in data.columns:
        print("Required columns 'Salary', 'Job Title', or 'Gender' missing.")
        return

    # Filter data to include only Male and Female gender entries
    filtered_data = data[data['Gender'].isin(['Male', 'Female'])]

    # Calculate the median salary for each job title and sort them
    median_salaries = filtered_data.groupby('Job Title')['Salary'].median().sort_values()

    # Identify the 10 lowest paying jobs
    lowest_paying_jobs = median_salaries.head(10).index

    # Extract data for the 10 lowest paying jobs
    lowest_paying_jobs_data = filtered_data[filtered_data['Job Title'].isin(lowest_paying_jobs)]

    # Calculate the gender distribution across the lowest paying jobs
    total_gender_distribution = lowest_paying_jobs_data['Gender'].value_counts(normalize=True) * 100

    output = "Gender distribution across the 10 lowest paying jobs (excluding 'Other'):\n\n"
    output += "Total Gender Distribution (Male & Female only):\n" + total_gender_distribution.to_string() + "\n\n"

    # Loop through each of the lowest paying jobs to calculate and add their gender distribution to the output
    for job in lowest_paying_jobs:
        job_data = lowest_paying_jobs_data[lowest_paying_jobs_data['Job Title'] == job]
        gender_distribution = job_data['Gender'].value_counts(normalize=True) * 100
        output += f"Job: {job}\nGender Distribution (Male & Female only):\n{gender_distribution.to_string()}\n\n"

    # Ensure the result directory exists; create it if it does not
    os.makedirs(result_path, exist_ok=True)

    result_file_path = os.path.join(result_path, 'lowest_paying_jobs/lowest_paying_jobs.txt')
    with open(result_file_path, 'w') as file:
        file.write(output)

    print("Lowest Paying Jobs analysis completed and saved.")
