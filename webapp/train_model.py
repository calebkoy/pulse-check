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
  train_reviews_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'movie-reviews', 'train')
  train_pos_df = pd.read_csv(os.path.join(train_reviews_dir, 'reviews-pos.csv'))  
  train_neg_df = pd.read_csv(os.path.join(train_reviews_dir, 'reviews-neg.csv'))  
  train_pos_labels = np.ones(len(train_pos_df))
  train_neg_labels = np.zeros(len(train_neg_df))
  X = pd.concat([train_pos_df, train_neg_df]).to_numpy()
  y = np.concatenate((train_pos_labels, train_neg_labels))

  classifier = NaiveBayesClassifier(TextPreprocessor())
  test_X = pd.concat([train_pos_df[:3], train_neg_df[:3]]).to_numpy()
  test_y = np.array([1, 1, 1, 0, 0, 0])
  scores = cross_validate(classifier, test_X, test_y, cv=2, 
                          scoring=make_scorer(average_correct_predictions),
                          return_estimator=True, return_train_score=True)
  key = 'estimator'
  estimator = scores[key][0]
  with open('classifier.pkl', 'wb') as f:
    pickle.dump(estimator, f)

if __name__ == "__main__":
  main()