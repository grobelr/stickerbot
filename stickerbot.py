"""
Main Source
"""
from threading import Thread
import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
from botwrapper import fbwrapper

import requests
import hashlib
import time
import leveldb
import json

app = Flask(__name__)


IMGUR_URL = 'https://api.imgur.com/3/image'

@app.route('/', methods=['GET', 'POST'])
def mainbot():
    """ Main Function """
    if request.method == 'POST':
        payload = request.get_json(force=True)
        proccessmessages = Thread(target=botprocess, args=(payload, ))
        proccessmessages.start()
        return "ok"
    else:
        return fbwrapper.verify_token(request.args['hub.verify_token'], request.args['hub.challenge'])

def botprocess(payload):
    """ Get the sticker and get out! """
    print payload
    userid, _, userinputdata, stickerid = fbwrapper.bring_me_args(payload)
    fbwrapper.sendtext(userid, "Sticker recebido: " + str(stickerid))
    urlimage = uploadmedia(userinputdata)
    fbwrapper.sendmedia(userid, 'image', urlimage)


def uploadmedia(url):
    print url
    headers = {"Authorization": "Client-ID " + IMGUR_CLIENT} 
    params = {
        'image': url
        }
    response = requests.post(
        IMGUR_URL,
        json=params,
        headers=headers
    )
    print response.text
    jsondecode = json.loads(response.text)
    return jsondecode['data']['link']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    #app.run()
