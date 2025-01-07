from typing import Dict, List, Optional
import json
import os
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TweetMetrics:
    engagement_score: float
    retweet_count: int
    favorite_count: int
    has_media: bool
    has_links: bool
    has_mentions: bool
    length: int

class TweetExtractor:
    def __init__(self, data_dir: str = "processed_data"):
        self.data_dir = data_dir
        self.output_dir = "curated_tweets"
        os.makedirs(self.output_dir, exist_ok=True)

    def calculate_engagement_score(self, tweet: Dict) -> float:
        """Calculate engagement score based on likes and retweets."""
        return (tweet.get('favorite_count', 0) * 1.0 + 
                tweet.get('retweet_count', 0) * 2.0)  # Weigh retweets more

    def get_tweet_metrics(self, tweet: Dict) -> TweetMetrics:
        """Extract metrics from a tweet."""
        text = tweet.get('text', '')
        return TweetMetrics(
            engagement_score=self.calculate_engagement_score(tweet),
            retweet_count=tweet.get('retweet_count', 0),
            favorite_count=tweet.get('favorite_count', 0),
            has_media='media' in tweet,
            has_links='http' in text.lower(),
            has_mentions=len(tweet.get('mentions', [])) > 0,
            length=len(text)
        )

    def select_relevant_tweets(self, tweets: List[Dict], limit: int = 50) -> List[Dict]:
        """Select most relevant tweets based on engagement and content."""
        # Add metrics to tweets
        tweets_with_metrics = []
        for tweet in tweets:
            if not tweet.get('text'):
                continue
                
            metrics = self.get_tweet_metrics(tweet)
            tweets_with_metrics.append({
                'tweet': tweet,
                'metrics': metrics
            })

        # Sort by engagement score
        tweets_with_metrics.sort(
            key=lambda x: x['metrics'].engagement_score,
            reverse=True
        )

        # Select diverse high-engagement tweets
        selected_tweets = []
        seen_patterns = set()
        
        for tweet_data in tweets_with_metrics:
            tweet = tweet_data['tweet']
            text = tweet['text'].lower()
            
            # Skip very similar tweets
            text_pattern = ''.join(sorted(text.split()))
            if text_pattern in seen_patterns:
                continue
            
            seen_patterns.add(text_pattern)
            selected_tweets.append(tweet)
            
            if len(selected_tweets) >= limit:
                break

        return selected_tweets

    def extract_and_save(self, filename: str) -> Optional[Dict]:
        """Extract relevant tweets and save to curated file."""
        try:
            # Load processed data
            input_path = os.path.join(self.data_dir, filename)
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Select relevant tweets
            relevant_tweets = self.select_relevant_tweets(data.get('tweets', []))

            # Prepare curated data
            curated_data = {
                'profile': data.get('profile', {}),
                'relevant_tweets': relevant_tweets,
                'metadata': {
                    'total_tweets_analyzed': len(data.get('tweets', [])),
                    'selected_tweets': len(relevant_tweets),
                    'extraction_date': datetime.now().isoformat()
                }
            }

            # Save curated data
            output_filename = f"curated_{os.path.basename(filename)}"
            output_path = os.path.join(self.output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(curated_data, f, indent=2, ensure_ascii=False)

            return curated_data

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            return None

def main():
    extractor = TweetExtractor()
    
    # Process all files in the processed_data directory
    for filename in os.listdir(extractor.data_dir):
        if filename.startswith('processed_') and filename.endswith('.json'):
            print(f"Extracting relevant tweets from {filename}...")
            result = extractor.extract_and_save(filename)
            
            if result:
                print(f"Successfully extracted {len(result['relevant_tweets'])} relevant tweets")
            else:
                print(f"Failed to process {filename}")

if __name__ == "__main__":
    main() 