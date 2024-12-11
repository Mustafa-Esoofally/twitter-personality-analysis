import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

# Local Model Configuration
LOCAL_MODEL_URL = os.getenv('LOCAL_MODEL_URL', 'http://127.0.0.1:7860')

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
PROMPTS_DIR = os.path.join(PROJECT_ROOT, 'prompts')

# Model configurations
MODELS = {
    'claude': {
        'name': 'claude-2',
        'provider': 'anthropic',
        'type': 'api'
    },
    'miqu': {
        'name': 'sophosympatheia/Midnight-Miqu-70B-v1.0',
        'provider': 'local',
        'type': 'local',
        'url': LOCAL_MODEL_URL
    }
}

# Analysis parameters
MAX_TWEETS_PER_PROFILE = 1000
ANALYSIS_TYPES = ['personality', 'chat_system', 'creative'] 