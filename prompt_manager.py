import os
import json
from typing import Dict, Optional
from utils import load_json


class PromptManager:
    """Manages prompts for different stages of the MADC framework"""

    def __init__(self, prompt_path: str = "./prompt.json"):
        self.prompt_path = prompt_path
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        """Load prompts from JSON file"""
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_path}")
        return load_json(self.prompt_path)

    def get_observation_prompt(self, question: str) -> str:
        """Get observation stage prompt"""
        template = self.prompts.get("observation_stage", "")
        return f"{template}\n\nQuestion: {question}"

    def get_reflection_prompt(self, question: str, observation_result: str) -> str:
        """Get reflection stage prompt"""
        template = self.prompts.get("reflection_stage", "")
        return f"{template}\n\nQuestion: {question}\n\nImage Description: {observation_result}"

    def get_reasoning_prompt(self, question: str, observation_result: str) -> str:
        """Get reasoning stage prompt"""
        template = self.prompts.get("reasoning_stage", "")
        return f"{template}\n\nQuestion: {question}\n\nImage Description: {observation_result}"

    def get_decision_prompt(self, question: str, chain_of_thought: str) -> str:
        """Get decision stage prompt"""
        template = self.prompts.get("decision_stage", "")
        return f"{template}\n\nQuestion: {question}\n\nChain of Thought: {chain_of_thought}"

    def get_stage_prompt(self, stage: str) -> str:
        """Get raw prompt for a specific stage"""
        stage_key = f"{stage}_stage"
        if stage_key not in self.prompts:
            raise ValueError(f"Unknown stage: {stage}")
        return self.prompts[stage_key]

    def update_prompt(self, stage: str, new_prompt: str):
        """Update prompt for a specific stage"""
        stage_key = f"{stage}_stage"
        if stage_key not in self.prompts:
            raise ValueError(f"Unknown stage: {stage}")
        self.prompts[stage_key] = new_prompt

    def save_prompts(self, output_path: Optional[str] = None):
        """Save prompts to file"""
        save_path = output_path or self.prompt_path
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.prompts, f, ensure_ascii=False, indent=2)

    def reload(self):
        """Reload prompts from file"""
        self.prompts = self._load_prompts()

    def validate(self) -> bool:
        """Validate that all required prompts are present"""
        required_stages = ["observation_stage", "reflection_stage", "reasoning_stage", "decision_stage"]
        for stage in required_stages:
            if stage not in self.prompts or not self.prompts[stage]:
                raise ValueError(f"Missing or empty prompt for: {stage}")
        return True
