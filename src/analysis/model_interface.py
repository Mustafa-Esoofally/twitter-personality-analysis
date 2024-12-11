import os
from typing import Dict, Any
import anthropic
import requests
from ..utils.config import MODELS, ANTHROPIC_API_KEY, LOCAL_MODEL_URL

class ModelInterface:
    def __init__(self):
        """Initialize model interfaces."""
        self.claude = anthropic.Client(api_key=ANTHROPIC_API_KEY)
        self.local_model_url = LOCAL_MODEL_URL

    def generate_with_claude(self, prompt: str) -> str:
        """Generate response using Claude."""
        response = self.claude.completions.create(
            model="claude-2",
            max_tokens_to_sample=1000,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:"
        )
        return response.completion

    def generate_with_miqu(self, prompt: str) -> str:
        """Generate response using local Midnight Miqu model.
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            str: Generated response
        """
        try:
            payload = {
                "prompt": f"### Instruction: {prompt}\n### Response:",
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
                "typical_p": 0.9,
                "repetition_penalty": 1.1,
                "encoder_repetition_penalty": 1.0,
                "top_k": 0,
                "min_length": 0,
                "no_repeat_ngram_size": 0,
                "num_beams": 1,
                "penalty_alpha": 0,
                "length_penalty": 1,
                "early_stopping": True,
                "seed": -1,
                "add_bos_token": True,
                "truncation_length": 4096,
                "ban_eos_token": False,
                "skip_special_tokens": True,
                "stopping_strings": ["### Instruction:", "### Response:"]
            }
            
            response = requests.post(f"{self.local_model_url}/api/v1/generate", json=payload)
            response.raise_for_status()
            return response.json()['results'][0]['text'].strip()
        except Exception as e:
            print(f"Error generating Miqu response: {str(e)}", flush=True)
            raise

    def generate_all_responses(self, prompt: str, prompt_type: str) -> Dict[str, str]:
        """Generate responses from all models for a prompt."""
        responses = {}
        
        # Generate Claude response
        try:
            responses['claude'] = self.generate_with_claude(prompt)
        except Exception as e:
            print(f"Error generating Claude response: {str(e)}", flush=True)
            responses['claude'] = f"Error: {str(e)}"
            
        # Generate Miqu response
        try:
            responses['miqu'] = self.generate_with_miqu(prompt)
        except Exception as e:
            print(f"Error generating Miqu response: {str(e)}", flush=True)
            responses['miqu'] = f"Error: {str(e)}"
        
        return responses

    def save_responses(self, responses: Dict[str, str], output_path: str) -> None:
        """Save model responses to a file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for model, response in responses.items():
                f.write(f"=== {model.upper()} RESPONSE ===\n\n")
                f.write(response)
                f.write("\n\n")

def main():
    """Main function to test model interface."""
    interface = ModelInterface()
    
    test_prompt = """Analyze the following tweet:
    "Just had the most amazing coffee experience at this hidden gem in SF! ☕️✨ The barista was literally an artist! #CoffeeLife #SanFrancisco"
    
    Provide a brief personality analysis of the author."""
    
    responses = interface.generate_all_responses(test_prompt, "test")
    interface.save_responses(responses, "test_responses.txt")

if __name__ == "__main__":
    main() 