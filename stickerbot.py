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
import fileinput

app = Flask(__name__)


IMGUR_URL = 'https://api.imgur.com/3/image'
IMGUR_CLIENT = os.environ['IMGUR_CLIENT']

## Adjust your path here.
@app.route('/stickerbot', methods=['GET', 'POST'])
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
    userid, _, userinputdata, stickerid = fbwrapper.bring_me_args(payload)
    if stickerid == "None":
        fbwrapper.sendtext(userid, "Naaaaaaaaaaa!! Send me a Sticker or get out!")
        return
    stickervars = getSticker(stickerid, db)

    if stickervars:
        jsonSticker = json.loads(stickervars)
        fbwrapper.sendtext(userid, "Description: " + jsonSticker['description'])
        fbwrapper.sendtext(userid, "Mood: " + jsonSticker['mood'])
        fbwrapper.sendtext(userid, "StickerID: " + stickerid)
    else:
        fbwrapper.sendtext(userid, "Not found, stickerid: " + stickerid)
        urlimage = uploadmedia(userinputdata)
        putSticker(stickerid, urlimage, db)
        fbwrapper.sendtext(userid, "thx for helping me find all sticker!")
        fbwrapper.sendtext(userid, "You can see every fckin sticker that I got on https://github.com/grobelr/stickerbot")
        updateFile(stickerid, urlimage, "Not Set!", "Not Set!")


def uploadmedia(url):
    headers = {"Authorization": "Client-ID " + IMGUR_CLIENT} 
    params = {
        'image': url
        }
    response = requests.post(
        IMGUR_URL,
        json=params,
        headers=headers
    )
    jsondecode = json.loads(response.text)
    return jsondecode['data']['link']

def getSticker(stickerid, db):
    try: 
        s = db.Get(stickerid)
        return s
    except:
        return False

def putSticker(stickerid, urlimage, db):
    try:
        sticker = {}
        sticker['urlimage'] = urlimage
        sticker['description'] = "Not set!"
        sticker['mood'] = "Not set!"
        jsoned = json.dumps(sticker)
        db.Put(stickerid, jsoned)
        return True
    except:
        return False

def updateFile(stickerid, imageurl, description, mood):
    gitimage = '![Image of Sticker](' + imageurl + ')'
    f = open("README.md","a+")
    f.write("\n|" + stickerid +  "|" + gitimage + "|" + description + "|" + mood + "|")
    f.close()

if __name__ == '__main__':
    db = leveldb.LevelDB("./sticker")
    app.run(host='0.0.0.0', port=7000)
    #app.run()
