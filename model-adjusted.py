import argparse
import logging
from config import paths
from models.adjusted.prognosis.src import interactive_prognosis, model_training, model_evaluation, automated_prognosis
from models.adjusted.data_preparation.src import training_data_adjustment

# Setup logging configuration
logging.basicConfig(filename=paths.path_log_model_adjusted, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model():
    logging.info('Training model started')
    model_training.train_model()
    logging.info('Training model completed')

def evaluate_model():
    logging.info('Model evaluation started')
    model_evaluation.evaluate_model()
    logging.info('Model evaluation completed')

def prognose(args):
    logging.info(f'Prognosis process started with args: {args}')
    if args.interactive:
        logging.info('Interactive prognosis started')
        interactive_prognosis.prognose_interactive()
        logging.info('Interactive prognosis completed')

    elif args.automated:
        logging.info('Automated prognosis started')
        automated_prognosis.prognose_automated()
        logging.info('Automated prognosis completed')

    else:
        logging.error('Invalid prognosis arguments')
        raise Exception('Invalid prognose arguments')
    logging.info('Prognosis process completed')

def call_prepare_training_data():
    logging.info('Preparation of training data started')
    training_data_adjustment.prepare_training_data()
    logging.info('Preparation of training data completed')

# Initialize the parser
parser = argparse.ArgumentParser(description="Call specific functions based on arguments")

# Train model arguments
parser.add_argument('--train', action='store_true', help='Train model')
parser.add_argument('--evaluate', action='store_true', help='Evaluate model')

# Prognosis arguments
parser.add_argument('--prognose', action='store_true', help='Prognose salaries')
parser.add_argument('--interactive', action='store_true', help='Interactive prognosis')
parser.add_argument('--automated', action='store_true', help='Automated prognosis')

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
