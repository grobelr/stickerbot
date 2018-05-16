import requests

FACEHOOKURL = "https://graph.facebook.com/v2.9/me"


def sendmedia(userid, typemedia=None, url=None, attachment_id=None):
    """ Insert/Send Photos/Videos """
    if typemedia is None:
        print "Tipo nao definido inserMedia"
        return
    else:
        if attachment_id is None:
            message = {
                'recipient':{
                    'id':userid
                },
                'message':{
                    'attachment':{
                        'type':typemedia,
                        'payload':{
                            'url':url,
                            'is_reusable':'true'
                        }
                    }
                }
            }
        else:
            message = {
                'recipient':{
                    'id':userid
                },
                'message':{
                    'attachment':{
                        'type':typemedia,
                        'payload':{
                            'attachment_id':attachment_id
                        }
                    }
                }
            }
    sendmessage(message)

"""
Decompose the Hell Jayson!
"""
def bring_me_args(body):
    """ Facebook input Handler """
    for eachmessage in body['entry']:
        messaging = eachmessage['messaging']
        for fbmessage in messaging:
            if fbmessage.get('message'):
                recipient_id = fbmessage['sender']['id']
                if fbmessage['message'].get('text'):
                    typedata = 'text'
                    userinput = fbmessage['message']['text']
                if fbmessage['message'].get('is_echo'):
                    typedata = 'echo'
                if fbmessage['message'].get('attachments'):
                    typedata = 'attachments'
                    for att in fbmessage['message'].get('attachments'):
                        userinput = att['payload']['url']
                if fbmessage['message'].get('quick_reply'):
                    typedata = 'quick_reply'
                    userinput = fbmessage['message']['quick_reply']['payload']
                if fbmessage['message'].get('sticker_id'):
                    stickerid = fbmessage['message']['sticker_id']
                else:
                    stickerid = None
            elif fbmessage.get('postback'):
                recipient_id = fbmessage['sender']['id']
                if fbmessage['postback'].get('payload'):
                    typedata = 'postback'
                    userinput = fbmessage['postback']['payload']
                if fbmessage['postback'].get('referral'):
                    typedata = 'ref'
                    userinput = fbmessage['postback']['referral']['ref']
            else:
                typedata = ''
                userinput = ''
    return recipient_id, typedata, userinput, stickerid

"""
Verify the mutfcker Token!
"""
def verify_token(hubverify_token, hubchallenge):
    """ Verify Facebook Token """
    if hubverify_token == VERIFY_TOKEN:
        return hubchallenge
    else:
        return "Invalid verification token"

"""
Send the mutfcker text!
"""
def sendtext(userid, text):
    message = {
        'recipient':{
            'id':userid
            },
        'message':{
            'text':text
        }
    }
    sendmessage(message)

"""
Guess what!
"""
def sendmessage(message):
    params = {
        'access_token': TOKEN
        }
    #print json.dumps(message)
    response = requests.post(
        '%s/messages' % FACEHOOKURL,
        params=params,
        json=message
    )
    if response.status_code != 200:
        print response.json()

