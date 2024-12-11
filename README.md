# Twitter Personality Analysis & Prompt Generation

This project analyzes Twitter data to generate personality insights and create effective chatbot prompts using multiple AI models.

## Project Structure
```
.
├── data/               # Raw and processed Twitter data
├── src/               # Source code
│   ├── data/          # Data processing modules
│   ├── analysis/      # Analysis and prompt generation
│   └── utils/         # Utility functions
├── notebooks/         # Jupyter notebooks for analysis
├── prompts/          # Generated prompts and templates
└── results/          # Analysis outputs and visualizations
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with your API keys:
```
ANTHROPIC_API_KEY=your_key_here
HUGGINGFACE_API_TOKEN=your_token_here
```

## Usage

1. Data Processing:
```bash
python src/data/process_twitter_data.py
```

2. Generate Analysis:
```bash
python src/analysis/generate_analysis.py
```

## Models Used
- Anthropic's Claude
- Midnight Miqu 70B
- [Third model choice]

## Features
- Twitter data processing and cleaning
- Personality psychoanalysis generation
- Chat system prompt generation
- Creative output generation

## Output Types
1. Personality Psychoanalysis
   - Unique traits and quirks analysis
   - Popular tweet analysis
   - Casual and insightful style

2. Chat System Prompt
   - Personality essence capture
   - Interaction style guidelines
   - Behavioral boundaries
   - Deployment-ready format

3. Creative Output
   - Custom analysis format
   - Unique perspective on profile data
   - Documentation of approach
``` 