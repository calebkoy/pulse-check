import pickle

import flask
import numpy as np
import pandas as pd
import requests
import twitter
import yaml

import text_classifier

with open('model/classifier.pkl', 'rb') as f:
  classifier = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main():
  if flask.request.method == 'GET':
    return flask.render_template('main.html')

  if flask.request.method == 'POST':
    topic = flask.request.form['topic']
    endpoint_url = f'https://api.twitter.com/2/tweets/search/recent?query={topic}&tweet.fields=created_at,lang&max_results=100'
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    response_json = twitter_auth_and_connect(bearer_token, endpoint_url)
    
    # Test what happens when a topic that has no tweets (for the specified time period) is used in the request.
    # Update the code below accordingly.
    
    # Filter for English tweets
    # Q: are you sure you want to modify the original response? A: TBC    
    if 'data' in response_json: # Q: Is this necessary? A: TBC
      response_json['data'] = ([tweet for tweet in response_json['data'] 
                                if tweet['lang'] == "en" 
                                or tweet['lang'] == "en-gb"])

    # TODO: Consider wrapping the necessary code in a try, 
    # in case the data that is returned is not as expected and you get an exception
    # Replace retweets that end in an ellipsis with the full tweet
    # ============================================================
    # Q: Is this robust to potential changes to the unicode? A: TBC
    # Q: Is it possible that there are different unicode or other code values for this symbol? A: TBC
    ellipsis_unicode = '\u2026'     
    retweet_abbreviation = 'RT'
    retweeted_tweets = {}
    # For each tweet (which I'm almost sure will be a RT) in data that ends in an ellipsis
    for tweet in response_json['data']:                  
      ## if the tweet text ends in an ellipsis and the string starts with RT
      ## (I haven't come across any cases where the former is true and the latter isn't; so the latter might not be necessary)
      ## (I'll leave it in just in case)
      if (tweet['text'].endswith(ellipsis_unicode) 
          and tweet['text'].startswith(retweet_abbreviation)):
        ## Replace the tweet with the full text of the tweet    
        # 1. get ID of referenced tweet
        for tweet_reference in tweet['referenced_tweets']:
          if tweet_reference['type'] == 'retweeted':
            retweeted_tweet_id = tweet_reference['id']
            break                      
        # 2. get full tweet
        if retweeted_tweet_id in retweeted_tweets:
          full_tweet = retweeted_tweets[retweeted_tweet_id]
        else:
          for referenced_tweet in response_json['includes']['tweets']:
            if referenced_tweet['id'] == retweeted_tweet_id:
              full_tweet = referenced_tweet['text']
              retweeted_tweets[retweeted_tweet_id] = full_tweet
              break
        
        tweet['full_text'] = full_tweet

    # For each tweet
    ## Consider removing \n, \" and &amp; (and similar &xxx character combos); might not be a problem if ascii set to false (maybe not for the &xxx, though)
    ## Remove URLs (probably regex)
    ## Remove emojis might not be a problem if ascii set to false
    ## Remove user mentions (the @ symbol and the username)
    ## remove repeated characters (maybe use nltk word_tokenize) if they won't be removed in the classifier
    ## Consider removing hashtags (just the hash symbol) if they won't be removed in the classifier
    ## Maybe consider splitting up multi-word hashtags

    # TODO: replace 'sentiment' with what it should be
    return flask.render_template('main.html', result=sentiment)

def process_yaml():
  with open("config.yaml") as file:
    return yaml.safe_load(file)

def create_bearer_token(data):
  return data["search_tweets_api"]["bearer_token"]

def twitter_auth_and_connect(bearer_token, url):
  headers = {"Authorization": "Bearer {}".format(bearer_token)}
  response = requests.request("GET", url, headers=headers)
  return response.json()

if __name__ == '__main__':
  app.run()