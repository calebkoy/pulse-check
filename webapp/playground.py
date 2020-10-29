import copy
import json
import re

import emoji
import nltk
import requests
import twitter
import yaml

def process_yaml():
  with open("config.yaml") as file:
    return yaml.safe_load(file)

def create_bearer_token(data):
  return data["search_tweets_api"]["bearer_token"]

def make_request(bearer_token, url):
  headers = {"Authorization": "Bearer {}".format(bearer_token)}
  response = requests.request("GET", url, headers=headers)
  return response.json()

def get_tweets(topic, max_results):  
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
    remove_html_character_entities(tweet)
    remove_urls(tweet)
    remove_emoji(tweet)
    remove_at_mentions(tweet)
    if (tweet['text'].endswith(ellipsis_unicode) 
        and tweet['text'].startswith(retweet_abbreviation)):        
      
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
      tweet['full_text'] = full_tweet
      tweet['text'] = tweet['text'][2:]

def main():                              
  text = 'a a a the the the the other words'
  freq_dist = nltk.FreqDist(text)
  print(freq_dist.keys())
  pass
  # with open('response-11.json', 'r') as f:
  #   response_json = json.load(f)
  #   for tweet in response_json['data']:
  #     tweet['text'] = re.sub(r'@\S+', '', tweet['text'])
  #   with open('response-11-no-at-mentions.json', 'w', encoding='utf-8') as f2:
  #     json.dump(response_json, f2, indent=2)

  
  #pass
  # max_results = 10 # CAREFUL!
  # topic = 'covid'
  # response_json = get_tweets(topic, max_results)    
    
  # if 'data' in response_json: 
  #   response_json['data'] = ([tweet for tweet in response_json['data'] 
  #                             if tweet['lang'] == "en" 
  #                             or tweet['lang'] == "en-gb"])              
  
  # id = '11'
  
  # with open(f'response-{id}-ensure-ascii-false.json', 'w', encoding='utf-8') as f:
  #   json.dump(response_json, f, ensure_ascii=False, indent=2)  
  # with open(f'response-{id}.json', 'w', encoding='utf-8') as f:
  #   json.dump(response_json, f, indent=2)  
  
  # process_tweets(response_json)            

  # with open(f'response-{id}-tweets-processed.json', 'w', encoding='utf-8') as f:
  #   json.dump(response_json, f, indent=2)

if __name__ == "__main__":
  main()