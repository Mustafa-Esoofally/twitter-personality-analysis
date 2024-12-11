import json
import os
from typing import Dict, List, Any
import pandas as pd
from src.utils.config import DATA_DIR

class TwitterDataProcessor:
    def __init__(self, raw_data_path: str):
        """Initialize the Twitter data processor.
        
        Args:
            raw_data_path (str): Path to the raw Twitter JSON data
        """
        self.raw_data_path = raw_data_path
        self.processed_data = None

    def load_raw_data(self) -> Dict[str, Any]:
        """Load raw Twitter JSON data."""
        with open(self.raw_data_path, 'r', encoding='utf-8') as f:
            # Read the file content
            content = f.read()
            
            # Split into individual JSON objects if multiple exist
            json_objects = content.split('{"data":')
            json_objects = [obj for obj in json_objects if obj.strip()]
            
            # Process each JSON object
            all_items = []
            for obj in json_objects:
                if not obj.startswith('{'):
                    obj = '{"data":' + obj
                try:
                    data = json.loads(obj)
                    if 'data' in data and 'items' in data['data']:
                        all_items.extend(data['data']['items'])
                except json.JSONDecodeError:
                    continue
            
            # Get the first tweet for profile info
            first_tweet = all_items[0] if all_items else {}
            
            return {
                'items': all_items,
                'profile': {
                    'username': first_tweet.get('author_username'),
                    'name': first_tweet.get('author_name', first_tweet.get('author_username', 'Unknown')),
                    'description': first_tweet.get('author_description', ''),
                    'followers_count': first_tweet.get('author_followers_count', 0),
                    'friends_count': first_tweet.get('author_friends_count', 0),
                    'total_tweets': len(all_items)
                }
            }

    def clean_tweet_data(self, tweets: List[Dict[str, Any]]) -> pd.DataFrame:
        """Clean and structure tweet data.
        
        Args:
            tweets (List[Dict]): List of raw tweet dictionaries
            
        Returns:
            pd.DataFrame: Cleaned tweet data
        """
        cleaned_tweets = []
        for tweet in tweets:
            cleaned_tweet = {
                'id': tweet.get('id'),
                'text': tweet.get('text', ''),
                'created_time': tweet.get('created_time'),
                'favorite_count': tweet.get('favorite_count', 0),
                'retweet_count': tweet.get('retweet_count', 0),
                'reply_count': tweet.get('reply_count', 0),
                'quote_count': tweet.get('quote_count', 0),
                'view_count': tweet.get('view_count', 0),
                'post_type': tweet.get('post_type', ''),
                'source': tweet.get('source', ''),
                'text_lang': tweet.get('text_lang', ''),
                'attached_media': tweet.get('attached_medias_url', []),
                'attached_links': tweet.get('attached_links_expanded_url', []),
                'is_reply': tweet.get('in_reply_to_post_id') is not None,
                'is_quote': tweet.get('quoted_status_id') is not None,
                'is_retweet': False  # No retweet info in this format
            }
            cleaned_tweets.append(cleaned_tweet)
        
        return pd.DataFrame(cleaned_tweets)

    def process_data(self) -> None:
        """Process the raw Twitter data into structured format."""
        raw_data = self.load_raw_data()
        tweets = raw_data.get('items', [])
        
        # Process tweets
        tweets_df = self.clean_tweet_data(tweets)
        
        self.processed_data = {
            'profile': raw_data['profile'],
            'tweets': tweets_df
        }

    def save_processed_data(self, output_dir: str) -> None:
        """Save processed data to files.
        
        Args:
            output_dir (str): Directory to save processed data
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Run process_data() first.")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save profile data
        profile_path = os.path.join(output_dir, 'profile_data.json')
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(self.processed_data['profile'], f, indent=2)
        
        # Save tweets data
        tweets_path = os.path.join(output_dir, 'tweets_data.csv')
        self.processed_data['tweets'].to_csv(tweets_path, index=False)

def main():
    """Main function to process Twitter data."""
    # Process raw data files
    raw_data_dir = os.path.join(DATA_DIR, 'raw')
    processed_data_dir = os.path.join(DATA_DIR, 'processed')
    
    for filename in os.listdir(raw_data_dir):
        if filename.endswith('.json'):
            print(f"Processing {filename}...")
            processor = TwitterDataProcessor(os.path.join(raw_data_dir, filename))
            processor.process_data()
            
            # Create user-specific directory for processed data
            user_dir = os.path.join(processed_data_dir, filename.replace('.json', ''))
            processor.save_processed_data(user_dir)
            print(f"Processed data saved to {user_dir}")

if __name__ == "__main__":
    main() 