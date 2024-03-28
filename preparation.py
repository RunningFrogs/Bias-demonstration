import argparse
from general.datasets.src import test_data_generation, training_data_preparation


def call_generate_data(num_rows):
    test_data_generation.generate_basic_test_data(num_rows)
    test_data_generation.expand_test_datas()
    test_data_generation.remove_gender_age_and_age()

def call_prepare_training_data():
    training_data_preparation.prepare_training_data_basic()


# Initialize the parser
parser = argparse.ArgumentParser(description="Call specific functions based on arguments")

# Prepare data argument
parser.add_argument('--generate', type=int, help='Generate test data')
parser.add_argument('--prepare', action='store_true', help='Prepare training data')


# Parse the arguments
args = parser.parse_args()

if args.generate:
    call_generate_data(args.generate)

if args.prepare:
    call_prepare_training_data()
