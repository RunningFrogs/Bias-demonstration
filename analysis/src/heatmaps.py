import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_heatmaps(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    # Load the data from the specified CSV file
    file_path = f'{input_path}'
    data = pd.read_csv(file_path)

    # Dictionary for translating 'Gender' values to German
    gender_translation = {'Female': 'weiblich', 'Male': 'männlich', 'Other': 'andere'}

    # Translate 'Gender' values to German
    data['Gender'] = data['Gender'].map(gender_translation)

    # Group the data by 'Education Level' and 'Gender'
    grouped_data = data.groupby(['Education Level', 'Gender'])

    # Calculate the median salary across all individuals
    median_salary = data['Salary'].median()

    # Create a heatmap for the percentage of individuals earning above the median salary
    # Grouped by 'Education Level' and 'Gender'
    percentage = grouped_data['Salary'].apply(lambda x: (x > median_salary).mean()).unstack()
    # Ensure columns are in the desired order: 'männlich', 'weiblich', 'andere'
    percentage = percentage[['männlich', 'weiblich', 'andere']]
    plt.figure(figsize=(8, 6))
    heatmap_percentage = sns.heatmap(percentage, annot=True, cmap='coolwarm', fmt=".2f")
    heatmap_percentage.set_title('Anteil der Personen, welche überdurchschnittlich verdienen\n'
                                 'nach Bildungsabschluss und Geschlecht')
    heatmap_percentage.set_xlabel('Geschlecht')
    heatmap_percentage.set_ylabel('Bildungsabschluss')
    plt.tight_layout()
    plt.savefig(f'{result_path}/heatmaps/percentage_above_median.png')

    # Create a heatmap for the average incomes of each combination of 'Education Level' and 'Gender'
    # Adjusted to display the median incomes
    median_income = grouped_data['Salary'].median().unstack()
    # Ensure columns are in the desired order: 'männlich', 'weiblich', 'andere'
    median_income = median_income[['männlich', 'weiblich', 'andere']]
    plt.figure(figsize=(8, 6))
    heatmap_median_income = sns.heatmap(median_income, annot=True, cmap='coolwarm', fmt=".2f")
    heatmap_median_income.set_title('Median-Einkommen nach Bildungsabschluss und Geschlecht in Rupien')
    heatmap_median_income.set_xlabel('Geschlecht')
    heatmap_median_income.set_ylabel('Bildungsabschluss')
    plt.tight_layout()
    plt.savefig(f'{result_path}/heatmaps/median_income.png')

