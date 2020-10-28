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
  endpoint_url = 'https://api.twitter.com/2/tweets/search/recent?max_results=100&query=covid'
  data = process_yaml()
  bearer_token = create_bearer_token(data)
  res_json = twitter_auth_and_connect(bearer_token, endpoint_url)
  print(res_json)

if __name__ == "__main__":
  main()