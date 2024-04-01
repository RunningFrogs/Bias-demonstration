import pandas as pd
from joblib import load
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from config import paths

def evaluate_model():
    # Load model
    model = load(paths.path_model_no_gender)

    # Load evaluation data
    data = pd.read_csv(paths.path_evaluation_data_no_gender)
    X_test = data.drop(columns=['Salary'])
    y_true = data['Salary']

    # Predict salaries
    y_pred = model.predict(X_test)

    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    average_salary = y_true.mean()
    rmse_ratio = rmse / average_salary

    # Print metrics
    print(f"R2: {r2}")
    print(f"RMSE: {rmse}")
    print(f"RMSE in relation to average income: {rmse_ratio}")

    # Save metrics in text file
    with open(paths.path_evaluation_metrics_no_gender, 'w') as file:
        file.write(f"R2: {r2}\n")
        file.write(f"RMSE: {rmse}\n")
        file.write(f"RMSE in relation to average income: {rmse_ratio}\n")
