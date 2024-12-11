import os
import json
import pandas as pd
import argparse
from src.data.process_twitter_data import TwitterDataProcessor
from src.analysis.prompt_generator import PromptGenerator
from src.analysis.model_interface import ModelInterface
from src.utils.config import DATA_DIR, PROMPTS_DIR, RESULTS_DIR

def process_twitter_data(raw_data_path: str) -> None:
    """Process raw Twitter data.
    
    Args:
        raw_data_path (str): Path to raw Twitter JSON file
    """
    print(f"Loading data from {raw_data_path}", flush=True)
    processor = TwitterDataProcessor(raw_data_path)
    print("Processing data...", flush=True)
    processor.process_data()
    
    # Create user-specific directory for processed data
    user_dir = os.path.join(DATA_DIR, 'processed', 
                           os.path.basename(raw_data_path).replace('.json', ''))
    print(f"Saving processed data to {user_dir}", flush=True)
    processor.save_processed_data(user_dir)
    return user_dir

def generate_prompts(processed_data_dir: str) -> str:
    """Generate prompts from processed data.
    
    Args:
        processed_data_dir (str): Directory containing processed data
        
    Returns:
        str: Path to generated prompts
    """
    print(f"Loading processed data from {processed_data_dir}", flush=True)
    # Load processed data
    with open(os.path.join(processed_data_dir, 'profile_data.json'), 'r') as f:
        profile_data = json.load(f)
    tweets_df = pd.read_csv(os.path.join(processed_data_dir, 'tweets_data.csv'))
    print("Loaded processed data successfully", flush=True)
    
    # Generate prompts
    print("Initializing prompt generator...", flush=True)
    generator = PromptGenerator(profile_data, tweets_df)
    output_dir = os.path.join(PROMPTS_DIR, 
                             os.path.basename(processed_data_dir))
    print(f"Saving prompts to {output_dir}", flush=True)
    generator.save_prompts(output_dir)
    return output_dir

def generate_model_responses(prompts_dir: str) -> None:
    """Generate responses from all models for each prompt.
    
    Args:
        prompts_dir (str): Directory containing prompt files
    """
    print(f"Initializing model interface for {prompts_dir}", flush=True)
    interface = ModelInterface()
    
    # Process each prompt type
    prompt_types = ['personality_analysis', 'chat_system', 'creative_analysis']
    for prompt_type in prompt_types:
        prompt_path = os.path.join(prompts_dir, f'{prompt_type}.txt')
        print(f"Processing {prompt_type} prompt...", flush=True)
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
        
        # Generate responses
        print(f"Generating responses for {prompt_type}...", flush=True)
        responses = interface.generate_all_responses(prompt, prompt_type)
        
        # Save responses
        output_path = os.path.join(
            RESULTS_DIR,
            os.path.basename(prompts_dir),
            f'{prompt_type}_responses.txt'
        )
        print(f"Saving responses to {output_path}", flush=True)
        interface.save_responses(responses, output_path)

def main():
    """Main function to run the entire analysis pipeline."""
    parser = argparse.ArgumentParser(description='Twitter Personality Analysis Pipeline')
    parser.add_argument('raw_data_path', type=str, help='Path to raw Twitter JSON file')
    args = parser.parse_args()
    
    print("=== Twitter Personality Analysis Pipeline ===")
    
    try:
        # Step 1: Process Twitter data
        print("\n1. Processing Twitter data...", flush=True)
        processed_dir = process_twitter_data(args.raw_data_path)
        print(f"Data processed and saved to: {processed_dir}", flush=True)
        
        # Step 2: Generate prompts
        print("\n2. Generating prompts...", flush=True)
        prompts_dir = generate_prompts(processed_dir)
        print(f"Prompts generated and saved to: {prompts_dir}", flush=True)
        
        # Step 3: Generate model responses
        print("\n3. Generating model responses...", flush=True)
        generate_model_responses(prompts_dir)
        print(f"Responses saved to: {os.path.join(RESULTS_DIR, os.path.basename(prompts_dir))}", flush=True)
        
        print("\nAnalysis pipeline completed successfully!", flush=True)
    except Exception as e:
        print(f"\nError: {str(e)}", flush=True)
        import traceback
        print("\nFull traceback:", flush=True)
        print(traceback.format_exc(), flush=True)
        raise

if __name__ == "__main__":
    main() 