import json
from typing import Dict, List

class PromptTemplates:
    @staticmethod
    def personality_analysis_template() -> str:
        """Template for generating personality analysis from Twitter data."""
        return '''You are a skilled psychologist and social media analyst. Analyze the following Twitter profile data to create a detailed personality assessment.

Profile Information:
{profile_info}

Tweet Analysis:
- Total Tweets Analyzed: {total_tweets}
- Average Engagement: {engagement_metrics}
- Top Tweets:
{top_tweets}

Based on this data, provide:
1. Core Personality Traits
2. Communication Style
3. Key Interests and Values
4. Behavioral Patterns
5. Social Interaction Style
6. Notable Quirks or Unique Characteristics

Format your analysis in a clear, insightful manner that captures the essence of the person behind these tweets.'''

    @staticmethod
    def chatbot_system_prompt_template() -> str:
        """Template for generating chatbot system prompts based on personality analysis."""
        return '''You are tasked with creating a system prompt that will make an AI chatbot embody the personality of the following Twitter user.

Personality Analysis:
{personality_analysis}

Key Behavioral Metrics:
{behavioral_metrics}

Create a system prompt that:
1. Defines the core personality and behavioral traits
2. Establishes the communication style and tone
3. Sets appropriate behavioral boundaries
4. Includes typical response patterns
5. Specifies how to handle different types of interactions

The prompt should make the AI chatbot authentically represent the analyzed personality while maintaining appropriate ethical boundaries.'''

    @staticmethod
    def creative_analysis_template() -> str:
        """Template for generating creative analysis outputs."""
        return '''Analyze the following Twitter profile from a unique creative perspective.

Profile Data:
{profile_data}

Tweet Patterns:
{tweet_patterns}

Create one of the following creative outputs:
1. A "day in the life" narrative that captures their typical thought patterns
2. A sitcom episode outline based on their tweet style and interests
3. A psychological profile written in their own tweeting style
4. An "alternate universe" version of their personality
5. A "brand guide" for their personal communication style

Choose the most fitting creative format based on the data and produce an engaging, insightful piece that captures their essence.'''

    @staticmethod
    def format_profile_data(profile_data: Dict) -> str:
        """Format profile data for use in templates."""
        return f"""Username: {profile_data.get('username', 'N/A')}
Name: {profile_data.get('name', 'N/A')}
Description: {profile_data.get('description', 'N/A')}
Followers: {profile_data.get('followers_count', 'N/A')}
Following: {profile_data.get('following_count', 'N/A')}"""

    @staticmethod
    def format_tweet_metrics(metrics: Dict) -> str:
        """Format tweet metrics for use in templates."""
        return f"""Total Tweets: {metrics.get('total_tweets', 0)}
Average Likes: {metrics.get('avg_likes', 0):.2f}
Average Retweets: {metrics.get('avg_retweets', 0):.2f}"""

    @staticmethod
    def format_top_tweets(tweets: List[Dict], limit: int = 5) -> str:
        """Format top tweets for use in templates."""
        formatted_tweets = []
        for i, tweet in enumerate(tweets[:limit], 1):
            formatted_tweets.append(
                f"{i}. \"{tweet['text']}\"\n"
                f"   Likes: {tweet['favorite_count']}, "
                f"Retweets: {tweet['retweet_count']}"
            )
        return "\n".join(formatted_tweets)

    def generate_personality_prompt(self, profile_data: Dict, metrics: Dict, top_tweets: List[Dict]) -> str:
        """Generate a complete personality analysis prompt."""
        return self.personality_analysis_template().format(
            profile_info=self.format_profile_data(profile_data),
            total_tweets=metrics['total_tweets'],
            engagement_metrics=self.format_tweet_metrics(metrics),
            top_tweets=self.format_top_tweets(top_tweets)
        )

    def generate_chatbot_prompt(self, personality_analysis: str, metrics: Dict) -> str:
        """Generate a complete chatbot system prompt."""
        return self.chatbot_system_prompt_template().format(
            personality_analysis=personality_analysis,
            behavioral_metrics=self.format_tweet_metrics(metrics)
        )

    def generate_creative_prompt(self, profile_data: Dict, tweet_patterns: Dict) -> str:
        """Generate a complete creative analysis prompt."""
        return self.creative_analysis_template().format(
            profile_data=self.format_profile_data(profile_data),
            tweet_patterns=json.dumps(tweet_patterns, indent=2)
        ) 