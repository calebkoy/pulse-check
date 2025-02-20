import math
import sys
from collections import defaultdict, Counter

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

class NaiveBayesClassifier(ClassifierMixin, BaseEstimator):
  def __init__(self, text_preprocessor):
    self.text_preprocessor = text_preprocessor        
    
  def fit(self, X, y):                                                       
    X, y = check_X_y(X, y, dtype='str')
    self.classes_, self.y_ = np.unique(y, return_inverse=True)                                                     
    self.X_ = X.reshape(len(X))        
    
    self.__group_data_by_class()
    self.__compute_log_class_priors()
    
    self.vocab_ = set()          
    self.class_total_word_counts_ = defaultdict(int)
    for c, data in self.grouped_data_.items():                        
      for index, text in enumerate(data):                                
        processed_text = self.text_preprocessor.process(text)
        data[index] = processed_text
        
        split_text = processed_text.split()
        self.class_total_word_counts_[c] += len(split_text)
        for word in split_text:
          self.vocab_.add(word)                                  
                    
    self.tf_idf_matrices_ = {}
    vectorizer = TfidfVectorizer(vocabulary=self.vocab_)
    for c, data in self.grouped_data_.items():                                                
      self.tf_idf_matrices_[c] = vectorizer.fit_transform(data).toarray()            
      
    self.tf_idf_matrix_feature_names_ = vectorizer.get_feature_names()
                  
    return self
  
  def predict(self, X):        
    check_is_fitted(self)                
    X = check_array(X, dtype='str')        
    vocab_size = len(self.vocab_)        
    predictions = np.empty(len(X))        
    for index, text in enumerate(X.reshape(len(X))):            
      predictions[index] = self.__compute_maximum_a_posteriori(text, vocab_size)                    
    
    return predictions
  
  def __group_data_by_class(self):
    self.grouped_data_ = {} 
    for index, c in enumerate(self.classes_):
      self.grouped_data_[c] = self.X_[np.asarray(self.y_ == index).nonzero()]                    
  
  def __compute_log_class_priors(self):
    self.log_class_priors_ = {}
    number_of_samples = len(self.X_)
    for c in self.classes_:            
      self.log_class_priors_[c] = math.log(len(self.grouped_data_[c]) / number_of_samples)        
          
  def __compute_maximum_a_posteriori(self, text, vocab_size):
    max_posterior = -sys.maxsize
    most_likely_class = -sys.maxsize
    for c in self.classes_:                
      posterior = self.log_class_priors_[c]
      processed_text = self.text_preprocessor.process(text)                
      word_counts = Counter(processed_text.split())
      total_words_in_class_texts = self.class_total_word_counts_[c]  
      tf_idf_matrix_column_sums = self.tf_idf_matrices_[c].sum(axis=0)
      for index, word in enumerate(self.vocab_):
        word_count = word_counts[word]
        if word_count == 0: 
          continue
        tf_idf_matrix_word_column_index = self.tf_idf_matrix_feature_names_.index(word)
        tf_idf_matrix_column_sum = tf_idf_matrix_column_sums[tf_idf_matrix_word_column_index]
        laplace_probability = (tf_idf_matrix_column_sum + 1) / (total_words_in_class_texts + vocab_size)                
        posterior += (word_count * math.log(laplace_probability))
      if posterior > max_posterior:
        max_posterior = posterior
        most_likely_class = c
    
    return most_likely_class        