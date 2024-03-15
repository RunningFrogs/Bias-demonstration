import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def generate_top_paid_jobs(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    # Load the data from CSV file
    df = pd.read_csv(input_path)

    # Dictionary for translating gender labels to German
    gender_translation = {'Female': 'weiblich', 'Male': 'männlich', 'Other': 'andere'}

    # Translate gender labels in the 'Gender' column to German
    df['Gender'] = df['Gender'].map(gender_translation)

    # Filter job titles where more than 10 people are employed
    positions_count = df['Job Title'].value_counts()
    positions_more_than_10 = positions_count[positions_count > 10].index

    # Filter the DataFrame to include only job titles with more than 10 employees
    df_filtered = df[df['Job Title'].isin(positions_more_than_10)]

    # Check if df_filtered is empty
    if df_filtered.empty:
        print(f"No data found for job title with more than 10 employees.")
        return

    # Calculate the average salary for each job title
    average_salary_by_position = df_filtered.groupby('Job Title')['Salary'].mean()

    # Select the top 10 highest-paid job titles
    top_10_positions = average_salary_by_position.nlargest(10).index

    # Filter the DataFrame to include only the top 10 highest-paid job titles
    df_top_positions = df_filtered[df_filtered['Job Title'].isin(top_10_positions)]

    # Count the number of males and females in these positions
    gender_distribution = df_top_positions.groupby(['Job Title', 'Gender']).size().unstack(fill_value=0)

    # Ensure the order of genders is correct: 'male', 'female', 'other'
    desired_order = ['männlich', 'weiblich', 'andere']
    gender_distribution = gender_distribution.reindex(desired_order, axis=1, fill_value=0)

    # Calculate the percentage distribution of genders
    gender_distribution_percentage = gender_distribution.div(gender_distribution.sum(axis=1), axis=0) * 100

    # Create a heatmap for the percentage gender distribution
    plt.figure(figsize=(10, 8))
    sns.heatmap(gender_distribution_percentage, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Prozent'})
    plt.title('Verteilung der Geschlechter in den 10 bestbezahltesten Positionen')
    plt.xlabel('Geschlecht')
    plt.ylabel('Position')
    plt.tight_layout()  # Prevents cutting off labels
    plt.savefig(f'{result_path}top_paid_jobs/top_paid_jobs_percent.png')

    # Create a heatmap for the absolute gender distribution
    plt.figure(figsize=(10, 8))
    sns.heatmap(gender_distribution, annot=True, fmt="d", cmap="YlOrRd", cbar_kws={'label': 'Anzahl'})
    plt.title('Absolute Verteilung der Geschlechter in den 10 bestbezahltesten Positionen')
    plt.xlabel('Geschlecht')
    plt.ylabel('Position')
    plt.tight_layout()  # Prevents cutting off labels
    plt.savefig(f'{result_path}top_paid_jobs/top_paid_jobs_absolute.png')
