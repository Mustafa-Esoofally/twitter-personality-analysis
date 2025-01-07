# Twitter Personality Analyzer

A sophisticated tool for analyzing Twitter personalities using Claude AI, focusing on communication patterns, personality traits, and professional insights.

## Overview

This project provides a comprehensive framework for analyzing Twitter personalities using Anthropic's Claude AI. It processes Twitter data, generates personality analyses, and provides detailed insights into communication styles, behavioral patterns, and professional characteristics.

## Features

- **Twitter Data Processing**: Extracts and processes Twitter data from various sources
- **AI-Powered Analysis**: Leverages Claude-3 for deep personality analysis
- **Structured Output**: Generates detailed reports covering:
  - Communication Style Analysis
  - Core Personality Traits
  - Social Network Behavior
  - Professional Insights
- **Flexible Testing Framework**: Supports batch processing and individual profile analysis
- **Result Management**: Saves analyses in both structured and human-readable formats

## Project Structure

```
├── analysis_results/     # Stores analysis JSON files
├── chat_prompts/        # Contains chat prompt templates
├── curated_tweets/      # Processed and curated tweet data
├── data/               # Raw data storage
├── generated_prompts/   # Generated analysis prompts
├── processed_data/     # Intermediate processed data
├── src/               # Source code for tweet extraction
├── test_results/      # Output of personality analyses
└── requirements.txt   # Project dependencies
```

## Key Components

- `claude_tester.py`: Main analysis engine using Claude AI
- `twitter_data_processor.py`: Twitter data processing utilities
- `chat_prompts.py`: Manages chat prompt generation and templates
- `prompt_templates.py`: Template definitions for AI interactions

## Prerequisites

- Python 3.8+
- Anthropic API key (set in `.env` file)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [project-directory]
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

1. **Run Personality Analysis**:
```bash
python claude_tester.py
```

2. **Process Twitter Data**:
```bash
python twitter_data_processor.py
```

The analysis results will be saved in the `test_results` directory as text files.

## Dependencies

- anthropic==0.18.1: Claude AI API interface
- python-dotenv==1.0.1: Environment variable management
- json5==0.9.14: Enhanced JSON processing
- nltk==3.8.1: Natural language processing
- numpy==1.24.3: Numerical computing
- requests==2.31.0: HTTP requests

## Output Format

The analysis output includes detailed sections on:
- Communication style and patterns
- Core personality traits
- Social interaction behaviors
- Professional characteristics and tendencies

Results are saved as human-readable text files with clear section formatting.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Specify your license here]

## Acknowledgments

- Anthropic's Claude AI for powering the analysis
- [Add any other acknowledgments] 