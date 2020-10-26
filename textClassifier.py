import os
import csv
import pandas as pd

# load in movie review data
def load_data():
  imdb_dataset = os.path.join(os.getcwd(), 'imdb-dataset', 'IMDB-Dataset')
  reviews_df = pd.read_csv(imdb_dataset)
  reviews_df.head()


# process the data 
## separate into train and test
## remove HTML tags (use BeautifulSoup)
## remove punctuation and numbers (but not \s?)
## remove words of length less than 3
## remove stop words
## lowercase everything
## lemmatise
## split into train and test sets
## convert to bow
### collect unique words in corpus to form your vocab (for train and then for test)
### construct document-term matrix (use CountVectorizer?)
### apply tf-idf (consider TfidfVectorizer)

# apply laplace smoothing (does this go under implementation of the classifier?)

# implement the classifier

# train the classifier 

# evaluate the classifier

def create_review_df(path, output_path):
  reviews = []
  encoding = "utf8"
  for filename in os.listdir(path):
    with open(os.path.join(path, filename), encoding=encoding) as f:
      reviews.append(f.read())
  reviews_df = pd.DataFrame({'review': reviews})
  reviews_df.to_csv(output_path, index=False)

if __name__ == "__main__":
  movie_reviews_path = os.path.join(os.getcwd(), 'movie-reviews')
  train_path = os.path.join(movie_reviews_path, 'train')
  test_path = os.path.join(movie_reviews_path, 'test')
  
  train_pos_path = os.path.join(train_path, 'pos')
  train_neg_path = os.path.join(train_path, 'neg')
  test_pos_path = os.path.join(test_path, 'pos')
  test_neg_path = os.path.join(test_path, 'neg')

  create_review_df(test_neg_path, os.path.join(test_path, 'reviews-neg.csv'))
  
  #create_review_df(os.path.join(train_path, 'temp'), os.path.join(train_path, 'temp-reviews.csv'))  
  #temp_df = pd.read_csv(os.path.join(train_path, 'temp-reviews.csv'))
  #print(temp_df)
  #print(temp_df['review'][6])
  
  #load_data()    
  
  # print(train_neg[0], '\n')
  # print(train_neg[-1], '\n')
  # print(train_pos[0], '\n')
  # print(train_pos[-1], '\n')
  # print(test_neg[0], '\n')
  # print(test_neg[-1], '\n')
  # print(test_pos[0], '\n')
  # print(test_pos[-1], '\n')

# def load_data():
#   """"""
#   cwd = os.getcwd()
#   reviews_dir = os.path.join(cwd, 'movie-reviews')
#   test_dir = os.path.join(reviews_dir, 'test')
#   train_dir = os.path.join(reviews_dir, 'train')
#   encoding = "utf8"
  
#   train_neg = []
#   train_neg_dir = os.path.join(train_dir, 'neg')
#   for filename in os.listdir(train_neg_dir):
#     with open(os.path.join(train_neg_dir, filename), encoding=encoding) as f:
#       train_neg.append(f.read())

#   train_pos = []
#   train_pos_dir = os.path.join(train_dir, 'pos')
#   for filename in os.listdir(train_pos_dir):
#     with open(os.path.join(train_pos_dir, filename), encoding=encoding) as f:
#       train_pos.append(f.read())

#   test_neg = []
#   test_neg_dir = os.path.join(test_dir, 'neg')
#   for filename in os.listdir(test_neg_dir):
#     with open(os.path.join(test_neg_dir, filename), encoding=encoding) as f:
#       test_neg.append(f.read())

#   test_pos = []
#   test_pos_dir = os.path.join(test_dir, 'pos')
#   for filename in os.listdir(test_pos_dir):
#     with open(os.path.join(test_pos_dir, filename), encoding=encoding) as f:
#       test_pos.append(f.read())

#   return train_neg, train_pos, test_neg, test_pos