import os
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Model configuration for each stage"""
    name: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95


@dataclass
class StageConfig:
    """Configuration for each cognitive stage"""
    observation: ModelConfig = field(default_factory=ModelConfig)
    reflection: ModelConfig = field(default_factory=ModelConfig)
    reasoning: ModelConfig = field(default_factory=ModelConfig)
    decision: ModelConfig = field(default_factory=ModelConfig)


@dataclass
class APIConfig:
    """API configuration"""
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0


@dataclass
class ExperimentConfig:
    """Experiment configuration"""
    dataset_path: str = "./data"
    output_dir: str = "./results"
    log_dir: str = "./logs"
    batch_size: int = 1
    save_intermediate: bool = True
    verbose: bool = True


class Config:
    """Main configuration manager"""

    def __init__(self, config_path: Optional[str] = None):
        self.api = APIConfig()
        self.stages = StageConfig()
        self.experiment = ExperimentConfig()

        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)
        else:
            self.load_from_env()

    def load_from_file(self, config_path: str):
        """Load configuration from YAML file"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)

        if 'api' in config_dict:
            for key, value in config_dict['api'].items():
                if hasattr(self.api, key):
                    setattr(self.api, key, value)

        if 'stages' in config_dict:
            for stage_name, stage_config in config_dict['stages'].items():
                if hasattr(self.stages, stage_name):
                    model_config = ModelConfig(**stage_config)
                    setattr(self.stages, stage_name, model_config)

        if 'experiment' in config_dict:
            for key, value in config_dict['experiment'].items():
                if hasattr(self.experiment, key):
                    setattr(self.experiment, key, value)

    def load_from_env(self):
        """Load configuration from environment variables"""
        self.api.api_key = os.getenv('OPENAI_API_KEY', '')
        self.api.base_url = os.getenv('OPENAI_BASE_URL', self.api.base_url)

    def validate(self) -> bool:
        """Validate configuration"""
        if not self.api.api_key:
            raise ValueError("API key is required. Set OPENAI_API_KEY environment variable or provide in config file.")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'api': {
                'base_url': self.api.base_url,
                'timeout': self.api.timeout,
                'max_retries': self.api.max_retries,
                'retry_delay': self.api.retry_delay
            },
            'stages': {
                'observation': vars(self.stages.observation),
                'reflection': vars(self.stages.reflection),
                'reasoning': vars(self.stages.reasoning),
                'decision': vars(self.stages.decision)
            },
            'experiment': vars(self.experiment)
        }
