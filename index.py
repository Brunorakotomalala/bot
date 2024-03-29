import os
import json
import requests

from flask import Flask, request

app = Flask(__name__)

FB_ACCESS_TOKEN = 'EAAItsfpuIEkBAIZBoW8bqJnRU89GxgViqnoOTA2tANKItTxsNkx4foFcZAdlZB4rKY6A1jNbwM3WWE15emaTvZA9gtXcpAkagyghhvOZCdTSiivfF4ZCPqx0lfffg501WbPGMSFMrAuJ0wZBFmH3d3Tho9JPxQRC93OFMSwDlii39ELAVIQLUwY'
FB_VERIFY_TOKEN = 'Bruno'
FB_API_URL = f"https://graph.facebook.com/v10.0/me/messages?access_token={FB_ACCESS_TOKEN}"

@app.route('/', methods=['GET'])
def verify_fb_token():
    if request.args.get('hub.verify_token') == FB_VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else:
        return 'Invalid verification token'

@app.route('/', methods=['POST'])
def webhook():
    message_data = request.get_json()
    for message_entry in message_data['entry']:
        for message_event in message_entry['messaging']:
            if 'message' in message_event:
                sender_id = message_event['sender']['id']
                message_text = message_event['message']['text']
                send_message(sender_id, message_text)
    return 'Message processed'

def send_message(recipient_id, message_text):
    message_data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    message_headers = {'Content-Type': 'application/json'}
    requests.post(FB_API_URL, headers=message_headers, data=json.dumps(message_data))

if __name__ == '__main__':
    app.run(port=5000)
