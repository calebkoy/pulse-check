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
  res_json = twitter_auth_and_connect(bearer_token, endpoint_url)  
  res_json_copy = copy.deepcopy(res_json)  
  res_json_copy['data'] = [obj for obj in res_json_copy['data'] if obj['lang'] == "en" or obj['lang'] == "en-gb"]  

  #print([object for object in res_json['data'] if object['lang'] == "en" or object['lang'] == "en-gb"], '\n')  
  #print(res_json)
  # TODO: DUMP THE NEXT BATCH USING PRETTY JSON AND WITHOUT!!    
  with open('temp-tweets-7-ensure-ascii-true-utf-8.json', 'w', encoding='utf-8') as f:
    json.dump(res_json, f, indent=2)
  with open('temp-tweets-7-ensure-ascii-false-utf-8.json', 'w', encoding='utf-8') as f:
    json.dump(res_json, f, ensure_ascii=False, indent=2)
  with open('temp-tweets-7-ensure-ascii-false-utf-8-only-en.json', 'w', encoding='utf-8') as f:
    json.dump(res_json_copy, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  main()