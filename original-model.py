import argparse

from models.original.prognosis.src import interactive_prognosis, model_training, model_evaluation, \
    automated_prognosis


# TODO: Abhängigkeiten ausarbeiten, dass Parameter nur in bestimmten Kombinationen funktionieren
# TODO: Paths in zentrale Datei außerhalb der Modelle verwalten?

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


# Initialize the parser
parser = argparse.ArgumentParser(description="Script to call specific functions based on arguments")

# Prepare data argument
parser.add_argument('--prepare', action='store_true', help='Prepare flag')

# Train model arguments
parser.add_argument('--train', action='store_true', help='Train model flag')
parser.add_argument('--evaluate', action='store_true', help='Evaluation flag')

# Prognosis arguments
parser.add_argument('--prognose', action='store_true', help='Prognose flag')
parser.add_argument('--interactive', action='store_true', help='Interactive flag')
parser.add_argument('--automated', action='store_true', help='Automated data flag')


# Parse the arguments
args = parser.parse_args()

if args.train:
    train_model()

if args.prognose:
    prognose(args)

if args.evaluate:
    evaluate_model()
