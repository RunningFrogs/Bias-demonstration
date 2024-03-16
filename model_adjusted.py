import argparse

from models.adjusted.prognosis.src import interactive_prognosis, model_training, model_evaluation, \
    automated_prognosis
from models.adjusted.data_preparation.src import ethical_training_data_preparation

def train_model():
    model_training.train_model()


def evaluate_model():
    model_evaluation.evaluate_model()


def prognose(args):
    if args.interactive:
        interactive_prognosis.prognose_interactive()

    elif args.automated:
        automated_prognosis.prognose_automated()

    else:
        raise Exception("Invalid prognose arguments")


def call_prepare_training_data():
    ethical_training_data_preparation.prepare_etical_data()


# Initialize the parser
parser = argparse.ArgumentParser(description="Script to call specific functions based on arguments")

# Train model arguments
parser.add_argument('--train', action='store_true', help='Train model flag')
parser.add_argument('--evaluate', action='store_true', help='Evaluation flag')

# Prognosis arguments
parser.add_argument('--prognose', action='store_true', help='Prognose flag')
parser.add_argument('--interactive', action='store_true', help='Interactive flag')
parser.add_argument('--automated', action='store_true', help='Automated data flag')

parser.add_argument('--prepare', action='store_true', help='Prepare training data')

# Parse the arguments
args = parser.parse_args()

if args.train:
    train_model()

if args.prognose:
    prognose(args)

if args.evaluate:
    evaluate_model()

if args.prepare:
    call_prepare_training_data()
