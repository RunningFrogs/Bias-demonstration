import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config import paths
import logging

logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def balance_genders(df):
    # Identify unique genders and job categories
    unique_genders = df['Gender'].unique()
    unique_jobs = df.groupby(['Education Level', 'Job Title', 'Years of Experience']).size().reset_index().drop(0, axis=1)

    logging.info(f'Unique genders identified: {unique_genders}. Starting gender balancing for each job category.')

    def generate_synthetic_data(row, gender):
        synthetic_row = row.copy()
        synthetic_row['Gender'] = gender
        return synthetic_row

    balanced_df = pd.DataFrame()
    for _, job in unique_jobs.iterrows():
        # Create a mask to filter the DataFrame for the current job category
        job_mask = (df['Education Level'] == job['Education Level']) & \
                   (df['Job Title'] == job['Job Title']) & \
                   (df['Years of Experience'] == job['Years of Experience'])
        job_df = df[job_mask]

        if job_df.empty:
            logging.warning(f'No entries found for job category: {job.to_dict()}')

        max_count = job_df['Gender'].value_counts().max()

        for gender in unique_genders:
            gender_df = job_df[job_df['Gender'] == gender]

            # If no entries for gender, generate synthetic data
            if gender_df.empty:
                logging.info(
                    f'No entries for gender "{gender}" in job category: {job.to_dict()}. Generating synthetic data.')
                synthetic_data = generate_synthetic_data(job_df.iloc[0], gender)
                gender_df = pd.DataFrame([synthetic_data])

            # Resample to match the max gender count, allowing for duplication
            resampled_gender_df = gender_df.sample(n=max_count, replace=True, random_state=42).reset_index(drop=True)
            balanced_df = pd.concat([balanced_df, resampled_gender_df], axis=0)

    logging.info('Gender balancing complete. Dataset is now balanced across genders for each job category.')
    return balanced_df.reset_index(drop=True)

def standardize_salaries(df):
    logging.info('Standardizing salaries across the dataset.')
    # Calculate the median salary for each job category
    median_salary_mapping = df.groupby(['Education Level', 'Job Title', 'Years of Experience'])['Salary'].median().reset_index(name='Fair Median Salary')
    # Merge the median salaries back into the original dataframe
    df = pd.merge(df, median_salary_mapping, on=['Education Level', 'Job Title', 'Years of Experience'], how='left')
    # Replace original salaries with the standardized ones
    df['Salary'] = df['Fair Median Salary']
    df.drop(columns=['Fair Median Salary'], inplace=True)
    logging.info('Salaries standardized based on median for each job category.')
    return df

def prepare_training_data():
    logging.info('Checking for unprepared training data.')
    # Check if file exists
    if not os.path.exists(paths.path_unprepared_training_data):
        logging.error(f'Unprepared training data file {paths.path_unprepared_training_data} does not exist.')
        print(f'{paths.path_unprepared_training_data} does not exist.')
        return

    logging.info('Starting the advanced preparation of the training data.')

    df = pd.read_csv(paths.path_unprepared_training_data)
    logging.info('Unprepared training data loaded successfully.')

    logging.info('Cleaning and formatting data.')
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

    # Remove rows with any missing values
    df = df.dropna(how='any')

    # Convert numerical fields to integers
    df['Salary'] = df['Salary'].astype(int)
    df['Years of Experience'] = df['Years of Experience'].astype(int)
    df['Age'] = df['Age'].astype(int)




    # Balance genders and salary
    df = balance_genders(df)
    df = standardize_salaries(df)

    # Split the data
    logging.info('Splitting data into training and evaluation datasets.')
    train_data, eval_data = train_test_split(df, test_size=0.2, random_state=42)
    logging.info('Data split into training and evaluation datasets.')

    # Save evaluation data
    logging.info('Saving evaluation dataset.')
    eval_data.to_csv(paths.path_evaluation_data_adjusted, index=False)
    logging.info('Evaluation dataset saved.')

    # Save training data
    logging.info('Saving prepared training data.')
    train_data.to_csv(paths.path_prepared_training_data_adjusted, index=False)
    logging.info('Training data prepared, balanced, and saved.')

    print(f'Training data saved at {paths.path_prepared_training_data_adjusted}.')
    print(f'Evaluation data saved at {paths.path_evaluation_data_adjusted}.')