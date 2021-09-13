from flask import Flask,request
from flask import request_started
from flask import request_finished
from datetime import datetime
from ruamel import yaml
import requests
import socket
import time 
import json
import os
import zmq

from search_request_body import *
from config import *


def stream_data(data):
    """
    Send data to master event manager via zeromq
    """

    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect(get_socket())

    print("Starting loop...")
    time.sleep(2)
    sock.send_json(data)
    sock.close()
    ctx.term()

def incoming_request(sender):
    """
    Manage Incoming requests
    """

    d = {"name": "", "dmscode": "", "newstate": "", "messageid": ""}
    if request.method == 'POST':
        module_name = sender.name 
        input_data= json.loads(request.data)

        docid = dict_search(["documentId","documentid"], input_data)
        docname = dict_search(["documentName","filename"], input_data)
        messageid = dict_search(["messageid"], input_data)

        d["name"] = list(docname.values())[0]
        d["dmscode"] = list(docid.values())[0]
        d["newstate"] = "Started " + module_name
        d["messageid"] = list(messageid.values())[0]

        stream_data(d)

def request_ended(sender, response):
    """
    Manage response
    """

    d = {"name": "", "dmscode": "", "newstate": "", "messageid": ""}
    if request.method == 'POST':
        module_name = sender.name 
        input_data= json.loads(request.data)

        docid = dict_search(["documentId","documentid"], input_data)
        docname = dict_search(["documentName","filename"], input_data)
        messageid = dict_search(["messageid"], input_data)
        
        d["name"] = list(docname.values())[0]
        d["dmscode"] = list(docid.values())[0]
        d["newstate"] = "Finished " + module_name
        d["messageid"] = list(messageid.values())[0]

        stream_data(d)


def send_event(app):
    """
    Main Process
    """
    request_started.connect(incoming_request, app)
    request_finished.connect(request_ended, app)
