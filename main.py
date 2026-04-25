#!/usr/bin/env python
"""
MADC Framework - Main Entry Point
Command-line interface for running MADC experiments
"""

import argparse
import sys
import os
from config import Config
from prompt_manager import PromptManager
from pipeline import MADCPipeline
from evaluator import Evaluator
from utils import load_jsonl, setup_logger


def main():
    parser = argparse.ArgumentParser(
        description='MADC Framework - Multi-Agent Dual-system Chain-of-Cognition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Single inference:
    python main.py --mode single --image ./data/image.png --question "What is in the image?"

  Batch processing:
    python main.py --mode batch --dataset ./data/test.jsonl

  Evaluation:
    python main.py --mode eval --dataset ./data/test.jsonl --config config.yaml
        """
    )

    parser.add_argument('--mode', type=str, default='single',
                       choices=['single', 'batch', 'eval'],
                       help='Execution mode')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--image', type=str,
                       help='Image path for single mode')
    parser.add_argument('--question', type=str,
                       help='Question for single mode')
    parser.add_argument('--dataset', type=str,
                       help='Dataset path for batch/eval mode')
    parser.add_argument('--output', type=str,
                       help='Output path for results')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')

    args = parser.parse_args()

    try:
        config = Config(args.config if os.path.exists(args.config) else None)
        config.validate()

        if args.verbose:
            config.experiment.verbose = True

        logger = setup_logger("MADC", config.experiment.log_dir)
        logger.info("Starting MADC Framework")
        logger.info(f"Mode: {args.mode}")

        prompt_manager = PromptManager()
        pipeline = MADCPipeline(config, prompt_manager, logger)

        if args.mode == 'single':
            if not args.image or not args.question:
                logger.error("--image and --question are required for single mode")
                sys.exit(1)

            result = pipeline.run(args.image, args.question)
            print("\n" + "="*50)
            print("Final Answer:")
            print("="*50)
            print(result['final_answer'])
            print("="*50 + "\n")

        elif args.mode == 'batch':
            if not args.dataset:
                logger.error("--dataset is required for batch mode")
                sys.exit(1)

            data = load_jsonl(args.dataset)
            output_path = args.output or os.path.join(config.experiment.output_dir, 'batch_results.json')
            results = pipeline.run_batch(data, output_path)
            logger.info(f"Batch processing completed. Results saved to {output_path}")

        elif args.mode == 'eval':
            if not args.dataset:
                logger.error("--dataset is required for eval mode")
                sys.exit(1)

            evaluator = Evaluator(logger)
            data = load_jsonl(args.dataset)
            results = pipeline.run_batch(data)

            ground_truths = [item.get('answer', '') for item in data]
            metrics = evaluator.evaluate_results(results, ground_truths)

            report_path = args.output or os.path.join(config.experiment.output_dir, 'evaluation_report.json')
            evaluator.generate_report(metrics, report_path)
            logger.info(f"Evaluation completed. Report saved to {report_path}")

            print("\n" + "="*50)
            print("Evaluation Metrics:")
            print("="*50)
            for key, value in metrics.items():
                print(f"{key}: {value}")
            print("="*50 + "\n")

        logger.info("MADC Framework completed successfully")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
