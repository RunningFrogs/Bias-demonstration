import argparse

from general.analysis.src import frequency_distribution, lowest_paying_jobs, average_values, top_paid_jobs, \
    frequency_distribution_gender, heatmaps, salary_distribution
from config import paths


def analyze_default(input_path, result_path):
    average_values.generate_average_values(input_path, result_path)
    average_values.generate_average_salaries(input_path, result_path)
    average_values.analyze_gender_pay_gap(input_path, result_path)
    salary_distribution.analyze_salary_distribution(input_path, result_path)
    frequency_distribution.generate_text_frequency_distribution(input_path, result_path)
    frequency_distribution.generate_graphic_frequency_distribution(input_path, result_path)
    frequency_distribution_gender.generate_graphic_frequency_distribution(input_path, result_path)


def analyze_data(args):
    if args.training:
        input_path = paths.path_prepared_training_data_original
        result_path = paths.path_analysis_result_training_data_original
        heatmaps.generate_heatmaps(input_path, result_path)
        top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
        lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)
        analyze_default(input_path, result_path)

    elif args.test:
        input_path = paths.path_test_data_expanded
        result_path = paths.path_analysis_result_test_data_original
        analyze_default(input_path, result_path)

    elif args.prognosis:
        if args.original:
            input_path = paths.path_prognosed_data_original
            result_path = paths.path_analysis_result_prognosed_data_original
            heatmaps.generate_heatmaps(input_path, result_path)
            top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
            lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)
            analyze_default(input_path, result_path)

    else:
        raise Exception("Invalid analyze arguments")


parser = argparse.ArgumentParser(description="Script to call specific functions based on arguments")

# Analyze arguments
parser.add_argument('--analyze', action='store_true', help='Analyze flag')
parser.add_argument('--training', action='store_true', help='Training data flag')
parser.add_argument('--test', action='store_true', help='Test data flag')
parser.add_argument('--prognosis', action='store_true', help='Prognosis data flag')
parser.add_argument('--original', action='store_true', help='Original prognosis data flag')
parser.add_argument('--ethical', action='store_true', help='Original prognosis data flag')

# Parse the arguments
args = parser.parse_args()

if args.analyze:
    analyze_data(args)
