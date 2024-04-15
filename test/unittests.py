# FILEPATH: /Users/ianmoore/development/source/repos/upark-server/tests/test_server.py
import unittest
import app.server as server
import json

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        self.app.testing = True

    def test_home(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'"Welcome to the UPark API"')

    def test_get_lots(self):
        result = self.app.get('/lots')
        self.assertEqual(result.status_code, 200)
        # Add more assertions based on the expected data

    def test_get_lot(self):
        result = self.app.get('/lots/1')  # assuming a lot with id 1 exists
        self.assertEqual(result.status_code, 200)
        # Add more assertions based on the expected data

    def test_get_lot_id(self):
        result = self.app.get('/lots/lot_name')  # assuming a lot with name 'lot_name' exists
        self.assertEqual(result.status_code, 200)
        # Add more assertions based on the expected data

    def test_get_reports(self):
        result = self.app.get('/reports')
        self.assertEqual(result.status_code, 200)
        # Add more assertions based on the expected data

    def test_get_buildings(self):
        result = self.app.get('/buildings')
        self.assertEqual(result.status_code, 200)
        # Add more assertions based on the expected data

    def test_get_username(self):
        result = self.app.get('/user/1')  # assuming a user with id 1 exists
        self.assertEqual(result.status_code, 200)
        # Add more assertions based on the expected data

    def test_post_report(self):
        report_data = {
            'user_id': 1,
            'time': '2022-01-01 00:00:00',
            'lot_id': 1,
            'est_fullness': 0.5
        }
        result = self.app.post('/report', data=json.dumps(report_data), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'"Report added"')

if __name__ == "__main__":
    unittest.main()