from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from config import Config
from prompt_manager import PromptManager
from stages import ObservationStage, ReflectionStage, ReasoningStage, DecisionStage
from utils import setup_logger, Timer, save_json


class MADCPipeline:
    """Main pipeline for MADC framework"""

    def __init__(self, config: Config, prompt_manager: PromptManager, logger: Optional[logging.Logger] = None):
        self.config = config
        self.prompt_manager = prompt_manager
        self.logger = logger or setup_logger("MADCPipeline", config.experiment.log_dir)

        self.client = OpenAI(
            api_key=config.api.api_key,
            base_url=config.api.base_url,
            timeout=config.api.timeout
        )

        self.observation_stage = ObservationStage(
            self.client,
            vars(config.stages.observation),
            self.logger
        )
        self.reflection_stage = ReflectionStage(
            self.client,
            vars(config.stages.reflection),
            self.logger
        )
        self.reasoning_stage = ReasoningStage(
            self.client,
            vars(config.stages.reasoning),
            self.logger
        )
        self.decision_stage = DecisionStage(
            self.client,
            vars(config.stages.decision),
            self.logger
        )

    def run(self, image_path: str, question: str, save_intermediate: bool = None) -> Dict[str, Any]:
        """
        Run the complete MADC pipeline

        Args:
            image_path: Path to input image
            question: Question to answer
            save_intermediate: Whether to save intermediate results

        Returns:
            Dictionary containing all stage results
        """
        if save_intermediate is None:
            save_intermediate = self.config.experiment.save_intermediate

        self.logger.info(f"Starting MADC pipeline for question: {question}")
        results = {
            "image_path": image_path,
            "question": question,
            "stages": {}
        }

        with Timer("Complete Pipeline", self.logger):
            with Timer("Observation Stage", self.logger):
                observation_prompt = self.prompt_manager.get_observation_prompt(question)
                observation_result = self.observation_stage.execute(image_path, observation_prompt)
                results["stages"]["observation"] = observation_result

            with Timer("Reflection Stage", self.logger):
                reflection_prompt = self.prompt_manager.get_reflection_prompt(question, observation_result)
                reflection_result = self.reflection_stage.execute(reflection_prompt)
                results["stages"]["reflection"] = reflection_result

            if reflection_result != "1":
                with Timer("Reasoning Stage", self.logger):
                    reasoning_prompt = self.prompt_manager.get_reasoning_prompt(question, observation_result)
                    reasoning_result = self.reasoning_stage.execute(reasoning_prompt)
                    results["stages"]["reasoning"] = reasoning_result
                    chain_of_thought = reasoning_result
            else:
                self.logger.info("Skipping reasoning stage (direct answer possible)")
                results["stages"]["reasoning"] = None
                chain_of_thought = observation_result

            with Timer("Decision Stage", self.logger):
                decision_prompt = self.prompt_manager.get_decision_prompt(question, chain_of_thought)
                decision_result = self.decision_stage.execute(decision_prompt)
                results["stages"]["decision"] = decision_result
                results["final_answer"] = decision_result

        self.logger.info(f"Pipeline completed. Final answer: {decision_result}")

        return results

    def run_batch(self, data_list: list, output_path: Optional[str] = None) -> list:
        """
        Run pipeline on a batch of data

        Args:
            data_list: List of dictionaries with 'image_path' and 'question' keys
            output_path: Path to save batch results

        Returns:
            List of results
        """
        self.logger.info(f"Starting batch processing for {len(data_list)} items")
        all_results = []

        for idx, data in enumerate(data_list):
            self.logger.info(f"Processing item {idx + 1}/{len(data_list)}")
            try:
                result = self.run(data["image_path"], data["question"])
                result["index"] = idx
                all_results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing item {idx}: {str(e)}")
                all_results.append({
                    "index": idx,
                    "error": str(e),
                    "image_path": data.get("image_path"),
                    "question": data.get("question")
                })

        if output_path:
            save_json(all_results, output_path)
            self.logger.info(f"Batch results saved to {output_path}")

        return all_results
