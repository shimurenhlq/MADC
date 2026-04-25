import os
import json
import logging
from typing import Dict, Any, List, Optional
from collections import defaultdict
from utils import load_json, load_jsonl, save_json, setup_logger


class Evaluator:
    """Evaluator for M3CoT dataset and other benchmarks"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or setup_logger("Evaluator")

    def load_dataset(self, dataset_path: str, dataset_type: str = "m3cot") -> List[Dict[str, Any]]:
        """
        Load dataset from file

        Args:
            dataset_path: Path to dataset file
            dataset_type: Type of dataset (m3cot, scienceqa, etc.)

        Returns:
            List of dataset items
        """
        self.logger.info(f"Loading dataset from {dataset_path}")

        if dataset_path.endswith('.jsonl'):
            data = load_jsonl(dataset_path)
        elif dataset_path.endswith('.json'):
            data = load_json(dataset_path)
        else:
            raise ValueError(f"Unsupported file format: {dataset_path}")

        self.logger.info(f"Loaded {len(data)} items from dataset")
        return data

    def extract_answer(self, text: str, choices: Optional[List[str]] = None) -> str:
        """
        Extract answer from model output

        Args:
            text: Model output text
            choices: List of possible choices (if multiple choice)

        Returns:
            Extracted answer
        """
        text = text.strip().lower()

        if choices:
            for choice in choices:
                if choice.lower() in text:
                    return choice

        return text

    def calculate_accuracy(self, predictions: List[str], ground_truths: List[str]) -> float:
        """
        Calculate accuracy

        Args:
            predictions: List of predicted answers
            ground_truths: List of ground truth answers

        Returns:
            Accuracy score
        """
        if len(predictions) != len(ground_truths):
            raise ValueError("Predictions and ground truths must have the same length")

        correct = sum(1 for pred, gt in zip(predictions, ground_truths)
                     if pred.strip().lower() == gt.strip().lower())
        accuracy = correct / len(predictions) if predictions else 0.0

        return accuracy

    def evaluate_results(self, results: List[Dict[str, Any]],
                        ground_truths: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluate pipeline results

        Args:
            results: List of pipeline results
            ground_truths: Optional list of ground truth answers

        Returns:
            Evaluation metrics
        """
        self.logger.info("Evaluating results")

        metrics = {
            "total": len(results),
            "successful": 0,
            "failed": 0,
            "reasoning_used": 0,
            "direct_answer": 0
        }

        predictions = []
        for result in results:
            if "error" in result:
                metrics["failed"] += 1
            else:
                metrics["successful"] += 1
                if result.get("stages", {}).get("reasoning"):
                    metrics["reasoning_used"] += 1
                else:
                    metrics["direct_answer"] += 1

                predictions.append(result.get("final_answer", ""))

        if ground_truths and len(ground_truths) == metrics["successful"]:
            metrics["accuracy"] = self.calculate_accuracy(predictions, ground_truths)
            self.logger.info(f"Accuracy: {metrics['accuracy']:.4f}")

        metrics["success_rate"] = metrics["successful"] / metrics["total"] if metrics["total"] > 0 else 0
        metrics["reasoning_rate"] = metrics["reasoning_used"] / metrics["successful"] if metrics["successful"] > 0 else 0

        self.logger.info(f"Evaluation complete: {metrics}")

        return metrics

    def analyze_by_category(self, results: List[Dict[str, Any]],
                           categories: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze results by category

        Args:
            results: List of pipeline results
            categories: List of categories for each result

        Returns:
            Category-wise metrics
        """
        category_results = defaultdict(list)

        for result, category in zip(results, categories):
            category_results[category].append(result)

        category_metrics = {}
        for category, cat_results in category_results.items():
            category_metrics[category] = self.evaluate_results(cat_results)

        return category_metrics

    def generate_report(self, metrics: Dict[str, Any], output_path: str):
        """
        Generate evaluation report

        Args:
            metrics: Evaluation metrics
            output_path: Path to save report
        """
        self.logger.info(f"Generating report at {output_path}")

        report = {
            "summary": metrics,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }

        save_json(report, output_path)
        self.logger.info("Report generated successfully")
