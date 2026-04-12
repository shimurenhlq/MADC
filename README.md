# MADC: Chain-of-Cognition Through Multi-Agent Collaboration Against Cross-Modal Cognitive Interference

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the official implementation of the paper **"Chain-of-Cognition Through Multi-Agent Collaboration Against Cross-Modal Cognitive Interference"** (Accepted by *IEEE TRANSACTIONS ON AUDIO, SPEECH AND LANGUAGE PROCESSING, 2026*).

## 💡 Introduction

Multi-modal Large Language Models (MLLMs) often suffer from **Cross-Modal Cognitive Interference (CMCI)**, where visual perception and reasoning capabilities mutually interfere during multi-modal Chain-of-Thought (CoT) reasoning. 

To address this, we propose **MADC**, a Multi-Agent Dual-system Chain-of-Cognition framework. MADC explicitly structures the cognitive process into four distinct stages:
1. **Perception**: Extracts key visual features using specialized vision-language agents.
2. **Assessment**: Evaluates cognitive load to determine if deeper reasoning is needed.
3. **Reasoning**: Performs logical deduction relying purely on extracted text context to avoid visual interference.
4. **Decision-making**: Integrates visual cues and rationales for the final answer.

## 📂 Repository Structure

- `framework.py`: The main pipeline implementing the four-stage MADC framework using LLM APIs.
- `prompt.json`: The meticulously designed prompts for the observation, reflection, reasoning, and decision stages.
- `requirements.txt`: Python dependencies required to run the code.

## 🚀 Quick Start

### 1. Install Dependencies
Create a virtual environment and install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys and Parameters
Before running the code, you **MUST** update the API configurations in `framework.py`. Please open `framework.py` and replace the `***` placeholders with your actual information:

* **API Key**: Replace `api_key="***"` with your actual OpenAI (or compatible) API Key.
* **Base URL**: Replace `base_url="***"` with your API Base URL (if applicable).
* **Model Names**: Replace `model="***"` with the specific model you wish to use for each stage (e.g., `gpt-4o`, `qwen-vl`, etc.).
* **Data Paths**: Update `image_path` and `question` variables to point to your test image and corresponding question.

### 3. Run the Framework
```bash
python framework.py
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