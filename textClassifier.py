import nltk
import os
import re

from nltk.corpus import stopwords

# load in data
def load_data():
  """"""
  
  topics = ['business', 
            'entertainment',
            'politics', 
            'sport', 
            'tech']
  
  data_directory = os.path.join(os.getcwd(), 'data')
  documents_by_class = []
  # for each topic:
  for topic in topics:
    documents = []
    # open the corresponding directory
    directory = os.path.join(data_directory, topic)
    # for each file in the directory
    for filename in os.listdir(directory):
      # read the contents of the file as a string
      # and place the result in a list corresponding 
      # to documents for that class
      with open(os.path.join(directory, filename)) as f:
        documents.append(f.read())
    documents_by_class.append(documents)
  return documents_by_class
      

# process data
def process_data(documents_by_class):
  """"""
  for topic_documents in documents_by_class:
    # remove spaces
    topic_documents[:] = [' '.join(document.split()) for document in topic_documents]
    
    # remove punctuation ( !"£$%^&*()-_+=[]{};:'@#~\|,<.>/? ) and numbers
    # TODO: consider if there's an optimisation using a lambda function
    topic_documents[:] = [re.sub('[^a-zA-Z]', ' ', document) for document in topic_documents]             
        
    # consider removing single-character words 
    # (which might be the result of removing punctuation and numbers)
    topic_documents[:] = [' '.join([w for w in document.split() if len(w) > 1]) for document in topic_documents]
  
    # lowercase all words
    topic_documents[:] = [document.lower() for document in topic_documents]
  
    # tokenize
    topic_documents[:] = [document.split() for document in topic_documents]
  
    # remove stopwords (use nltk?)
    topic_documents[:] = [[word for word in doc if word not in stopwords.words("english")] 
                          for doc in topic_documents]
    
    # lemmatize the words

  return documents_by_class

# split data into train and test and validation (use k-fold cross-validation)

# train the model

# evaluate the model

if __name__ == "__main__":     
  documents_by_class = load_data()    
  # topic_1 = documents_by_class[0]
  # topic_1[:] = [' '.join(document.split()) for document in topic_1]
  # print(topic_1[0], '\n') 
  # print(documents_by_class[0][0])
  #print(single_doc)
  # single_doc = ' '.join(single_doc.split())
  #print(single_doc)
  # single_doc = re.sub('[^a-zA-Z]', ' ', single_doc)
  # print(single_doc)

  #documents_by_class[:] = process_data(documents_by_class)
  # for document in documents_by_class[0]:
  #   print(document[:50])
  # for topic_documents in documents_by_class:
  #   print('New topic\n')
  #   for document in topic_documents:
  #     print(document[:50], '\n')
