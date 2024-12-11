import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import re
from collections import Counter

class PersonalityAnalyzer:
    def __init__(self, profile_data: Dict):
        self.profile_data = profile_data
        self.username = profile_data['username']
        self.tweets = profile_data['tweets']
        self.analytics = profile_data.get('analytics', {})
        self._process_tweets()
    
    def _process_tweets(self):
        """Extract key patterns and metrics from tweets for analysis."""
        self.common_topics = []
        self.response_patterns = []
        self.interaction_style = []
        
        # Analyze tweet patterns
        all_text = " ".join([t['text'] for t in self.tweets])
        
        # Identify common phrases and patterns
        self.uses_emojis = bool(re.search(r'[\U0001F300-\U0001F9FF]', all_text))
        self.uses_memes = len([t for t in self.tweets if 'media_urls' in t and t['media_urls']]) / len(self.tweets)
        self.avg_tweet_length = sum(len(t['text']) for t in self.tweets) / len(self.tweets)
        
        # Get top engaging tweets for reference
        self.top_tweets = sorted(self.tweets, key=lambda x: x['favorite_count'], reverse=True)[:5]
        
        # Analyze interaction patterns
        self.reply_rate = len([t for t in self.tweets if t.get('in_reply_to_profile_id')]) / len(self.tweets)
        
        # Extract common words and phrases
        words = re.findall(r'\b\w+\b', all_text.lower())
        self.common_words = Counter(words).most_common(20)
    
    def generate_psychoanalysis_prompt(self) -> str:
        """Generate a prompt for personality psychoanalysis."""
        prompt = f"""Analyze the Twitter personality of @{self.username} based on the following data:

Key Metrics:
- Average engagement: {self.analytics.get('avg_favorites', 0):,.0f} favorites, {self.analytics.get('avg_retweets', 0):,.0f} retweets
- Tweet style: {'Uses emojis, ' if self.uses_emojis else ''}{'Heavy meme user' if self.uses_memes > 0.2 else 'Limited meme use'}
- Average tweet length: {self.avg_tweet_length:.0f} characters
- Reply rate: {self.reply_rate*100:.1f}% of tweets are replies

Most Popular Tweets:
{self._format_top_tweets()}

Common Topics & Language:
{', '.join(word for word, count in self.common_words[:10])}

Based on this data, provide a casual but insightful psychoanalysis that:
1. Identifies core personality traits and quirks
2. Analyzes their communication style and social dynamics
3. Highlights unique behavioral patterns
4. Speculates about their motivations and insecurities
5. Discusses how they present themselves versus potential underlying traits

Write in an entertaining, accessible style while maintaining psychological depth. Include specific examples from their tweets to support your analysis."""
        return prompt
    
    def generate_chat_system_prompt(self) -> str:
        """Generate a system prompt for a chat model to emulate the personality."""
        prompt = f"""You are a chat AI that embodies the Twitter personality of @{self.username}. Your responses should reflect the following characteristics:

Communication Style:
- Tweet length: Typically uses {self.avg_tweet_length:.0f} characters
- Engagement style: {'Highly responsive' if self.reply_rate > 0.3 else 'Selective in responses'}
- Language: {self._get_language_style()}

Behavioral Guidelines:
1. Match their response patterns: {self._get_response_patterns()}
2. Use similar language patterns and common phrases
3. Maintain consistent opinions and viewpoints
4. Reflect their interaction style: {self._get_interaction_style()}

Example Interactions (based on high-engagement tweets):
{self._format_interaction_examples()}

Boundaries:
1. Stay within their established topic areas and interests
2. Maintain their typical emotional range and reaction patterns
3. Use similar humor style and meme references
4. Preserve their unique quirks while avoiding caricature

Your goal is to provide responses that feel authentic to their personality while maintaining appropriate boundaries and ethical considerations."""
        return prompt
    
    def generate_creative_analysis(self, analysis_type: str = "insecurity") -> str:
        """Generate a creative analysis prompt based on the specified type."""
        if analysis_type == "insecurity":
            prompt = f"""Analyze @{self.username}'s potential insecurities based on their Twitter behavior:

Engagement Patterns:
- Response rate to criticism: {self._analyze_criticism_response()}
- Self-reference frequency: {self._analyze_self_references()}
- Defensive patterns: {self._analyze_defensive_patterns()}

Popular Tweet Themes:
{self._format_top_tweets(include_analysis=True)}

Consider:
1. What drives their need for engagement?
2. How do they handle criticism and praise?
3. What patterns emerge in their self-presentation?
4. What compensatory behaviors are visible?
5. How does their public persona relate to potential private concerns?

Provide an insightful analysis that's respectful while being honest about observed patterns."""
        else:
            prompt = "Unsupported analysis type"
        return prompt
    
    def _format_top_tweets(self, include_analysis: bool = False) -> str:
        """Format top tweets for prompt inclusion."""
        result = ""
        for i, tweet in enumerate(self.top_tweets[:3], 1):
            result += f"{i}. \"{tweet['text'][:100]}...\"\n"
            result += f"   Engagement: {tweet['favorite_count']:,} favorites, {tweet['view_count']:,} views\n"
            if include_analysis:
                result += f"   Tone: {self._analyze_tweet_tone(tweet)}\n"
        return result
    
    def _get_language_style(self) -> str:
        """Analyze and describe language style."""
        style = []
        if self.uses_emojis:
            style.append("Frequent emoji use")
        if self.uses_memes > 0.2:
            style.append("Heavy meme references")
        if self.avg_tweet_length < 100:
            style.append("Concise")
        elif self.avg_tweet_length > 200:
            style.append("Verbose")
        return ", ".join(style) or "Standard communication style"
    
    def _get_response_patterns(self) -> str:
        """Analyze typical response patterns."""
        patterns = []
        if self.reply_rate > 0.3:
            patterns.append("Highly interactive")
        if self.uses_memes > 0.2:
            patterns.append("Often responds with memes")
        return ", ".join(patterns) or "Standard response patterns"
    
    def _get_interaction_style(self) -> str:
        """Analyze interaction style."""
        style = []
        if self.reply_rate > 0.3:
            style.append("Engaged with community")
        if self.avg_tweet_length < 100:
            style.append("Quick, punchy responses")
        return ", ".join(style) or "Balanced interaction style"
    
    def _format_interaction_examples(self) -> str:
        """Format example interactions based on popular tweets."""
        examples = ""
        for tweet in self.top_tweets[:2]:
            examples += f"User: [Relevant topic]\n"
            examples += f"{self.username}: {tweet['text'][:100]}...\n\n"
        return examples
    
    def _analyze_criticism_response(self) -> str:
        """Analyze how they respond to criticism."""
        # This would need more sophisticated analysis
        return "Analysis requires more detailed interaction data"
    
    def _analyze_self_references(self) -> str:
        """Analyze frequency of self-references."""
        self_refs = sum(1 for t in self.tweets if re.search(r'\bI\b|\bme\b|\bmy\b', t['text'], re.IGNORECASE))
        rate = self_refs / len(self.tweets)
        return f"{rate*100:.1f}% of tweets contain self-references"
    
    def _analyze_defensive_patterns(self) -> str:
        """Analyze defensive communication patterns."""
        # This would need more sophisticated analysis
        return "Analysis requires more detailed interaction data"
    
    def _analyze_tweet_tone(self, tweet: Dict) -> str:
        """Analyze the tone of a tweet."""
        # Simple tone analysis based on basic patterns
        text = tweet['text'].lower()
        if '!' in text:
            return "Enthusiastic"
        elif '?' in text:
            return "Inquisitive"
        elif any(word in text for word in ['should', 'must', 'need']):
            return "Assertive"
        return "Neutral"

def load_profile(username: str) -> Optional[Dict]:
    """Load profile data from processed JSON file."""
    try:
        filepath = f"data/processed/{username}_profile.json"
        print(f"Attempting to load profile from: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Successfully loaded JSON data")
            # Get the first (and should be only) user data from the dictionary
            user_id, user_data = next(iter(data.items()))
            print(f"Found user data for ID: {user_id}")
            return user_data
    except Exception as e:
        print(f"Error loading profile: {str(e)}")
        return None

def main():
    # Example usage
    username = "elonmusk"  # or any other username in your dataset
    profile_data = load_profile(username)
    
    if profile_data:
        analyzer = PersonalityAnalyzer(profile_data)
        
        print("\nGenerating Personality Psychoanalysis Prompt...")
        print("=" * 80)
        print(analyzer.generate_psychoanalysis_prompt())
        
        print("\nGenerating Chat System Prompt...")
        print("=" * 80)
        print(analyzer.generate_chat_system_prompt())
        
        print("\nGenerating Insecurity Analysis Prompt...")
        print("=" * 80)
        print(analyzer.generate_creative_analysis("insecurity"))

if __name__ == '__main__':
    main() 