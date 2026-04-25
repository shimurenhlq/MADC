from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import logging
from openai import OpenAI


class BaseStage(ABC):
    """Base class for all cognitive stages"""

    def __init__(self, client: OpenAI, model_config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.client = client
        self.model_config = model_config
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self, *args, **kwargs) -> str:
        """Execute the stage logic"""
        pass

    def _call_api(self, messages: list, max_retries: int = 3, retry_delay: float = 1.0) -> str:
        """Call OpenAI API with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_config.get('name', 'gpt-4o'),
                    messages=messages,
                    temperature=self.model_config.get('temperature', 0.7),
                    max_tokens=self.model_config.get('max_tokens', 2048),
                    top_p=self.model_config.get('top_p', 0.95)
                )
                return response.choices[0].message.content
            except Exception as e:
                self.logger.warning(f"API call failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise

    def _log_input(self, stage_name: str, **kwargs):
        """Log stage input"""
        self.logger.info(f"[{stage_name}] Input: {kwargs}")

    def _log_output(self, stage_name: str, output: str):
        """Log stage output"""
        self.logger.info(f"[{stage_name}] Output: {output[:200]}...")
