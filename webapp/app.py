import pickle

import flask
import numpy as np
import pandas as pd
import requests
import twitter
import yaml
# from imdb import IMDb

import text_classifier

with open('model/classifier.pkl', 'rb') as f:
  classifier = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main():
  if flask.request.method == 'GET':
    return flask.render_template('main.html')

  if flask.request.method == 'POST':
    # TODO: remove; only for testing
    # review = flask.request.form['movie_review']
    # classifier_input = np.array(review).reshape((1, 1))
    # prediction = classifier.predict(classifier_input)
    # sentiment = 'positive' if prediction[0] == 1 else 'negative'
    

    # TODO: Get a set of reviews for this movie
    movie_name = flask.request.form['movie']
    imdb_instance = IMDb() 
    movie_matches = imdb_instance.search_movie(movie_name)
    # reviews_df = TBC

    # TODO: Predict the sentiment of these reviews
    # predictions = classifier.predict(reviews_df.to_numpy())
    # total_positive_reviews = len(predictions[predictions==1])
    # total_negative_reviews = len(predictions[predictions==0])

    return flask.render_template('main.html', result=sentiment)

if __name__ == '__main__':
  app.run()