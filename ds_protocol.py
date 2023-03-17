# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module is in charge of changing data into JSON format"""

import json
from collections import namedtuple
from Profile import Post

DataTuple = namedtuple('DataTuple', ['token'])


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
