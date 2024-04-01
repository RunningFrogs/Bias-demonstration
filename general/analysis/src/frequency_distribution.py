import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_graphic_frequency_distribution(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    df = pd.read_csv(input_path)

    # Dictionary for translating column names and 'Gender' values to German
    column_translations = {
        'Age': 'Alter',
        'Education Level': 'Bildungsabschluss',
        'Gender': 'Geschlecht',
        'Job Title': 'Berufsbezeichnung',
        'Salary': 'Gehalt in Rupien',
        'Years of Experience': 'Berufserfahrung in Jahren',
    }
    gender_translation = {'Female': 'weiblich', 'Male': 'männlich', 'Other': 'andere'}

    # Translate 'Gender' values to German
    df['Gender'] = df['Gender'].map(gender_translation)

    # Check if "Salary" exists, otherwise remove it from translation
    if 'Salary' not in df.columns:
        column_translations.pop('Salary', None)

    # Create and save graphical frequency distribution diagrams for each column
    saved_files = []
    for column in df.columns:
        plt.figure(figsize=(10, 6))
        if df[column].dtype == 'object':
            # For categorical columns - create a bar chart showing the percentage distribution
            value_counts = df[column].value_counts(normalize=True) * 100
            value_counts.plot(kind='bar', color='blue', alpha=0.7)
        else:
            # For numerical columns - create a histogram showing the percentage distribution
            weights = (np.ones_like(df[column]) / len(df[column])) * 100
            df[column].plot(kind='hist', bins=30, alpha=0.7, edgecolor='black', color='blue', weights=weights)

        # Use translated title if available, else use the original column name
        title = column_translations.get(column, column)
        plt.title(f'Verteilung nach {title}')
        plt.xticks(rotation=45, ha='right')  # Rotate labels to prevent overlapping
        plt.ylabel('Prozent')
        xlabel = column_translations.get(column, column)
        plt.xlabel(xlabel)
        plt.tight_layout()

        # Save the diagram as a PNG
        file_name = f'{result_path}frequency_distribution/graphic/{column}_distribution.png'
        plt.savefig(file_name)
        saved_files.append(file_name)
        plt.close()

        print("Graphic Frequency Distribution finished.")


def generate_text_frequency_distribution(input_path, result_path):
    df = pd.read_csv(input_path)

    # Remove empty rows
    df = df.dropna(how='all')

    # Check if "Salary" exists, otherwise remove it from calculation
    if 'Salary' not in df.columns:
        df = df.drop(columns=['Salary'], errors='ignore')  # Remove 'Salary', if it exists

    # Create a directory for the results if it does not exist
    output_dir = f'{result_path}/frequency_distribution/text/'
    os.makedirs(output_dir, exist_ok=True)

    # Function to calculate the gender distribution
    def calculate_gender_distribution(sub_df, group_column):
        # Calculate the count and percentage of each gender in the subset
        gender_counts = sub_df.groupby(group_column)['Gender'].value_counts(normalize=True).unstack(fill_value=0)
        gender_percentages = gender_counts * 100
        return gender_percentages

    # Create and save text files with frequency distribution for each column
    for column in df.columns:
        # Calculate unique values and their absolute frequency
        value_counts = df[column].value_counts(dropna=True)
        txt_file_path = f'{output_dir}/{column}_distribution.txt'
        with open(txt_file_path, 'w') as file:
            file.write(f'Value distribution for {column}:\n\n')
            for value, count in value_counts.items():
                file.write(f'{value}: {count} ({count / len(df) * 100:.2f}%)\n')
                if df[column].dtype == 'object' and column != 'Gender':
                    sub_df = df[df[column] == value]
                    gender_distribution = calculate_gender_distribution(sub_df, column)
                    for gender, percentage in gender_distribution.loc[value].items():
                        file.write(f'  {gender}: {percentage:.2f}%\n')
            file.write('\n')

    print("Text Frequency Distribution finished.")
