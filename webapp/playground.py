import pickle
import re

import emoji
import numpy as np
import pandas as pd
import requests
import twitter
import yaml

import text_classifier

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
  # TODO: Consider wrapping the necessary code in a try, 
  # in case the data that is returned is not as expected and you get an exception    
    
  ellipsis_unicode = '\u2026'     
  retweet_abbreviation = 'RT'
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
          full_tweet = retweeted_tweets[retweeted_tweet_id]
        else:
          for referenced_tweet in response_json['includes']['tweets']:
            if referenced_tweet['id'] == retweeted_tweet_id:
              full_tweet = referenced_tweet['text']
              retweeted_tweets[retweeted_tweet_id] = full_tweet
              break        
        tweet['text'] = full_tweet      
    remove_html_character_entities(tweet)
    remove_urls(tweet)
    remove_emoji(tweet)
    remove_at_mentions(tweet)    

def main():                                
  max_results = 10 # CAREFUL!
  topic = 'covid'
  response_json = get_tweet_data(topic, max_results)      
  if 'data' in response_json:
    response_json['data'] = ([tweet for tweet in response_json['data'] 
                              if tweet['lang'] == "en" 
                              or tweet['lang'] == "en-gb"])
  else:
    # TODO: write this case
    pass   
  process_tweets(response_json) 
  tweets = []
  for tweet in response_json['data']:
    tweets.append(tweet['text'])
  print(f"Number of tweets: {len(tweets)}\n") # TODO: remove
  for index, tweet in enumerate(tweets): # TODO: remove
    print(f"Tweet: {index}\n{tweet}\n") # TODO: remove
  with open('classifier.pkl', 'rb') as f:
    classifier = pickle.load(f)
  predictions = classifier.predict(pd.DataFrame(tweets).to_numpy())
  print(f"Predictions: {predictions}")    # TODO: remove

def test_modification_function(tweet):
  tweet['text'] = re.sub(r'www\.\S+|https?://\S+', '', tweet['text'])

def process(my_dict):
  print("Before processing:\n")
  for tweet in my_dict['data']:
    print(tweet["text"])
    test_modification_function(tweet)
    print(tweet["text"], '\n')

def test():
  my_dict = {"data":[{"text": "My tweet! https://mytweet.com"}, 
                     {"text": "My other tweet! https://myothertweet.com"}]}

  print(my_dict)
  process_tweets(my_dict)
  print("After processing:\n")
  for tweet in my_dict['data']:    
    print(tweet["text"], '\n')
  

if __name__ == "__main__":  
  #test()
  main()