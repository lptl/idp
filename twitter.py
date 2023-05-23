import os
import sys
from typing import List
import pandas as pd
import snscrape.modules.twitter as sntwitter

def get_search_result(query_content: str) -> List:
    scraper = sntwitter.TwitterSearchScraper(query_content)
    return scraper.get_items()

def get_user_tweets(username: str, max_tweets_num: int) -> List:
    try:
        # the alternative is the profile page, which includes retweets but it 
        # only returns about 3200 tweets. So the best you can do is use the 
        # twitter-profile scraper to at least discover all retweets among the 
        # user's 3200 most recent tweets. 
        profile_scraper = sntwitter.TwitterProfileScraper(username)
        user_scraper = sntwitter.TwitterUserScraper(username)
    except ValueError:
        print(f"User {username} not found")
        return []
    tweets = []
    profile_tweets_length = min(3200, max_tweets_num) if max_tweets_num is not None else 3200
    for profile_tweet in profile_scraper.get_items():
        if len(tweets) >= profile_tweets_length:
            break
        tweets.append(profile_tweet)
    user_tweets_length = max_tweets_num - len(tweets) if max_tweets_num is not None else None
    for user_tweet in user_scraper.get_items():
        if user_tweets_length is not None and len(tweets) >= user_tweets_length:
            return tweets
        tweets.append(user_tweet)
    return tweets

def get_tweet_text(tweets, length_range: List[int]):
    texts = []
    for tweet in tweets:
        raw_content = tweet.rawContent
        print(raw_content, len(raw_content.split()))
        if length_range is not None:
            words_count = len(raw_content.split())
            if words_count >= length_range[0] and words_count <= length_range[1]:
                texts.append(raw_content)
        else: texts.append(raw_content)
    return texts

def get_user(username: str):
    scraper = sntwitter.TwitterUserScraper(username)
    return scraper._get_entity()

def read_csv_file(filename: str, filter_columns: List[str]) -> pd.DataFrame:
    if not os.path.exists(filename):
        print('File not found: {}'.format(filename))
        sys.exit(1)
    raw_data = pd.read_csv(filename)
    filtered_data = raw_data[filter_columns] if filter_columns is not None else raw_data
    return filtered_data

def write_to_csv_file(data_frame: pd.DataFrame, filename: str) -> None:
    data_frame.to_csv(filename, index=False)

if __name__ == '__main__':
    csv_file_name = '../founders_dataset_IDP.csv'
    filter_columns = ['legal_name', 'domain', 'person_name', 'gender', 'facebook_url', 'linkedin_url', 'twitter_url']
    data_frame = read_csv_file(csv_file_name, filter_columns)
    max_search_users = 10
    for index, row in data_frame.iterrows():
        if index >= max_search_users:
            break
        if pd.isna(row['twitter_url']): 
            print(f"Skipping {row['person_name']}'s twitter as there is no twitter link")
            continue
        twitter_user_name = row['twitter_url'].split('/')[-1]
        tweets = get_user_tweets(twitter_user_name, 100)
        texts = get_tweet_text(tweets, [20, 200])
        # here append the scraping result of lindkedin and facebook
        write_to_csv_file(pd.DataFrame(texts), ''.join(row['person_name'].split(' ')) + '.csv')