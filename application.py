import skype_chatbot
import os
import json
from flask import Flask, request
app = Flask(__name__)

app_id = "ed163f1f-e7ce-4940-bda9-e5e1987aab72" 
app_secret = "B3ZRkqum-a3WdU3*grM2NInP@FH*ay8z" 


bot = skype_chatbot.SkypeBot(app_id, app_secret)

@app.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux {}".format(os.environ.get('APP_ID'))

@app.route('/api/messages', methods=['POST', 'GET'])
def webhook():
    try:
        ml
    except NameError:
        from train import Train
        ml = Train()
        ml.start()
    answer = ''    
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            bot_id = data['recipient']['id']
            bot_name = data['recipient']['name']
            recipient = data['from']
            service = data['serviceUrl']
            sender = data['conversation']['id']
            text = data['text']

            bot.send_message(bot_id, bot_name, recipient, service, sender, 'You said: "{}" and my answer: "{}"'.format(text, ml.answer(text)))
        except Exception as e:
            print(e)
    if request.method == 'GET':
        question = request.args.get('q');
        answer = ml.answer(question if question else 'Hi');
    return 'Code: 200. {}'.format(answer)

@app.route('/api/train', methods=['GET'])
def train():
    from train import Train
    ml = Train()
    try:
        ml.training()
        return "Train is completed"
    except Exception as e:
        return "Traing is failed {}".format(str(e))
