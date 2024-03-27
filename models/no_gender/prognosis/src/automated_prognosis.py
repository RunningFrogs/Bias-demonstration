import os
import pandas as pd
from joblib import load
from config import paths

def prognose_automated():
    if not os.path.exists(paths.path_test_data_without_gender):
        print(f'{paths.path_test_data_without_gender} does not exist.')
        return

    if not os.path.exists(paths.path_model_no_gender):
        print(f'{paths.path_model_no_gender} does not exist.')
        return

    # Load model
    trained_model = load(paths.path_model_no_gender)

    # Load input data from CSV
    input_data = pd.read_csv(paths.path_test_data_without_gender)

    # Predict on input data
    predicted_salaries = trained_model.predict(input_data)

    # Add the predictions to the test_data DataFrame
    input_data['Salary'] = predicted_salaries

    # Save the DataFrame with the predictions to a new CSV file
    input_data.to_csv(paths.path_prognosed_data_no_gender, index=False)
    print(f'Predictions saved at {paths.path_prognosed_data_no_gender}.')
