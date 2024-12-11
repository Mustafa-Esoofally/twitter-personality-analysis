import pandas as pd
import json
from typing import Dict, Any
import os

class PromptGenerator:
    def __init__(self, profile_data: Dict[str, Any], tweets_df: pd.DataFrame):
        """Initialize prompt generator with processed Twitter data.
        
        Args:
            profile_data (Dict): User profile information
            tweets_df (pd.DataFrame): Processed tweets data
        """
        self.profile = profile_data
        self.tweets = tweets_df
        
    def get_top_tweets(self, n: int = 10) -> pd.DataFrame:
        """Get top N tweets by engagement (likes + retweets)."""
        self.tweets['engagement'] = self.tweets['favorite_count'] + self.tweets['retweet_count']
        return self.tweets.nlargest(n, 'engagement')
        
    def generate_personality_prompt(self) -> str:
        """Generate prompt for personality analysis."""
        top_tweets = self.get_top_tweets(10)
        
        prompt = f"""Analyze the Twitter personality of @{self.profile['username']} based on their most engaging tweets.

Profile Information:
- Username: @{self.profile['username']}
- Total Tweets Analyzed: {self.profile['total_tweets']}

Here are their top 10 tweets by engagement:

"""
        for _, tweet in top_tweets.iterrows():
            prompt += f"- Tweet: {tweet['text']}\n"
            prompt += f"  Likes: {tweet['favorite_count']}, Retweets: {tweet['retweet_count']}\n\n"
            
        prompt += """Based on these tweets, provide a detailed personality analysis that includes:
1. Communication style and patterns
2. Key personality traits and characteristics
3. Topics they're most passionate about
4. How they interact with their audience
5. Notable behavioral patterns or quirks

Please provide specific examples from the tweets to support your analysis."""
        
        return prompt
        
    def generate_chat_system_prompt(self) -> str:
        """Generate prompt for chat system personality."""
        top_tweets = self.get_top_tweets(5)
        
        prompt = f"""Create a chat system personality based on @{self.profile['username']}'s Twitter presence.

Sample tweets for personality reference:

"""
        for _, tweet in top_tweets.iterrows():
            prompt += f"- {tweet['text']}\n\n"
            
        prompt += """Design a chat system that captures this personality:

1. Core Personality Traits:
   - Define 3-5 key personality characteristics
   - Explain how each trait should manifest in responses

2. Communication Style:
   - Typical response patterns
   - Common phrases or expressions
   - Tone and attitude

3. Knowledge Domains:
   - Primary topics of expertise
   - Areas of interest
   - How to handle topics outside expertise

4. Interaction Guidelines:
   - How to handle questions
   - Response style to criticism
   - Approach to humor and jokes
   - Boundaries and limitations

Please provide specific examples of how the chat system should respond in different scenarios."""
        
        return prompt
        
    def generate_creative_prompt(self) -> str:
        """Generate prompt for creative analysis."""
        recent_tweets = self.tweets.head(20)
        
        prompt = f"""Create a unique creative analysis of @{self.profile['username']}'s Twitter presence.

Based on these recent tweets:

"""
        for _, tweet in recent_tweets.iterrows():
            prompt += f"- {tweet['text']}\n\n"
            
        prompt += """Choose ONE of the following creative approaches:

1. Write a short story that captures their Twitter personality
2. Create a "day in the life" narrative based on their tweet patterns
3. Design a fictional interview that reveals their character
4. Analyze their tweets as if they were modern poetry
5. Create a sitcom character description based on their online presence

Be creative but ground your analysis in specific examples from their tweets."""
        
        return prompt
        
    def save_prompts(self, output_dir: str) -> None:
        """Save generated prompts to files.
        
        Args:
            output_dir (str): Directory to save prompt files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate and save each prompt type
        prompts = {
            'personality_analysis.txt': self.generate_personality_prompt(),
            'chat_system.txt': self.generate_chat_system_prompt(),
            'creative_analysis.txt': self.generate_creative_prompt()
        }
        
        for filename, prompt in prompts.items():
            with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(prompt) 