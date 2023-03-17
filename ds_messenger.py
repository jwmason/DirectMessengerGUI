# Mason Wong
# masonjw1@uci.edu
# 48567424

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    pass
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    pass