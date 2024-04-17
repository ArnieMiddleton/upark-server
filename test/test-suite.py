import unittest
import requests
# import json

# base_url = 'http://localhost:8082'

class TestApi(unittest.TestCase):

  def test_init(self):
    self.assertEqual(1, 1)

  # def test_get(self):
  #   result = requests.get(base_url)
  #   self.assertEqual(result.status_code, 200)

  # def test_post_report(self):
  #   report = {
  #     'user_id': 1,
  #     'time': '2022-01-01 00:00:00',
  #     'lot_id': 1,
  #     'longitude': 0.0,
  #     'latitude': 0.0,
  #     'approx_fullness': 0.5,
  #   }
  #   result = requests.post(base_url + "/report", json=report)
  #   self.assertEqual(result.status_code, 200)

if __name__ == "__main__":
  print("Running Test Suite")
  unittest.main()
  print("Completed Test Suite")


