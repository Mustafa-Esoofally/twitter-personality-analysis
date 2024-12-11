import os
import json
from typing import Dict, Optional, Literal
import anthropic
from huggingface_hub import InferenceClient
import requests
from personality_analyzer import PersonalityAnalyzer, load_profile

class ModelInterface:
    def __init__(self, mock_responses: bool = True):
        """Initialize with mock_responses=True for testing without API keys"""
        self.mock_responses = mock_responses
        if not mock_responses:
            # Initialize API keys from environment variables
            self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
            self.huggingface_key = os.getenv('HUGGINGFACE_API_TOKEN')  # Updated to match .env
            self.openai_key = os.getenv('OPENAI_API_KEY')
            
            print("API Keys found:")
            print(f"Anthropic: {'Yes' if self.anthropic_key else 'No'}")
            print(f"Hugging Face: {'Yes' if self.huggingface_key else 'No'}")
            print(f"OpenAI: {'Yes' if self.openai_key else 'No'}")
            
            # Initialize clients
            try:
                self.claude = anthropic.Anthropic(api_key=self.anthropic_key) if self.anthropic_key else None
                self.hf_client = InferenceClient(token=self.huggingface_key) if self.huggingface_key else None
            except Exception as e:
                print(f"Error initializing clients: {str(e)}")
                raise
    
    def _call_claude(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call Claude API with proper error handling."""
        if self.mock_responses:
            return "[Claude's analysis would appear here - mock response for testing]"
            
        try:
            message = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=max_tokens,
                temperature=0.7,
                system="You are an expert in psychological analysis and digital behavior patterns.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content
        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            return "[Error: Could not generate Claude's analysis]"

    def _call_midnight_miqu(self, prompt: str) -> str:
        """Call Hugging Face model through inference API."""
        if self.mock_responses:
            return "[Midnight Miqu's analysis would appear here - mock response for testing]"
            
        try:
            response = self.hf_client.text_generation(
                prompt,
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                max_new_tokens=1000,
                temperature=0.7,
                repetition_penalty=1.1
            )
            # Extract just the text content from the TextBlock
            if hasattr(response, 'text'):
                return response.text
            return str(response)
        except Exception as e:
            print(f"Error calling Hugging Face API: {str(e)}")
            return "[Error: Could not generate Hugging Face model's analysis]"

    def _call_gpt4(self, prompt: str) -> str:
        """Call GPT-4 API."""
        if self.mock_responses:
            return "[GPT-4's analysis would appear here - mock response for testing]"
            
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling GPT-4 API: {str(e)}")
            return "[Error: Could not generate GPT-4's analysis]"

    def generate_analysis(self, 
                         prompt: str, 
                         analysis_type: Literal["psychoanalysis", "chat_system", "creative"],
                         model: Literal["claude", "midnight_miqu", "gpt4"]) -> str:
        """Generate analysis using specified model."""
        
        # Add specific instructions based on model strengths and analysis type
        if model == "claude":
            if analysis_type == "psychoanalysis":
                # Claude excels at detailed psychological analysis
                prompt = f"""You are Claude, an expert in psychological analysis and digital behavior patterns.
Please analyze this Twitter profile's psychological characteristics, focusing on:
1. Professional identity and communication style
2. Community engagement patterns
3. Technical expertise demonstration
4. Knowledge sharing approaches
5. Organizational voice and brand personality

{prompt}

Please structure your response with clear sections and provide specific examples from the data."""
            
        elif model == "midnight_miqu":
            if analysis_type == "chat_system":
                # For creative chat system design
                prompt = f"""You are an AI expert in understanding technical community dynamics.
Analyze this Twitter profile's communication patterns, focusing on:
1. Technical knowledge presentation style
2. Community teaching and mentoring approach
3. Response patterns to technical questions
4. Educational content structure
5. Developer community engagement style

{prompt}

Express your insights in a way that helps create an authentic technical community voice."""
            
        else:  # gpt4
            if analysis_type == "creative":
                # For innovative technical content analysis
                prompt = f"""You are an AI expert in technical community analysis and educational psychology.
Analyze this Twitter profile's approach to technical education and community building:
1. Teaching methodology and knowledge sharing
2. Content accessibility and progression
3. Community building strategies
4. Technical authority establishment
5. Educational impact measurement

{prompt}

Structure your response to highlight both quantitative metrics and qualitative observations."""

        # Call appropriate model and ensure string response
        response = None
        if model == "claude":
            response = self._call_claude(prompt)
        elif model == "midnight_miqu":
            response = self._call_midnight_miqu(prompt)
        else:
            response = self._call_gpt4(prompt)
            
        # Ensure we return a string
        return str(response) if response is not None else "[No response generated]"

def save_analysis(analysis: Dict[str, str], output_file: str):
    """Save the analysis results to a JSON file."""
    # Convert any non-string values to strings
    serializable_analysis = {
        k: str(v) if not isinstance(v, str) else v
        for k, v in analysis.items()
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_analysis, f, indent=2, ensure_ascii=False)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate personality analysis using multiple models')
    parser.add_argument('username', help='Twitter username to analyze')
    parser.add_argument('--mock', action='store_true', help='Use mock responses instead of real API calls')
    
    args = parser.parse_args()
    
    try:
        # Load profile data
        print(f"\nLoading profile data for {args.username}...")
        profile_data = load_profile(args.username)
        
        if not profile_data:
            print(f"Failed to load profile data for @{args.username}")
            return
            
        print("Profile data loaded successfully.")
        
        # Initialize analyzer and model interface
        print("\nInitializing analyzer and model interface...")
        analyzer = PersonalityAnalyzer(profile_data)
        model_interface = ModelInterface(mock_responses=args.mock)
        
        # Generate prompts with specific focus for each model
        print("\nGenerating analysis prompts...")
        prompts = {
            "psychoanalysis": analyzer.generate_psychoanalysis_prompt(),
            "chat_system": analyzer.generate_chat_system_prompt(),
            "creative": analyzer.generate_creative_analysis("technical")
        }
        
        # Generate analyses using different models
        analyses = {}
        
        print(f"\nAnalyzing @{args.username}'s Twitter profile...")
        
        # Psychological Analysis by Claude
        print("\n1. Generating Professional Identity Analysis using Claude...")
        try:
            analyses["professional_identity_claude"] = model_interface.generate_analysis(
                prompts["psychoanalysis"], "psychoanalysis", "claude"
            )
        except Exception as e:
            print(f"Error during Claude analysis: {str(e)}")
            analyses["professional_identity_claude"] = "[Error during analysis]"
        
        # Community Engagement Analysis by Hugging Face model
        print("\n2. Generating Community Engagement Analysis using Hugging Face model...")
        try:
            analyses["community_engagement_hf"] = model_interface.generate_analysis(
                prompts["chat_system"], "chat_system", "midnight_miqu"
            )
        except Exception as e:
            print(f"Error during Hugging Face analysis: {str(e)}")
            analyses["community_engagement_hf"] = "[Error during analysis]"
        
        # Technical Education Analysis by GPT-4
        print("\n3. Generating Technical Education Analysis using GPT-4...")
        try:
            analyses["technical_education_gpt4"] = model_interface.generate_analysis(
                prompts["creative"], "creative", "gpt4"
            )
        except Exception as e:
            print(f"Error during GPT-4 analysis: {str(e)}")
            analyses["technical_education_gpt4"] = "[Error during analysis]"
        
        # Save results
        output_file = f"analysis_results_{args.username}.json"
        save_analysis(analyses, output_file)
        print(f"\nAnalyses saved to {output_file}")
        
        # Print results
        print("\nAnalysis Results:")
        print("=" * 80)
        
        for analysis_type, content in analyses.items():
            print(f"\n{analysis_type.upper()}:")
            print("-" * 40)
            print(content)
            print("\n" + "=" * 80)
            
    except Exception as e:
        print(f"An error occurred during analysis: {str(e)}")
        raise

if __name__ == '__main__':
    main() 