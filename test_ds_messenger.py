import unittest
from ds_messenger import DirectMessage, DirectMessenger

class TestDirectMessenger(unittest.TestCase):
    """This class tests all of DirectMessenger"""
    def setUp(self):
        """Sets up a test direct message"""
        self.dm = DirectMessenger(dsuserver="168.235.86.101", username="masonwong123", password="password")

    def test_send_message(self):
        """This tests the send function"""
        recipient = "masonwong12"
        message = "test message"
        self.assertTrue(self.dm.send(message, recipient))

    def test_retrieve_new(self):
        """This tests retrieving new messages"""
        recipient = "masonwong12"
        message = "test message"
        self.dm.send(message, recipient)
        messages = self.dm.retrieve_new()
        self.assertTrue(messages, {"response": {"type": "ok", "messages": [{"message": "directmessage", "from": "masonwong12", "timestamp": "1679264401.489704"}]}})
        self.assertTrue(messages, DirectMessage)

    def test_retrieve_all(self):
        """This tests retrieving all messages"""
        recipient = "masonwong12345"
        message1 = "test message 1"
        message2 = "test message 2"
        self.dm.send(message1, recipient)
        self.dm.send(message2, recipient)
        messages = self.dm.retrieve_all()
        self.assertTrue(messages, {"response": {"type": "ok", "messages": []}})
        self.assertTrue(messages, DirectMessage)

if __name__ == '__main__':
    unittest.main()