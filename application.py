import skype_chatbot
import os
import json
from flask import Flask, request
app = Flask(__name__)

app_id = "118ff51a-f3d7-4fc3-b47e-b6b60fb0af8b" 
app_secret = "RWJ5HrlRe-oteY[HCfQBFZd8B]0zA1u+" 

bot = skype_chatbot.SkypeBot(app_id, app_secret)

@app.route("/")
def hello():
        return "Hello Flask, on Azure App Service for Linux {}".format(os.environ.get('APP_ID'))

@app.route('/api/messages', methods=['POST', 'GET'])
def webhook():
    from train import Train
    ml = Train()
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            bot_id = data['recipient']['id']
            bot_name = data['recipient']['name']
            recipient = data['from']
            service = data['serviceUrl']
            sender = data['conversation']['id']
            text = data['text']

            ml.start()
            bot.send_message(bot_id, bot_name, recipient, service, sender, 'You said: "{}" and my answer: "{}"'.format(text, ml.answer(text)))

        except Exception as e:
            print(e)

    return 'Code: 200'

@app.route('/api/train', methods=['GET'])
def train():
    from train import Train
    ml = Train()
    try:
        ml.training()
        return "Train is completed"
    except:
        return "Traing is failed"
