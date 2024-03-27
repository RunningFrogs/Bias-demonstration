import os
import pandas as pd
from joblib import load
from config import paths

def prognose_interactive():
    if not os.path.exists(paths.path_model_no_gender):
        print(f'{paths.path_model_no_gender} does not exist.')
        return

    # Load model
    trained_model = load(paths.path_model_no_gender)

    # Query input data
    education_level = input("Education Level (High School, Bachelor's, Master's, PhD): ")
    job_title = input("Job Title: ")
    years_of_experience = float(input("Years of Experience: "))

    # Create a DataFrame from the input data
    input_data = pd.DataFrame({
        'Education Level': [education_level],
        'Job Title': [job_title],
        'Years of Experience': [years_of_experience]
    })

    # Predict on input data
    predicted_salary = trained_model.predict(input_data)

    # Print predicted income
    print(f'Predicted Income: ₹{predicted_salary[0]:,.0f}')