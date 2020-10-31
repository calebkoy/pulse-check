import pickle
import re

import emoji
import numpy as np
import pandas as pd
import requests
import twitter
import yaml

import text_classifier
from sentiment import Sentiment

def process_yaml():
  with open("config.yaml") as file:
    return yaml.safe_load(file)

def create_bearer_token(data):
  return data["search_tweets_api"]["bearer_token"]

def make_request(bearer_token, url):
  headers = {"Authorization": "Bearer {}".format(bearer_token)}
  response = requests.request("GET", url, headers=headers)
  return response.json()

def get_tweet_data(topic, max_results):  
  base_url = 'https://api.twitter.com/2/tweets/search/recent'  
  parameters = f'query={topic}&tweet.fields=created_at,lang&max_results={max_results}&expansions=referenced_tweets.id'
  endpoint_url = f'{base_url}?{parameters}'    
  bearer_token = create_bearer_token(process_yaml())
  return make_request(bearer_token, endpoint_url)

def remove_html_character_entities(tweet):
  tweet['text'] = re.sub(r'&[a-zA-Z]+;', '', tweet['text'])

def remove_urls(tweet):
  tweet['text'] = re.sub(r'www\.\S+|https?://\S+', '', tweet['text'])

def remove_emoji(tweet):
  tweet['text'] = emoji.get_emoji_regexp().sub(u'', tweet['text'])

def remove_at_mentions(tweet):
  tweet['text'] = re.sub(r'@\S+', '', tweet['text'])

def process_tweets(response_json):      
  ellipsis_unicode = '\u2026'     
  retweet_abbreviation = 'RT'
  quote_tweet_abbreviation = 'QT'
  retweeted_tweets = {}
  for tweet in response_json['data']:                        
    if tweet['text'].startswith(retweet_abbreviation):
      tweet['text'] = tweet['text'][2:]
      if tweet['text'].endswith(ellipsis_unicode):                  
        for tweet_reference in tweet['referenced_tweets']:
          if tweet_reference['type'] == 'retweeted':
            retweeted_tweet_id = tweet_reference['id']
            break                              
        if retweeted_tweet_id in retweeted_tweets:
          tweet['text'] = retweeted_tweets[retweeted_tweet_id]
        elif 'includes' in response_json:
          for referenced_tweet in response_json['includes']['tweets']:
            if referenced_tweet['id'] == retweeted_tweet_id:
              full_tweet = referenced_tweet['text']
              retweeted_tweets[retweeted_tweet_id] = full_tweet
              tweet['text'] = full_tweet
              break                      
    if tweet['text'].startswith(quote_tweet_abbreviation):
      tweet['text'] = tweet['text'][2:]
    remove_urls(tweet)
    remove_html_character_entities(tweet)    
    remove_emoji(tweet)
    remove_at_mentions(tweet)

def main():                                
  max_results = 10 # CAREFUL!
  topic = 'naive 10'
  response_json = get_tweet_data(topic, max_results)      
  print(response_json)
  if 'data' in response_json:
    response_json['data'] = ([tweet for tweet in response_json['data'] 
                              if tweet['lang'] == "en" 
                              or tweet['lang'] == "en-gb"])
    
    process_tweets(response_json) 
    tweets = []
    tweet_ids = []
    for tweet in response_json['data']:
      tweets.append(tweet['text'])    
      tweet_ids.append(tweet['id'])
    for tweet in tweets:
      print(tweet)
    tweet_ids = np.array(tweet_ids)
    with open('classifier.pkl', 'rb') as f:
      classifier = pickle.load(f)
    predictions = classifier.predict(pd.DataFrame(tweets).to_numpy())
    print(f"Predictions: {predictions}\n")    # TODO: remove  
    
    positive_indices = np.asarray(predictions == Sentiment.POSITIVE.value).nonzero()
    #neutral_indices = np.asarray(predictions == Sentiment.NEUTRAL.value).nonzero()
    negative_indices = np.asarray(predictions == Sentiment.NEGATIVE.value).nonzero()
    positive_tweet_ids = tweet_ids[positive_indices]
    #neutral_tweet_ids = tweet_ids[neutral_indices]
    negative_tweet_ids = tweet_ids[negative_indices]
    print(f"Positive tweet indices:\n{positive_indices}\n")
    print(f"Positive tweet IDs:\n{positive_tweet_ids}\n\n")
    #print(f"Neutral tweet indices:\n{neutral_indices}\n")
    #print(f"Neutral tweet IDs:\n{neutral_tweet_ids}\n\n")
    print(f"Negative tweet indices:\n{negative_indices}\n")
    print(f"Negative tweet IDs:\n{negative_tweet_ids}\n\n")
  else:
    # TODO: write this case
    # Consider checking for any error, interpreting them if possible 
    # and returning a helpful message to the user
    pass       

if __name__ == "__main__":    
  main()