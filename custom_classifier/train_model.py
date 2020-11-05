import os
import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer

from custom_scorer import average_correct_predictions
from text_preprocessor import TextPreprocessor
from text_classifier import NaiveBayesClassifier

def main():  
  tweet_1 = "I love Twitter so much!"
  tweet_2 = "The sun came up today."
  tweet_3 = "I hate working at this place. There's so much work!"
  tweet_4 = "I'm not sure if I can survive this heat. It's really too much."
  tweet_5 = "I just saw a red car."
  tweet_6 = "Happy Birthday to me! I'm really looking forward to the day."
  X = pd.DataFrame([tweet_1, tweet_2, tweet_3, 
                    tweet_4, tweet_5, tweet_6]).to_numpy()
  y = np.array([2, 1, 0, 0, 1, 2])  
  classifier = NaiveBayesClassifier(TextPreprocessor())  
  scores = cross_validate(classifier, X, y, cv=2, 
                          scoring=make_scorer(average_correct_predictions),
                          return_estimator=True)
  key = 'estimator'
  estimator = scores[key][0]
  with open('classifier.pkl', 'wb') as f:
    pickle.dump(estimator, f)

if __name__ == "__main__":
  main()