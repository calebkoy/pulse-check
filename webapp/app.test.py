import unittest

from app import app

class BasicTestCase(unittest.TestCase):
  def test_main(self):
    tester = app.test_client(self)
    response = tester.get('/', content_type='html/text')
    self.assertEqual(response.status_code, 200)
    # TODO: figure out how to change this in order to test the various cases
    #self.assertEqual(response.data, b'Hello World!')

  def test_page_not_found(self):
    tester = app.test_client(self)
    response = tester.get('random_page', content_type='html/text')
    self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()