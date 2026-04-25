# MADC: Chain-of-Cognition Through Multi-Agent Collaboration Against Cross-Modal Cognitive Interference

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the official implementation of the paper **"Chain-of-Cognition Through Multi-Agent Collaboration Against Cross-Modal Cognitive Interference"** (Accepted by *IEEE TRANSACTIONS ON AUDIO, SPEECH AND LANGUAGE PROCESSING, 2026*).

## 💡 Introduction

Multi-modal Large Language Models (MLLMs) often suffer from **Cross-Modal Cognitive Interference (CMCI)**, where visual perception and reasoning capabilities mutually interfere during multi-modal Chain-of-Thought (CoT) reasoning. 

To address this, we propose **MADC**, a Multi-Agent Dual-system Chain-of-Cognition framework. MADC explicitly structures the cognitive process into four distinct stages:
1. **Observation (Perception)**: Extracts key visual features using specialized vision-language agents.
2. **Reflection (Assessment)**: Evaluates cognitive load to determine if deeper reasoning is needed.
3. **Reasoning**: Performs logical deduction relying purely on extracted text context to avoid visual interference.
4. **Decision-making**: Integrates visual cues and rationales for the final answer.

## 📂 Repository Structure

```
MADC/
├── config.py                 # Configuration management system
├── config.yaml              # Hyperparameter configuration file
├── prompt_manager.py        # Prompt loading and management
├── utils.py                 # Utility functions (logging, I/O, etc.)
├── pipeline.py              # Main MADC pipeline orchestration
├── evaluator.py             # Evaluation metrics and analysis
├── stages/                  # Modular stage implementations
│   ├── __init__.py
│   ├── base.py             # Base class for all stages
│   ├── observation.py      # Observation stage
│   ├── reflection.py       # Reflection stage
│   ├── reasoning.py        # Reasoning stage
│   └── decision.py         # Decision stage
├── prompt.json             # Stage-specific prompts
├── framework.py            # Legacy single-file implementation
├── setup.sh                # Environment setup script
├── run_experiment.sh       # Experiment runner script
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### 1. Environment Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
bash setup.sh
```

This will:
- Create a Python virtual environment
- Install all required dependencies
- Create necessary directories (data, results, logs)
- Generate a `.env` template file

### 2. Configure API Credentials

Edit the `.env` file with your API credentials:

```bash
# .env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. Configure Hyperparameters (Optional)

Edit `config.yaml` to customize model parameters for each stage:

```yaml
stages:
  observation:
    name: "gpt-4o"
    temperature: 0.7
    max_tokens: 2048
  reflection:
    name: "gpt-4o"
    temperature: 0.3
    max_tokens: 512
  # ... other stages
```

### 4. Run Experiments

#### Single Image Inference

```bash
bash run_experiment.sh --mode single \
  --image ./data/image.png \
  --question "What is in the image?"
```

#### Batch Processing

Prepare a JSONL file with your dataset:

```jsonl
{"image_path": "./data/image1.png", "question": "What is this?"}
{"image_path": "./data/image2.png", "question": "Describe the scene."}
```

Run batch processing:

```bash
bash run_experiment.sh --mode batch --dataset ./data/test.jsonl
```

#### Evaluation Mode

For datasets with ground truth answers:

```bash
bash run_experiment.sh --mode eval --dataset ./data/test.jsonl
```

This will generate an evaluation report with accuracy metrics.

## 🔧 Advanced Usage

### Python API

You can also use the framework programmatically:

```python
from config import Config
from prompt_manager import PromptManager
from pipeline import MADCPipeline

# Initialize
config = Config('config.yaml')
prompt_manager = PromptManager()
pipeline = MADCPipeline(config, prompt_manager)

# Run single inference
result = pipeline.run(
    image_path='./data/image.png',
    question='What is in the image?'
)

print(result['final_answer'])
```

### Custom Prompts

Modify `prompt.json` to customize the prompts for each stage:

```json
{
  "observation_stage": "Your custom observation prompt...",
  "reflection_stage": "Your custom reflection prompt...",
  "reasoning_stage": "Your custom reasoning prompt...",
  "decision_stage": "Your custom decision prompt..."
}
```

### Evaluation and Analysis

```python
from evaluator import Evaluator

evaluator = Evaluator()

# Load results
results = evaluator.load_dataset('./results/batch_results.json')

# Evaluate with ground truth
ground_truths = ['answer1', 'answer2', ...]
metrics = evaluator.evaluate_results(results, ground_truths)

# Generate report
evaluator.generate_report(metrics, './results/report.json')
```

## 📊 Features

- **Modular Architecture**: Each cognitive stage is implemented as a separate module for easy customization
- **Flexible Configuration**: YAML-based configuration for hyperparameters and model settings
- **Robust Error Handling**: Automatic retry logic and comprehensive logging
- **Batch Processing**: Efficient processing of multiple samples
- **Evaluation Tools**: Built-in metrics and analysis for M3CoT and other benchmarks
- **Extensible Design**: Easy to add new stages or modify existing ones

## 🧪 Testing on M3CoT Dataset

The framework is designed to work seamlessly with the M3CoT dataset. Prepare your data in JSONL format:

```jsonl
{"image_path": "./data/m3cot/image1.png", "question": "...", "answer": "..."}
```

Run evaluation:

```bash
bash run_experiment.sh --mode eval --dataset ./data/m3cot_test.jsonl
```

## 📖 Citation

If you find this code or our paper useful in your research, please consider citing:

```bibtex
@article{he2026chain,
  title={Chain-of-Cognition Through Multi-Agent Collaboration Against Cross-Modal Cognitive Interference},
  author={He, Liqi and Li, Zuchao and Shen, Mengjia and Wang, Ping and Zhang, Lefei},
  journal={IEEE Transactions on Audio, Speech and Language Processing},
  year={2026},
  publisher={IEEE}
}
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or issues, please open an issue on GitHub or contact the authors.