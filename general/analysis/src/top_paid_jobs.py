import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
from config import paths

# Configure logging
logging.basicConfig(filename=paths.path_log_analysis, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_top_paid_jobs(input_path, result_path):
    logging.info('Starting to generate charts for top paid jobs.')

    # Check if the input file exists
    if not os.path.exists(input_path):
        logging.error(f'Input file {input_path} does not exist. Exiting function.')
        print(f'{input_path} does not exist.')
        return
    else:
        logging.info(f'Input file {input_path} found. Proceeding with data loading.')

    # Load the data from CSV file
    df = pd.read_csv(input_path)
    logging.info('Data loaded successfully.')

    # Translate gender labels in the 'Gender' column to German
    gender_translation = {'Female': 'weiblich', 'Male': 'männlich', 'Other': 'andere'}
    df['Gender'] = df['Gender'].map(gender_translation)
    logging.info('Translated gender labels to German.')

    # Filter job titles where more than 10 people are employed
    positions_count = df['Job Title'].value_counts()
    positions_more_than_10 = positions_count[positions_count > 10].index
    df_filtered = df[df['Job Title'].isin(positions_more_than_10)]
    logging.info('Filtered job titles where more than 10 people are employed.')

    # Check if df_filtered is empty
    if df_filtered.empty:
        logging.warning(f"No data found for job title with more than 10 employees. Exiting function.")
        print(f"No data found for job title with more than 10 employees.")
        return

    # Calculate the average salary for each job title and select the top 10
    average_salary_by_position = df_filtered.groupby('Job Title')['Salary'].mean()
    top_10_positions = average_salary_by_position.nlargest(10).index
    logging.info('Identified top 10 highest-paid job titles.')

    # Filter the DataFrame for the top 10 highest-paid job titles
    df_top_positions = df_filtered[df_filtered['Job Title'].isin(top_10_positions)]

    # Count and calculate the percentage distribution of genders in these positions
    gender_distribution = df_top_positions.groupby(['Job Title', 'Gender']).size().unstack(fill_value=0)
    gender_distribution = gender_distribution.reindex(['männlich', 'weiblich', 'andere'], axis=1, fill_value=0)
    gender_distribution_percentage = gender_distribution.div(gender_distribution.sum(axis=1), axis=0) * 100
    logging.info('Calculated gender distribution in the top 10 highest-paid job titles.')

    # Create heatmaps for the gender distribution
    plt.figure(figsize=(10, 8))
    sns.heatmap(gender_distribution_percentage, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Prozent'})
    plt.title('Verteilung der Geschlechter in den 10 bestbezahltesten Positionen')
    plt.xlabel('Geschlecht')
    plt.ylabel('Position')
    plt.tight_layout()
    plt.savefig(f'{result_path}top_paid_jobs/top_paid_jobs_percent.png')
    logging.info('Generated heatmap for percentage gender distribution.')

    plt.figure(figsize=(10, 8))
    sns.heatmap(gender_distribution, annot=True, fmt="d", cmap="YlOrRd", cbar_kws={'label': 'Anzahl'})
    plt.title('Absolute Verteilung der Geschlechter in den 10 bestbezahltesten Positionen')
    plt.xlabel('Geschlecht')
    plt.ylabel('Position')
    plt.tight_layout()
    plt.savefig(f'{result_path}top_paid_jobs/top_paid_jobs_absolute.png')
    logging.info('Generated heatmap for absolute gender distribution.')

    logging.info('Completed generating charts for top paid jobs.')
    print("Analysis completed and saved.")
