# Mason Wong
# masonjw1@uci.edu
# 48567424

import socket
import json
import ds_protocol

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password

  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
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
      token = ds_protocol.extract_json(resp)[0] 
      msg2 = ds_protocol.directmessage(token, recipient, message)
      
      send2 = client.makefile('w')
      recv2 = client.makefile('r')
  
      msg2 = json.dumps(msg2)
      send2.write(msg2)
      send2.flush()
      resp2 = recv2.readline()[:-1]

      print('\nServer Response:', resp2)
      client.close()
      return True
    except (socket.error, TypeError):
      return False
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    pass


test = DirectMessenger('168.235.86.101', 'masonwong12', 'password')
test.send("hi this is a test", "masonwong123")
