import argparse

from models.original.prognosis.src import interactive_prognosis, model_training, model_evaluation, \
    automated_prognosis
from models.original.analysis.src import average_values, frequency_distribution, heatmaps, top_paid_jobs, \
                                         frequency_distribution_gender, salary_distribution, lowest_paying_jobs
from config import paths

# TODO: Abhängigkeiten ausarbeiten, dass Parameter nur in bestimmten Kombinationen funktionieren
# TODO: Paths in zentrale Datei außerhalb der Modelle verwalten?

def train_model():
    model_training.train_model()


def evaluate_model():
    model_evaluation.evaluate_model()


def analyze_data(args):
    if args.training:
        input_path = paths.path_prepared_training_data_original
        result_path = paths.path_analysis_result_training_data_original
        heatmaps.generate_heatmaps(input_path, result_path)
        top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
        lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)

    elif args.test:
        input_path = paths.path_test_data_expanded
        result_path = paths.path_analysis_result_test_data_original

    elif args.prognosis:
        input_path = paths.path_prognosed_data_original
        result_path = paths.path_analysis_result_prognosed_data_original
        heatmaps.generate_heatmaps(input_path, result_path)
        top_paid_jobs.generate_top_paid_jobs(input_path, result_path)
        lowest_paying_jobs.analyze_lowest_paying_jobs(input_path, result_path)

    else:
        raise Exception("Invalid analyze arguments")

    average_values.generate_average_values(input_path, result_path)
    average_values.generate_average_salaries(input_path, result_path)
    average_values.analyze_gender_pay_gap(input_path, result_path)
    salary_distribution.analyze_salary_distribution(input_path, result_path)
    frequency_distribution.generate_text_frequency_distribution(input_path, result_path)
    frequency_distribution.generate_graphic_frequency_distribution(input_path, result_path)
    frequency_distribution_gender.generate_graphic_frequency_distribution(input_path, result_path)


def prognose(args):
    if args.interactive:
        interactive_prognosis.prognose_interactive()

    elif args.automated:
        automated_prognosis.prognose_automated()

    else:
        raise Exception("Invalid prognose arguments")


# Initialize the parser
parser = argparse.ArgumentParser(description="Script to call specific functions based on arguments")

# Prepare data argument
parser.add_argument('--prepare', action='store_true', help='Prepare flag')

# Analyze arguments
parser.add_argument('--analyze', action='store_true', help='Analyze flag')
parser.add_argument('--training', action='store_true', help='Training data flag')
parser.add_argument('--test', action='store_true', help='Test data flag')
parser.add_argument('--prognosis', action='store_true', help='Prognosis data flag')

# Train model arguments
parser.add_argument('--train', action='store_true', help='Train model flag')
parser.add_argument('--evaluate', action='store_true', help='Evaluation flag')

# Prognosis arguments
parser.add_argument('--prognose', action='store_true', help='Prognose flag')
parser.add_argument('--interactive', action='store_true', help='Interactive flag')
parser.add_argument('--automated', action='store_true', help='Automated data flag')

# Create test data argument
parser.add_argument('--generate', type=int, help='Automated data flag')

# Parse the arguments
args = parser.parse_args()

if args.prepare:
    call_prepare_data()

if args.train:
    train_model()

if args.analyze:
    analyze_data(args)

if args.prognose:
    prognose(args)

if args.evaluate:
    evaluate_model()
