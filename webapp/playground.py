import copy
import json

import requests
import twitter
import yaml

def create_bearer_token(data):
  return data["search_tweets_api"]["bearer_token"]

def process_yaml():
  with open("config.yaml") as file:
    return yaml.safe_load(file)

def twitter_auth_and_connect(bearer_token, url):
  headers = {"Authorization": "Bearer {}".format(bearer_token)}
  response = requests.request("GET", url, headers=headers)
  return response.json()

def main():
  endpoint_url = 'https://api.twitter.com/2/tweets/search/recent?query=covid&tweet.fields=created_at,lang,entities&expansions=referenced_tweets.id'
  data = process_yaml()
  bearer_token = create_bearer_token(data)
  response_json = twitter_auth_and_connect(bearer_token, endpoint_url)        

  if 'data' in response_json: 
    response_json['data'] = ([tweet for tweet in response_json['data'] 
                              if tweet['lang'] == "en" 
                              or tweet['lang'] == "en-gb"])
      
  id = '10'
  
  with open(f'response-{id}-ensure-ascii-false.json', 'w', encoding='utf-8') as f:
    json.dump(response_json, f, ensure_ascii=False, indent=2)  
  with open(f'response-{id}.json', 'w', encoding='utf-8') as f:
    json.dump(response_json, f, indent=2)  
  
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

  with open(f'response-{id}-retweets-replaced.json', 'w', encoding='utf-8') as f:
    json.dump(response_json, f, indent=2)

if __name__ == "__main__":
  main()