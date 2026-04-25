#!/bin/bash

# MADC Framework - Experiment Runner
# This script runs MADC experiments with various configurations

set -e

echo "========================================="
echo "MADC Framework - Experiment Runner"
echo "========================================="

# Default values
CONFIG_FILE="config.yaml"
MODE="single"
IMAGE_PATH=""
QUESTION=""
DATASET_PATH=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --mode)
            MODE="$2"
            shift 2
            ;;
        --image)
            IMAGE_PATH="$2"
            shift 2
            ;;
        --question)
            QUESTION="$2"
            shift 2
            ;;
        --dataset)
            DATASET_PATH="$2"
            shift 2
            ;;
        --help)
            echo "Usage: bash run_experiment.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --config FILE       Configuration file (default: config.yaml)"
            echo "  --mode MODE         Execution mode: single, batch, eval (default: single)"
            echo "  --image PATH        Image path for single mode"
            echo "  --question TEXT     Question for single mode"
            echo "  --dataset PATH      Dataset path for batch/eval mode"
            echo "  --help              Show this help message"
            echo ""
            echo "Examples:"
            echo "  Single inference:"
            echo "    bash run_experiment.sh --mode single --image ./data/image.png --question 'What is in the image?'"
            echo ""
            echo "  Batch processing:"
            echo "    bash run_experiment.sh --mode batch --dataset ./data/test.jsonl"
            echo ""
            echo "  Evaluation:"
            echo "    bash run_experiment.sh --mode eval --dataset ./data/test.jsonl"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables from .env..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run experiment based on mode
echo "Running experiment in $MODE mode..."
echo ""

case $MODE in
    single)
        if [ -z "$IMAGE_PATH" ] || [ -z "$QUESTION" ]; then
            echo "Error: --image and --question are required for single mode"
            exit 1
        fi
        python -c "
from config import Config
from prompt_manager import PromptManager
from pipeline import MADCPipeline
import json

config = Config('$CONFIG_FILE')
prompt_manager = PromptManager()
pipeline = MADCPipeline(config, prompt_manager)

result = pipeline.run('$IMAGE_PATH', '$QUESTION')
print(json.dumps(result, indent=2, ensure_ascii=False))
"
        ;;
    batch)
        if [ -z "$DATASET_PATH" ]; then
            echo "Error: --dataset is required for batch mode"
            exit 1
        fi
        python -c "
from config import Config
from prompt_manager import PromptManager
from pipeline import MADCPipeline
from utils import load_jsonl
import os

config = Config('$CONFIG_FILE')
prompt_manager = PromptManager()
pipeline = MADCPipeline(config, prompt_manager)

data = load_jsonl('$DATASET_PATH')
output_path = os.path.join(config.experiment.output_dir, 'batch_results.json')
results = pipeline.run_batch(data, output_path)
print(f'Batch processing completed. Results saved to {output_path}')
"
        ;;
    eval)
        if [ -z "$DATASET_PATH" ]; then
            echo "Error: --dataset is required for eval mode"
            exit 1
        fi
        python -c "
from config import Config
from prompt_manager import PromptManager
from pipeline import MADCPipeline
from evaluator import Evaluator
from utils import load_jsonl
import os

config = Config('$CONFIG_FILE')
prompt_manager = PromptManager()
pipeline = MADCPipeline(config, prompt_manager)
evaluator = Evaluator()

data = load_jsonl('$DATASET_PATH')
results = pipeline.run_batch(data)

ground_truths = [item.get('answer', '') for item in data]
metrics = evaluator.evaluate_results(results, ground_truths)

report_path = os.path.join(config.experiment.output_dir, 'evaluation_report.json')
evaluator.generate_report(metrics, report_path)
print(f'Evaluation completed. Report saved to {report_path}')
"
        ;;
    *)
        echo "Error: Unknown mode '$MODE'"
        echo "Valid modes: single, batch, eval"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Experiment completed successfully!"
echo "========================================="
