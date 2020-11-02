import pickle
import re

import emoji
import flask
import numpy as np
import requests
import twitter
import yaml

from sentiment import Sentiment

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

def remove_non_alpha_or_space_characters(tweet):        
  tweet['text'] = re.sub(r'[^a-zA-Z\s]', '', tweet['text'])

def remove_many_consecutive_repeated_characters(tweet):
  tweet['text'] = re.sub(r'([a-zA-Z])\1{3,}', r'\1\1', tweet['text'])

def remove_short_words(tweet):
  tweet['text'] = re.sub(r'\b\w{1,2}\b', '', tweet['text'])

def process_tweets(response_json):
  ellipsis_unicode = '\u2026'     
  retweet_abbreviation = 'RT'  
  retweeted_tweets = {}
  for tweet in response_json['data']:                        
    if (tweet['text'].startswith(retweet_abbreviation) and 
        tweet['text'].endswith(ellipsis_unicode)):            
      
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
    remove_urls(tweet)
    remove_html_character_entities(tweet)    
    remove_emoji(tweet)
    remove_at_mentions(tweet)    
    remove_non_alpha_or_space_characters(tweet)
    remove_many_consecutive_repeated_characters(tweet)
    remove_short_words(tweet)

def compute_sentiment_percentages(predictions):
  total_predictions = len(predictions)      
  percent_positive = (sum((predictions == Sentiment.POSITIVE.value).astype(int)) / 
                      total_predictions)
  percent_negative = (sum((predictions == Sentiment.NEGATIVE.value).astype(int)) / 
                      total_predictions)
  return {"positive": round(percent_positive * 100, 1),          
          "negative": round(percent_negative * 100, 1)}

def get_tweet_ids_by_sentiment(predictions, tweet_ids):
  positive_indices = np.asarray(predictions == Sentiment.POSITIVE.value).nonzero()
  negative_indices = np.asarray(predictions == Sentiment.NEGATIVE.value).nonzero()
  positive_tweet_ids = tweet_ids[positive_indices]
  negative_tweet_ids = tweet_ids[negative_indices]
  return {"positive": positive_tweet_ids,          
          "negative": negative_tweet_ids}

@app.route('/')
def main():
  if not 'topic' in flask.request.args:
    return flask.render_template('main.html')    
  else:
    max_results = 10 # TODO: change to 100 for live app            
    topic = flask.request.args['topic'].strip()
    topic = re.sub(r'[^a-zA-Z\s]', '', topic)
    response_json = get_tweet_data(topic, max_results)                
    if 'data' in response_json: 
      response_json['data'] = ([tweet for tweet in response_json['data'] 
                                if tweet['lang'] == "en" 
                                or tweet['lang'] == "en-gb"])            
    
      if (not response_json['data']):
        return flask.render_template('main.html', no_show=True)
      process_tweets(response_json) 
      tweets = []
      tweet_ids = []      
      for tweet in response_json['data']:
        if tweet['text'] not in tweets:          
          tweets.append(tweet['text'])   
          tweet_ids.append(tweet['id'])       
      with open('grid_search_NB_clf_sentiment140.pkl', 'rb') as f:
        classifier = pickle.load(f)
      predictions = classifier.predict(tweets)
      sentiment_percentages = compute_sentiment_percentages(predictions)
      tweet_ids_by_sentiment = get_tweet_ids_by_sentiment(predictions, 
                                                          np.array(tweet_ids))
      tweet_base_url = "https://twitter.com/i/web/status"      
      return flask.render_template('main.html', 
                                    original_topic=topic, 
                                    sentiment_percentages=sentiment_percentages,
                                    tweet_ids=tweet_ids_by_sentiment,
                                    tweet_base_url=tweet_base_url,
                                    total_tweets=len(tweets)) 
    else:
      return flask.render_template('main.html', no_show=True)

if __name__ == '__main__':
  app.run()