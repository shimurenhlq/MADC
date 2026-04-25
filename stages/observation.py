from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from .base import BaseStage
from utils import encode_image, get_image_format


class ObservationStage(BaseStage):
    """Observation stage: Extract visual features from image"""

    def __init__(self, client: OpenAI, model_config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        super().__init__(client, model_config, logger)

    def execute(self, image_path: str, prompt: str) -> str:
        """
        Execute observation stage

        Args:
            image_path: Path to the input image
            prompt: Observation prompt including the question

        Returns:
            Visual description and analysis
        """
        self._log_input("Observation", image_path=image_path, prompt=prompt[:100])

        base64_image = encode_image(image_path)
        image_format = get_image_format(image_path)

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{image_format};base64,{base64_image}"
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        result = self._call_api(messages)
        self._log_output("Observation", result)

        return result
