import argparse

from general.datasets.src import test_data_generation

# TODO: Add comments and logging

def call_generate_data(num_rows):
    test_data_generation.generate_basic_test_data(num_rows)
    test_data_generation.expand_test_datas()



# Initialize the parser
parser = argparse.ArgumentParser(description="Script to call specific functions based on arguments")

# Prepare data argument
parser.add_argument('--generate', type=int, help='Generate test data')


# Parse the arguments
args = parser.parse_args()

if args.generate:
    call_generate_data(args.generate)
