# Mason Wong
# masonjw1@uci.edu
# 48567424

import socket
import json
import ds_protocol

class DirectMessage:
  def __init__(self, recipient = None, message = None, timestamp = None):
    self.recipient = recipient
    self.message = message
    self.timestamp = timestamp

class DirectMessenger(DirectMessage):
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    try:
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect((self.dsuserver, 3021))
      msg = ds_protocol.join(self.username, self.password)

      send = client.makefile('w')
      recv = client.makefile('r')

      msg = json.dumps(msg)
      send.write(msg)
      send.flush()
      resp = recv.readline()[:-1]

      print('\nServer Response:', resp)
      self.token = ds_protocol.extract_json(resp)[0]
      client.close()
    except (ValueError, ConnectionRefusedError, socket.error):
      raise ValueError("Error")

  def send(self, message:str, recipient:str) -> bool:
    """Sends direct message and returns true if message successfully sent,
    false if send failed."""
    try:
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
    except (socket.error, TypeError, ConnectionRefusedError):
      return False
		
  def retrieve_new(self) -> list:
    """Returns a list of DirectMessage objects containing all new messages"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((self.dsuserver, 3021))

    msg = ds_protocol.directmessage(self.token, messages = 'new')

    send2 = client.makefile('w')
    recv2 = client.makefile('r')

    msg = json.dumps(msg)
    send2.write(msg)
    send2.flush()
    resp2 = recv2.readline()[:-1]

    print('\nServer Response:', resp2)
    client.close()
    return resp2
 
  def retrieve_all(self) -> list:
    """Returns a list of DirectMessage objects containing all messages"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((self.dsuserver, 3021))

    msg = ds_protocol.directmessage(self.token, messages = 'all')

    send2 = client.makefile('w')
    recv2 = client.makefile('r')

    msg = json.dumps(msg)
    send2.write(msg)
    send2.flush()
    resp2 = recv2.readline()[:-1]

    print('\nServer Response:', resp2)
    client.close()
    return resp2

test = DirectMessenger('168.235.86.101', 'masonwong123', 'password')
# test_t_or_f = test.send("hi this is a test", "masonwong1234")
# print(test_t_or_f)
test_new = test.retrieve_new()
test_all = test.retrieve_all()