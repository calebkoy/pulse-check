import unittest

from app import app

class AppTests(unittest.TestCase):
  def setUp(self):
    self.app = app.test_client()
  
  def test_main_returns_homepage_when_no_query_parameters(self):    
    response = self.app.get('/', content_type='html/text')
    self.assertEqual(response.status_code, 200)    
    self.assertIn(b'Predict sentiment', response.data)

  def test_main_returns_analysed_tweets_or_no_show_message_when_topic_submitted(self):
    response = self.app.get('/?topic=twitter+dev', content_type='html/text')      
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Predict sentiment', response.data)         
  
  def test_page_not_found(self):
    response = self.app.get('/random_page', content_type='html/text')
    self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()