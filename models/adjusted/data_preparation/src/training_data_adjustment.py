import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config import paths
import logging

logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def balance_genders(df):
    # Identify unique genders present in the dataset.
    unique_genders = df['Gender'].unique()
    # Group the data by education level, job title, and years of experience to identify unique jobs.
    unique_jobs = df.groupby(['Education Level', 'Job Title', 'Years of Experience']).size().reset_index().drop(0, axis=1)

    # Function to generate synthetic data for underrepresented genders within specific job categories.
    def generate_synthetic_data(row, gender):
        synthetic_row = row.copy()
        synthetic_row['Gender'] = gender
        return synthetic_row

    balanced_df = pd.DataFrame()
    for _, job in unique_jobs.iterrows():
        # Create a mask to filter the dataframe for rows matching the current job's criteria.
        job_mask = (df['Education Level'] == job['Education Level']) & \
                   (df['Job Title'] == job['Job Title']) & \
                   (df['Years of Experience'] == job['Years of Experience'])

        # Apply the mask to obtain a dataframe of individuals with the same job title, education level, and years of experience.
        job_df = df[job_mask]
        # Determine the maximum gender representation for the current job to achieve balance.
        max_count = job_df['Gender'].value_counts().max()

        for gender in unique_genders:
            gender_df = job_df[job_df['Gender'] == gender]

            if gender_df.empty:
                # If a gender is not represented at all for a job, generate synthetic data for that gender.
                synthetic_data = generate_synthetic_data(job_df.iloc[0], gender)
                gender_df = pd.DataFrame([synthetic_data])

            # Resample the data to match the maximum count, allowing for replication if necessary.
            resampled_gender_df = gender_df.sample(n=max_count, replace=True, random_state=42).reset_index(drop=True)
            balanced_df = pd.concat([balanced_df, resampled_gender_df], axis=0)

    # Log the completion of the gender balancing process.
    logging.info('Dataset adjusted with synthetic data to ensure every gender is represented in each job equally.')
    return balanced_df.reset_index(drop=True)

def standardize_salaries(df):
    # Compute the median salary for each group defined by education level, job title, and years of experience.
    median_salary_mapping = df.groupby(['Education Level', 'Job Title', 'Years of Experience'])[
        'Salary'].median().reset_index(name='Fair Median Salary')

    # Merge this median salary information back into the original dataframe.
    df = pd.merge(df, median_salary_mapping, on=['Education Level', 'Job Title', 'Years of Experience'], how='left')

    # Adjust the salary to the computed fair median salary.
    df['Salary'] = df['Fair Median Salary']
    # Drop the now redundant column.
    df.drop(columns=['Fair Median Salary'], inplace=True)

    # Log the completion of the salary standardization process.
    logging.info('Salaries adjusted for fairness across genders.')
    return df

def prepare_training_data():
    # Check if the unprepared training data file exists, log and notify if it doesn't.
    if not os.path.exists(paths.path_unprepared_training_data):
        logging.error(f'Unprepared training data file {paths.path_unprepared_training_data} does not exist.')
        print(f'{paths.path_unprepared_training_data} does not exist.')
        return

    # Log the start of the training data preparation process.
    logging.info('Starting the advanced preparation of the training data.')

    # Load the unprepared training data.
    df = pd.read_csv(paths.path_unprepared_training_data)
    logging.info('Unprepared training data loaded successfully.')

    # Identify and log rows with missing data.
    missing_data_info = df[df.isnull().any(axis=1)]
    if not missing_data_info.empty:
        logging.info(f'Removing rows due to missing data. Rows affected: {len(missing_data_info)}')

    # Standardize education level strings for consistency.
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
    logging.info('Education level strings formatted.')

    # Remove rows with any missing values.
    df = df.dropna(how='any')

    # Convert numerical fields to integers and log the data cleaning process.
    df['Salary'] = df['Salary'].astype(int)
    df['Years of Experience'] = df['Years of Experience'].astype(int)
    df['Age'] = df['Age'].astype(int)
    logging.info('Numerical fields formatted and rows with missing values removed.')

    # Balance the dataset for gender representation across jobs.
    df = balance_genders(df)

    # Standardize salaries across different demographics.
    df = standardize_salaries(df)

    # Split the dataset into training and evaluation datasets.
    train_data, eval_data = train_test_split(df, test_size=0.2, random_state=42)
    logging.info('Data split into training and evaluation datasets.')

    # Save the prepared datasets to their respective paths.
    train_data.to_csv(paths.path_prepared_training_data_adjusted, index=False)
    eval_data.to_csv(paths.path_evaluation_data_adjusted, index=False)
    logging.info('Training and evaluation datasets saved.')

    # Notify the user of the locations where the datasets have been saved.
    print(f'Training data saved at {paths.path_prepared_training_data_adjusted}.')
    print(f'Evaluation data saved at {paths.path_evaluation_data_adjusted}.')
