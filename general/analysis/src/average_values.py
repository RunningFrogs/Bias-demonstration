import os
import pandas as pd

def generate_average_values(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} existiert nicht.')
        return

    data = pd.read_csv(input_path)

    # Define genders
    genders = ['Gesamt', 'Male', 'Female', 'Other']

    # Define columns on which average values are calculated
    columns = ['Age', 'Years of Experience', 'Salary']
    output = ""

    for column in columns:
        # Check if column exists in data
        if column in data.columns:
            output += f"{column}:\n"
            # Statistics for current category
            stats = data[column].agg(['mean', 'median', 'std', 'min', 'max'])
            output += (
                f"  Summary:\n"
                f"      Average: {stats['mean']:.2f}\n"
                f"      Median: {stats['median']:.2f}\n"
                f"      Standard deviation: {stats['std']:.2f}\n"
                f"      Range: from {stats['min']} to {stats['max']}\n"
            )

            # Gender-specific category
            for gender in genders[1:]:
                gender_data = data[data['Gender'] == gender]
                if not gender_data.empty:
                    stats = gender_data[column].agg(['mean', 'median', 'std', 'min', 'max'])
                    output += (
                        f"  {gender}:\n"
                        f"      Average: {stats['mean']:.2f}\n"
                        f"      Median: {stats['median']:.2f}\n"
                        f"      Standard deviation: {stats['std']:.2f}\n"
                        f"      Range: from {stats['min']} to {stats['max']}\n"
                    )
            output += "\n"

    print(output)

    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    # Save statistics
    os.makedirs(os.path.join(result_path, 'average_values'), exist_ok=True)
    filepath = os.path.join(result_path, 'average_values/average_values.txt')
    with open(filepath, 'w') as file:
        file.write(output)


def generate_average_salaries(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    data = pd.read_csv(input_path)
    genders = ['Male', 'Female', 'Other']

    # Check if required columns exist
    if 'Salary' not in data.columns or 'Job Title' not in data.columns or 'Gender' not in data.columns:
        print("Required columns 'Salary', 'Job Title', or 'Gender' missing.")
        return

    # Initialize dictionary for job statistics
    job_statistics = {}
    # Iterate over jobs
    for job in data['Job Title'].unique():
        job_data = data[data['Job Title'] == job]
        if not job_data.empty:
            avg_salary = job_data['Salary'].mean()
            median_salary = job_data['Salary'].median()
            gender_stats = {}
            # Calculate gender-specific salary statistics
            for gender in genders:
                gender_data = job_data[job_data['Gender'] == gender]
                if not gender_data.empty:
                    gender_avg_salary = gender_data['Salary'].mean()
                    gender_median_salary = gender_data['Salary'].median()
                    gender_stats[gender] = (gender_avg_salary, gender_median_salary)
            job_statistics[job] = (avg_salary, median_salary, gender_stats)

    # Sort jobs on average income
    sorted_job_statistics = dict(sorted(job_statistics.items(), key=lambda item: item[1][0], reverse=True))

    # Create output string
    output = "Average and median salaries by job (descending order of average salary), including gender breakdown:\n"
    for job, (avg_salary, median_salary, gender_stats) in sorted_job_statistics.items():
        output += f"  {job}:\n"
        output += f"      Average salary: {avg_salary:.2f}\n"
        output += f"      Median salary: {median_salary:.2f}\n"
        for gender, (g_avg_salary, g_median_salary) in gender_stats.items():
            output += (f"      {gender} Average: {g_avg_salary:.2f}\n"
                       f"      {gender} Median: {g_median_salary:.2f}\n")

    print(output)

    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    # Save data
    salaries_filepath = os.path.join(result_path, 'average_values/average_salaries.txt')
    os.makedirs(os.path.dirname(salaries_filepath), exist_ok=True)
    with open(salaries_filepath, 'w') as file:
        file.write(output)


def analyze_gender_pay_gap(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    data = pd.read_csv(input_path)
    # Check if all columns exist
    required_columns = ['Salary', 'Job Title', 'Gender']
    if not all(column in data.columns for column in required_columns):
        print("Required columns 'Salary', 'Job Title', or 'Gender' missing.")
        return

    # Initialize dictionary for pay gap
    job_gender_gaps = {}
    overall_gaps = {'Female': [], 'Other': []}

    # Iterate over all jobs to calculate pay gaps
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

    # Calculate pay gaps over all jobs
    overall_gap_averages = {gender: sum(gaps) / len(gaps) for gender, gaps in overall_gaps.items() if gaps}

    # Generate output
    output = "Gender pay gap analysis (percentage difference):\n"
    current_job = None
    for job_gender, gap_percentage in job_gender_gaps.items():
        job, gender = job_gender.rsplit(' ', 1)
        if job != current_job:
            if current_job is not None:
                output += "\n"
            current_job = job
        output += f"{job_gender}: {gap_percentage:.2f}%\n"

    output += "\nOverall average gender pay gap across all jobs:\n"
    for gender, average_gap in overall_gap_averages.items():
        output += f"{gender}: {average_gap:.2f}%\n"

    print(output)

    # Save data
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    gap_analysis_filepath = os.path.join(result_path, 'average_values/gender_pay_gap.txt')
    with open(gap_analysis_filepath, 'w') as file:
        file.write(output)