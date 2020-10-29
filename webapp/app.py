import pickle
import re

import emoji
import flask
import numpy as np
import pandas as pd
import requests
import twitter
import yaml

import text_classifier

app = flask.Flask(__name__, template_folder='templates')

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

def remove_retweet_abbreviation(tweet):
  tweet['text'] = re.sub(r'', '', tweet['text'])

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

@app.route('/', methods=['GET', 'POST'])
def main():
  if flask.request.method == 'GET':
    return flask.render_template('main.html')

  if flask.request.method == 'POST':    
    max_results = 10 # TODO: change to 100 for live app        
    response_json = get_tweet_data(flask.request.form['topic'], max_results)
    
    # Test what happens when a topic that has no tweets (for the specified time period) is used in the request.
    # and update the code below accordingly.
    
    # Q: are you sure you want to modify the original response? A: TBC    
    if 'data' in response_json: # Q: Is this necessary? A: TBC
      response_json['data'] = ([tweet for tweet in response_json['data'] 
                                if tweet['lang'] == "en" 
                                or tweet['lang'] == "en-gb"])            

    process_tweets(response_json) 

    tweets = []
    for tweet in response_json['data'] :
      tweets.append(tweet['text'])
    
    with open('classifier.pkl', 'rb') as f:
      classifier = pickle.load(f)

    predictions = classifier.predict(tweets.to_numpy())

    # TODO: replace 'sentiment' with what it should be
    return flask.render_template('main.html', result=sentiment)

if __name__ == '__main__':
  app.run()