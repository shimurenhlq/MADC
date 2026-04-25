from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from .base import BaseStage


class ReasoningStage(BaseStage):
    """Reasoning stage: Perform logical deduction based on text context"""

    def __init__(self, client: OpenAI, model_config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        super().__init__(client, model_config, logger)

    def execute(self, prompt: str) -> str:
        """
        Execute reasoning stage

        Args:
            prompt: Reasoning prompt including question and observation result

        Returns:
            Chain of thought reasoning
        """
        self._log_input("Reasoning", prompt=prompt[:100])

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        result = self._call_api(messages)
        self._log_output("Reasoning", result)

        return result
