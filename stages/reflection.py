from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from .base import BaseStage
from utils import parse_reflection_result


class ReflectionStage(BaseStage):
    """Reflection stage: Assess cognitive load and determine if reasoning is needed"""

    def __init__(self, client: OpenAI, model_config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        super().__init__(client, model_config, logger)

    def execute(self, prompt: str) -> str:
        """
        Execute reflection stage

        Args:
            prompt: Reflection prompt including question and observation result

        Returns:
            Binary decision: '1' if direct answer possible, '0' if reasoning needed
        """
        self._log_input("Reflection", prompt=prompt[:100])

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        result = self._call_api(messages)
        parsed_result = parse_reflection_result(result)

        self._log_output("Reflection", parsed_result)

        return parsed_result
