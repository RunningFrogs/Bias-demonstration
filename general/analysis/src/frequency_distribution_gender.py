import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_graphic_frequency_distribution(input_path, result_path):
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        return

    df = pd.read_csv(input_path)

    # Dictionary for translation
    column_translations = {
        'Age': 'Alter',
        'Education Level': 'Bildungsabschluss',
        'Gender': 'Geschlecht',
        'Job Title': 'Berufsbezeichnung',
        'Salary': 'Gehalt in Rupien',
        'Years of Experience': 'Berufserfahrung in Jahren',
    }
    gender_translation = {'Female': 'weiblich', 'Male': 'männlich', 'Other': 'andere'}
    gender_order = ['männlich', 'weiblich', 'andere']
    colors = ['blue', 'orange', 'green']

    # Translate gender values
    df['Gender'] = df['Gender'].map(gender_translation)

    graphic_path = os.path.join(result_path, 'frequency_distribution', 'graphic')
    os.makedirs(graphic_path, exist_ok=True)

    for column in df.columns:
        plt.figure(figsize=(10, 6))

        if column in ['Salary', 'Years of Experience']:
            # Create boxplots for "Salary" and "Years of Experience"
            for i, gender in enumerate(gender_order):
                gender_df = df[df['Gender'] == gender]
                plt.boxplot(gender_df[column], positions=[i + 1], patch_artist=True,
                            boxprops=dict(facecolor=colors[i]),
                            medianprops=dict(color="black"))
            plt.xticks([1, 2, 3], gender_order)
            plt.xlabel('Geschlecht')
            plt.ylabel(column_translations[column])

        elif column == 'Education Level' or column == 'Age':
            # Create bar chart for "Education Level" and "Age"
            order = df[column].value_counts().index if column == 'Education Level' else sorted(df[column].unique())
            value_counts = df.groupby([column, 'Gender']).size().unstack(fill_value=0).reindex(order)
            value_counts.loc[:, gender_order].plot(kind='bar', stacked=True, color=colors)
            plt.xlabel(column_translations[column])
            plt.ylabel('Anzahl')

        else:
            continue

        plt.title(f'Verteilung nach {column_translations.get(column, column)}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.savefig(f'{result_path}frequency_distribution_gender/{column}')
        plt.close()
    print("Frequency Distribution for gender finished.")