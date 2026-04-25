from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from .base import BaseStage


class DecisionStage(BaseStage):
    """Decision stage: Generate final answer based on reasoning or observation"""

    def __init__(self, client: OpenAI, model_config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        super().__init__(client, model_config, logger)

    def execute(self, prompt: str) -> str:
        """
        Execute decision stage

        Args:
            prompt: Decision prompt including question and chain of thought

        Returns:
            Final answer
        """
        self._log_input("Decision", prompt=prompt[:100])

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        result = self._call_api(messages)
        self._log_output("Decision", result)

        return result
