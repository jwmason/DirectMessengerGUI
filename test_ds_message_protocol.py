# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module tests the direct message function
from the ds protocol module"""

from ds_protocol import directmessage
import unittest

class TestDirectMessage(unittest.TestCase):
    
    def test_directmessage_new(self):
        expected_output = {"token": "test123", "directmessage": "new"}
        actual_output = directmessage(token="test123", messages="new")
        self.assertEqual(actual_output, expected_output)

    def test_directmessage_all(self):
        expected_output = {"token": "test123", "directmessage": "all"}
        actual_output = directmessage(token="test123", messages="all")
        self.assertEqual(actual_output, expected_output)

    def test_directmessage_entry(self):
        actual_output = directmessage(token="test123", user_msg="Hello World", user="user123")
        timestamp = actual_output['directmessage']['timestamp']
        expected_output = {"token": "test123", "directmessage": {"entry": "Hello World", "recipient": "user123", "timestamp": f'{timestamp}'}}
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
