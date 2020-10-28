import re

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

class ReviewProcessor:
  def remove_html_tags(self, text):
    return BeautifulSoup(text, features="html.parser").get_text()
  
  def remove_non_alpha_or_space_characters(self, text):        
    return re.sub(r'[^a-zA-Z\s]', '', text)
    
  def remove_short_words(self, text):
    return re.sub(r'\b\w{1,2}\b', '', text)
    
  def remove_stop_words(self, text):
    pattern = re.compile(r'\b(' + r'|'.join(stopwords.words("english")) + r')\b\s*')
    return pattern.sub('', text)
  
  def lemmatize(self, text):                
    lemmatizer = WordNetLemmatizer()
    split_text = text.split()
    split_text[:] = [lemmatizer.lemmatize(word) for word in split_text]
    split_text[:] = [lemmatizer.lemmatize(word, pos='v') for word in split_text]
    return ' '.join(split_text)                
  
  def process(self, text):
    text = self.remove_html_tags(text)
    text = self.remove_non_alpha_or_space_characters(text)
    text = self.remove_short_words(text).lower()
    text = self.remove_stop_words(text)
    return self.lemmatize(text)