import json
import os
from typing import Dict, List
from datetime import datetime
import argparse

def load_tweets(file_path: str) -> List[Dict]:
    """Load tweets from the raw data file."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        print(f"Current working directory: {os.getcwd()}")
        return []

    print(f"File found at {file_path}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    try:
        # Read the file in chunks to handle large files
        chunk_size = 1024 * 1024  # 1MB chunks
        json_data = ""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                json_data += chunk
        
        # Clean up any potential formatting issues
        json_data = json_data.strip()
        
        # Split content at points where new JSON objects begin
        json_parts = json_data.split('{"data":')
        json_parts = [part for part in json_parts if part.strip()]
        
        print(f"\nFound {len(json_parts)} potential JSON objects")
        
        all_tweets = []
        for i, part in enumerate(json_parts, 1):
            try:
                # Reconstruct the JSON object
                if not part.startswith('{'):
                    part = '{"data":' + part
                
                data = json.loads(part)
                
                if isinstance(data, dict) and 'data' in data and 'items' in data['data']:
                    tweets = data['data']['items']
                    all_tweets.extend(tweets)
                    print(f"Successfully parsed part {i}, found {len(tweets)} tweets")
                else:
                    print(f"Skipping part {i}: unexpected structure")
                    
            except json.JSONDecodeError as je:
                print(f"Error parsing part {i}: {je.msg}")
                continue
            except Exception as e:
                print(f"Unexpected error in part {i}: {str(e)}")
                continue
        
        print(f"\nTotal tweets loaded: {len(all_tweets)}")
        return all_tweets
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []

def extract_profile_data(tweets: List[Dict]) -> Dict[str, Dict]:
    """Extract relevant profile information from tweets."""
    profiles = {}
    
    for tweet in tweets:
        author_id = tweet.get('author_id')
        author_username = tweet.get('author_username')
        
        if not author_id or not author_username:
            continue
        
        if author_id not in profiles:
            profiles[author_id] = {
                'username': author_username,
                'tweets': [],
                'total_favorites': 0,
                'total_retweets': 0,
                'total_replies': 0,
                'total_quotes': 0,
                'total_views': 0
            }
        
        # Add tweet data
        tweet_data = {
            'id': tweet.get('id', ''),
            'text': tweet.get('text', ''),
            'created_time': tweet.get('created_time', ''),
            'favorite_count': tweet.get('favorite_count', 0),
            'retweet_count': tweet.get('retweet_count', 0),
            'reply_count': tweet.get('reply_count', 0),
            'quote_count': tweet.get('quote_count', 0),
            'view_count': tweet.get('view_count', 0),
            'source': tweet.get('source', ''),
            'post_type': tweet.get('post_type', ''),
            'hashtags': tweet.get('text_tags', []) or [],
            'mentioned_users': tweet.get('text_tagged_users', []) or [],
            'media_urls': tweet.get('attached_medias_url', []) or [],
            'video_urls': [v.get('url', '') for v in (tweet.get('attached_videos') or []) if v and v.get('url')]
        }
        
        # Update profile metrics
        profiles[author_id]['total_favorites'] += tweet_data['favorite_count']
        profiles[author_id]['total_retweets'] += tweet_data['retweet_count']
        profiles[author_id]['total_replies'] += tweet_data['reply_count']
        profiles[author_id]['total_quotes'] += tweet_data['quote_count']
        profiles[author_id]['total_views'] += tweet_data['view_count']
        
        profiles[author_id]['tweets'].append(tweet_data)
    
    return profiles

def save_processed_data(profiles: Dict[str, Dict], output_file: str):
    """Save the processed data to a JSON file."""
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

def process_tweets(username: str, input_file: str = None, output_file: str = None):
    """Process tweets for a specific username."""
    # Set default file paths if not provided
    if input_file is None:
        input_file = f'data/raw/{username}_tweets.txt'
    if output_file is None:
        output_file = f'data/processed/{username}_profile.json'
    
    print(f"Starting processing at {datetime.now()}")
    print(f"Processing tweets for @{username}")
    print(f"Loading tweets from {input_file}...")
    
    tweets = load_tweets(input_file)
    
    if not tweets:
        print("No tweets were loaded. Please check the input file.")
        return
    
    print("Processing profiles...")
    profiles = extract_profile_data(tweets)
    
    if not profiles:
        print("No profiles were extracted from the tweets.")
        return
    
    print(f"Saving processed data to {output_file}...")
    save_processed_data(profiles, output_file)
    
    print(f"Processing complete at {datetime.now()}")
    print(f"Found {len(profiles)} unique profiles")
    print(f"Total tweets processed: {sum(len(p['tweets']) for p in profiles.values())}")
    
    return profiles

def main():
    parser = argparse.ArgumentParser(description='Process Twitter data for a specific user')
    parser.add_argument('username', help='Twitter username to process')
    parser.add_argument('--input', help='Input file path (optional)')
    parser.add_argument('--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    process_tweets(args.username, args.input, args.output)

if __name__ == '__main__':
    main() 