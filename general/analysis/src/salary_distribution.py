import os
import pandas as pd

def analyze_salary_distribution(input_path, result_path):
    # Check if the input file exists
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    # Load the dataset
    data = pd.read_csv(input_path)

    # Check for required columns
    if 'Salary' not in data.columns or 'Gender' not in data.columns or 'Job Title' not in data.columns:
        print("Required columns 'Salary', 'Job Title', or 'Gender' missing.")
        return

    # Filter data for 'Male' and 'Female'
    filtered_data = data[data['Gender'].isin(['Male', 'Female'])]

    # Calculate overall median salary
    overall_median = filtered_data['Salary'].median()

    # Analyze lower decile
    lower_decile_threshold = filtered_data['Salary'].quantile(0.1)
    lower_decile_data = filtered_data[filtered_data['Salary'] <= lower_decile_threshold]

    # Calculate gender distribution for different salary ranges
    total_count = len(filtered_data)
    lower_decile_gender_distribution = lower_decile_data['Gender'].value_counts(normalize=False)
    lower_decile_gender_distribution_percentage = (lower_decile_gender_distribution / total_count) * 100

    above_median_data = filtered_data[filtered_data['Salary'] > overall_median]
    below_median_data = filtered_data[filtered_data['Salary'] <= overall_median]
    above_median_gender_distribution_percentage = (above_median_data['Gender'].value_counts(
        normalize=False) / total_count) * 100
    below_median_gender_distribution_percentage = (below_median_data['Gender'].value_counts(
        normalize=False) / total_count) * 100

    # Prepare the output
    median_info = f"Overall median salary (excluding 'Other'): {overall_median}\n\n"
    below_median_info = "Gender distribution below or equal to median salary (% of total, excluding 'Other'):\n" + below_median_gender_distribution_percentage.to_string() + "\n\n"
    above_median_info = "Gender distribution above median salary (% of total, excluding 'Other'):\n" + above_median_gender_distribution_percentage.to_string() + "\n\n"
    lower_decile_info = "Gender distribution in the lowest 10% of salaries (% of total, excluding 'Other'):\n" + lower_decile_gender_distribution_percentage.to_string() + "\n"

    output = median_info + below_median_info + above_median_info + lower_decile_info

    # Ensure the result path exists
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    result_file_path = os.path.join(result_path, 'salary_distribution/salary_distribution.txt')
    with open(result_file_path, 'w') as file:
        file.write(output)

    print("Salary Distribution analysis completed and saved.")
