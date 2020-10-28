import os
import pandas as pd

def create_review_csv(path, output_path):
  reviews = []
  encoding = "utf8"
  for filename in os.listdir(path):
    with open(os.path.join(path, filename), encoding=encoding) as f:
      reviews.append(f.read())
  reviews_df = pd.DataFrame({'review': reviews})
  reviews_df.to_csv(output_path, index=False)

movie_reviews_path = os.path.join(os.getcwd(), 'movie-reviews')
train_path = os.path.join(movie_reviews_path, 'train')
test_path = os.path.join(movie_reviews_path, 'test')

train_pos_path = os.path.join(train_path, 'pos')
train_neg_path = os.path.join(train_path, 'neg')
test_pos_path = os.path.join(test_path, 'pos')
test_neg_path = os.path.join(test_path, 'neg')

create_review_csv(train_neg_path, os.path.join(train_path, 'reviews-neg.csv'))
create_review_csv(train_pos_path, os.path.join(train_path, 'reviews-pos.csv'))
create_review_csv(test_neg_path, os.path.join(test_path, 'reviews-neg.csv'))
create_review_csv(test_pos_path, os.path.join(test_path, 'reviews-pos.csv'))