import argparse
from config import paths
from general.analysis.src import frequency_distribution, lowest_paying_jobs, average_values, top_paid_jobs, \
    frequency_distribution_gender, heatmaps, salary_distribution


def analyze_default(input_path, result_path):
    average_values.generate_average_values(input_path, result_path)
    average_values.generate_average_salaries(input_path, result_path)
    average_values.analyze_gender_pay_gap(input_path, result_path)
    salary_distribution.analyze_salary_distribution(input_path, result_path)
    frequency_distribution.generate_text_frequency_distribution(input_path, result_path)
    frequency_distribution.generate_graphic_frequency_distribution(input_path, result_path)
    frequency_distribution_gender.generate_graphic_frequency_distribution(input_path, result_path)

def analyze_training(args):
    if args.original:
        input_path = paths.path_prepared_training_data_original
        result_path = paths.path_analysis_result_training_data_original
        heatmaps.generate_heatmaps(input_path, result_path)
        top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
        lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)
        analyze_default(input_path, result_path)

    elif args.adjusted:
        input_path = paths.path_prepared_training_data_adjusted
        result_path = paths.path_analysis_result_training_data_adjusted
        heatmaps.generate_heatmaps(input_path, result_path)
        top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
        lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)
        analyze_default(input_path, result_path)

    else:
        raise Exception("Invalid analyze arguments")

def analyze_test(args):
    input_path = paths.path_test_data_expanded
    result_path = paths.path_analysis_result_test_data_original
    analyze_default(input_path, result_path)

def analyze_prognosis(args):
    if args.original:
        input_path = paths.path_prognosed_data_original
        result_path = paths.path_analysis_result_prognosed_data_original
        heatmaps.generate_heatmaps(input_path, result_path)
        top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
        lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)
        analyze_default(input_path, result_path)

    elif args.adjusted:
        input_path = paths.path_prognosed_data_adjusted
        result_path = paths.path_analysis_result_prognosed_data_adjusted
        heatmaps.generate_heatmaps(input_path, result_path)
        top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
        lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)
        analyze_default(input_path, result_path)

    else:
        raise Exception("Invalid analyze arguments")


parser = argparse.ArgumentParser(description="Call specific functions based on arguments")

# Analyze argument
parser.add_argument('--training', action='store_true', help='Training data')
parser.add_argument('--adjusted', action='store_true', help='Adjusted model')
parser.add_argument('--test', action='store_true', help='Test data')
parser.add_argument('--prognosis', action='store_true', help='Prognosis data')
parser.add_argument('--original', action='store_true', help='Original model')

# Parse the arguments
args = parser.parse_args()

if args.training:
    analyze_training(args)

if args.test:
    analyze_test(args)

if args.prognosis:
    analyze_prognosis(args)
