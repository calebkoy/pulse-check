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
    response = twitter_auth_and_connect(bearer_token, endpoint_url)
    
    # Filter for English tweets
    # Q: are you sure you want to modify the original response? A: TBC
    # TODO: check that the response has a 'data' key first    
    response['data'] = [obj for obj in response['data'] if obj['lang'] == "en" or obj['lang'] == "en-gb"]

    # For each tweet (which I'm almost sure will be a RT) in data that ends in an ellipsis
    ## Replace the tweet with the full text of the tweet

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