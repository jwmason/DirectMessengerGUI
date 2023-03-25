# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This function contains the classes to direct messaging"""

import socket
import json
import ds_protocol


class DirectMessage:
    """This class initiates the attributes
    of a direct message"""
    def __init__(self, recipient=None, message=None, timestamp=None):
        """This initiates th attributes"""
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    """This class initiates the abiliy to direct message"""
    def __init__(self, dsuserver=None, username=None, password=None) -> list:
        """This initiates the attributes of the class"""
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        try:
            if self.dsuserver:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.dsuserver, 3021))
                msg = ds_protocol.join(self.username, self.password)

                send = client.makefile('w')
                recv = client.makefile('r')

                msg = json.dumps(msg)
                send.write(msg)
                send.flush()
                resp = recv.readline()[:-1]

                self.token = ds_protocol.extract_json(resp)[0]
                client.close()
        except (ValueError, ConnectionRefusedError, socket.error):
            pass

    def send(self, message: str, recipient: str) -> bool:
        """Sends direct message and returns true if message successfully sent,
        false if send failed."""
        try:
            if self.dsuserver:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.dsuserver, 3021))

                msg = ds_protocol.directmessage(self.token, recipient, message)
                send2 = client.makefile('w')
                recv2 = client.makefile('r')

                msg = json.dumps(msg)
                send2.write(msg)
                send2.flush()
                resp2 = recv2.readline()[:-1]

                print('\nServer Response:', resp2)
                client.close()
                return True
        except (socket.error, TypeError, ConnectionRefusedError,
                json.JSONDecodeError, ValueError, Exception,
                NameError, OSError, TimeoutError, AttributeError):
            return False

    def retrieve_new(self) -> list:
        """Returns a list of DirectMessage objects containing
        all new messages"""
        try:
            if self.dsuserver:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.dsuserver, 3021))

                msg = ds_protocol.directmessage(self.token, messages='new')

                send2 = client.makefile('w')
                recv2 = client.makefile('r')

                msg = json.dumps(msg)
                send2.write(msg)
                send2.flush()
                resp2 = recv2.readline()[:-1]

                resp2 = json.loads(resp2)

                direct_messages = []
                for message in resp2['response']['messages']:
                    direct_message = DirectMessage(message['from'],
                                                   message['message'],
                                                   message['timestamp'])
                    direct_messages.append(direct_message)
                client.close()
                return direct_messages
        except (socket.error, TypeError, ConnectionRefusedError):
            return []

    def retrieve_all(self) -> list:
        """Returns a list of DirectMessage objects containing all messages"""
        try:
            if self.dsuserver:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.dsuserver, 3021))

                msg = ds_protocol.directmessage(self.token, messages='all')

                send2 = client.makefile('w')
                recv2 = client.makefile('r')

                msg = json.dumps(msg)
                send2.write(msg)
                send2.flush()
                resp2 = recv2.readline()[:-1]

                resp2 = json.loads(resp2)

                direct_messages = []
                for message in resp2['response']['messages']:
                    direct_message = DirectMessage(message['from'],
                                                   message['message'],
                                                   message['timestamp'])
                    direct_messages.append(direct_message)
                client.close()
                return direct_messages
        except (socket.error, TypeError, ConnectionRefusedError):
            return []
