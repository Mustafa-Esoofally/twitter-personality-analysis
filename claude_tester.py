import os
import json
import anthropic
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ClaudeTester:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude tester with API key."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set in ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.analysis_dir = "analysis_results"
        self.test_results_dir = "test_results"
        
        # Example tweets for few-shot prompting
        self.example_tweets = [
            "&gt;be me 1 year ago today\n&gt;never had built a product for paying customers\n&gt;3 months of experience as a swe intern\n&gt;15 mins of leetcode to my name\n&gt;epiphany that college is the wagie funnel\n\ntoday marks 1m arr",
            "If you're a software engineer and check one of these boxes dm me so I can hire you:\n-Diamond+ peak in League\n-50%+ of net worth is in Bitcoin\n-Waterloo\n\nTechnical interview will be clean arch install in less than 15 mins.",
            "i embraced a dull industry, built a shitty product, learned to sell b2b saas and hired smart people\n\nthat's the equation",
            "tpot is too unemployable\n\ni have interviewed dozens of you\n\nstick to poasting my friends",
            "Do we have prediction markets for shorting startups yet?",
            "99% of you need to stop studying deep learning and start studying sales",
            "current iteration: chief oracle, hire the best, fire fast, blitzscale without ever losing board control",
            "If you want to be great you have to either create or find the unconventional alpha.\n\nfacebook\nbitcoin\nyc\ntpot\n\nThese ideas were for clinically insane people at one point. Now they're for normies.\n\nIf your training data is the same as everyone else, you won't win.",
            "the ai perception gap is getting wider\n\nthat means ai products without pmf are about to capitulate 2022 crypto style",
            "read this pg essay and stopped going to school\n\ndecisiveness is learned. the longer you procrastinate going all in, the more you're teaching yourself to fail as a founder",
            "Candidate mentions langchain\n\nEasiest filter",
            "200K ARR closed in the last 48 hours, ACV: 7K.\n\nyour nextjs slop is nothing without some wolf of wall street demons behind it",
            "sales is not haskell\n\nautism is not a requirement\n\njust show them something and ask for a credit card",
            "Not going to like doxx but the aggregate of capital raised from top founders (8+) who interacted with this post is 1B+.\n\ntpot is the new leetcode slop by consensus\n\nI'm sorry, but it's so over",
            "I'd rather get a lobotomy than grow an audience on linkedin"
        ]

        # Instruction template for consistent prompt formatting
        self.instruction_template = """<|im_start|>system
You are an expert personality analyst specializing in digital communication patterns and behavioral psychology. Your task is to analyze Twitter personalities based on their communication patterns.

Focus on:

1. Communication Style Analysis:
   - Language patterns and word choice
   - Tone variations and emotional expression
   - Interaction patterns with others
   - Platform-specific features usage
   - Content themes and topics

2. Core Personality Traits:
   - Primary motivations and values
   - Decision-making style and thought processes
   - Social interaction preferences
   - Professional identity and interests
   - Risk tolerance and innovation mindset

3. Social Network Analysis:
   - Interaction patterns with mentions
   - Community building approach
   - Influence style and reach
   - Response patterns to different audience segments

4. Professional Insights:
   - Leadership and management style
   - Business philosophy and approach
   - Risk tolerance and decision-making
   - Areas of expertise and passion
   - Growth and learning patterns

Format your analysis in a clear, structured manner with specific examples from the tweets to support your observations.
<|im_end|>

<|im_start|>user
{user_message}
<|im_end|>

<|im_start|>assistant
{assistant_response}
<|im_end|>"""

    def load_analysis(self, filename: str) -> Dict:
        """Load analysis results from file."""
        file_path = os.path.join(self.analysis_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            return {}

    def generate_response(self, system_prompt: str, user_message: str, max_tokens: int = 1000) -> Optional[str]:
        """Generate response using Claude."""
        try:
            # Format the prompt using the instruction template
            formatted_prompt = self.instruction_template.format(
                user_message=user_message,
                assistant_response=""  # Empty for generation
            )
            
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": formatted_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None

    def format_example_tweets(self) -> str:
        """Format example tweets for few-shot prompting."""
        formatted = "Example Twitter Profile Analysis:\n\n"
        formatted += "TOP ENGAGED TWEETS:\n\n"
        
        for i, tweet in enumerate(self.example_tweets, 1):
            formatted += f"{i}. \"{tweet}\"\n\n"
        
        return formatted

    def test_personality_analysis(self, analysis_file: str) -> Optional[str]:
        """Test personality analysis prompt with enhanced analysis capabilities."""
        analysis = self.load_analysis(analysis_file)
        if not analysis:
            return None
            
        print(f"\nPerforming deep personality analysis for {analysis_file}...")
        
        # Combine example tweets with the analysis prompt
        user_message = self.format_example_tweets() + "\n\n" + analysis['personality_prompt']
        
        return self.generate_response(
            system_prompt="Analyze the Twitter personality based on their communication patterns and provide structured insights.",
            user_message=user_message
        )

    def test_all_analyses(self, save_results: bool = True) -> Dict:
        """Test personality analyses for all profiles."""
        results = {}
        os.makedirs(self.test_results_dir, exist_ok=True)
        
        for filename in os.listdir(self.analysis_dir):
            if not filename.startswith('analysis_'):
                continue
                
            print(f"\nAnalyzing profile: {filename}...")
            profile_results = {
                'personality_analysis': self.test_personality_analysis(filename)
            }
            results[filename] = profile_results
            
            if save_results and profile_results['personality_analysis']:
                output_file = os.path.join(self.test_results_dir, f"claude_personality_analysis_{filename}.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(profile_results['personality_analysis'])
                print(f"Analysis results saved to {output_file}")
        
        return results

def main():
    """Main function to run personality analyses."""
    try:
        tester = ClaudeTester()
        results = tester.test_all_analyses()
        print("\nPersonality analysis completed successfully!")
        
        # Print detailed results
        print("\nDetailed Analysis Results:")
        print("=" * 80)
        for filename, profile_results in results.items():
            print(f"\nProfile: {filename}")
            print("-" * 40)
            if profile_results['personality_analysis']:
                print(profile_results['personality_analysis'])
            else:
                print("No analysis results available")
            print("=" * 80)
        
        return results
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return None

if __name__ == "__main__":
    main() 