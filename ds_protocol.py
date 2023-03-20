# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module is in charge of changing data into JSON format"""

import json
import time
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['token'])

class Post(dict):
    """
    The Post class is responsible for working with individual user posts.
    It currently supports two features: A timestamp property that is set
    upon instantiation and when the entry object is set and an entry property
    that stores the post message.

    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        """This initiates the class"""
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """This sets entry"""
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        """This returns entry"""
        return self._entry

    def set_time(self, time: float):
        """This sets time"""
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        """This gets time"""
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)

def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert
    it to a DataTuple object with the token received by server.
    '''
    try:
        json_obj = json.loads(json_msg)
        if json_obj['response']['type'] == 'ok':
            token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(token)


def join(username, password):
    '''Returns join json object back to ds_client.'''
    json_join = {"join": {"username": f"{username}",
                          "password": f"{password}", "token": ""}}
    return json_join


def post(message, token):
    '''Returns post json object back to ds_client.'''
    if message == '' or message == ' ':
        json_post = 'error'
    else:
        json_post = {"token": f"{token}", "post": {"entry": f"{message}",
                     "timestamp": f"{Post(message).get_time()}"}}
    return json_post


def bio(bio, token):
    '''Returns bio json object back to ds_client.'''
    if bio == '' or bio == ' ':
        json_bio = 'error'
    else:
        json_bio = {"token": f"{token}", "bio": {"entry": f"{bio}",
                    "timestamp": f"{Post(bio).get_time()}"}}
    return json_bio


def server_response(resp):
    '''Returns True or False based on json object received
    by ds_client from DSP server.'''
    if resp["response"]["type"] == "error":
        send_return = False
    elif resp["response"]["type"] == "ok":
        send_return = True
    return send_return


def directmessage(token, user=None, user_msg=None, messages=None):

    if token and user_msg and user and messages is None:
        server_send = {"token":f"{token}", "directmessage": {"entry": f"{user_msg}","recipient":f"{user}", "timestamp": f"{Post(user_msg).get_time()}"}}
    elif token and messages == 'new':
        server_send = {"token":f"{token}", "directmessage": "new"}
    elif token and messages == 'all':
        server_send = {"token":f"{token}", "directmessage": "all"}
    return server_send
