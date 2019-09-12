import skype_chatbot
import os
import json
from prediction import Prediction
from train import Train
from flask import Flask, request
app = Flask(__name__)

# APP_ID, APP_SECRET are usually set via enviroment settings if you run it on your local 
# or app settings if you run in in azure  app service
app_id = os.environ.get('APP_ID')
app_secret = os.environ.get('APP_SECRET')
MODEL_DIR = os.environ.get('MODEL_DIR')
intents_file = "intents.json"
ml_prediction = Prediction(MODEL_DIR)

# skype_chatbot is used for simply reason. Should consider to use MS botbuilder for more features
# Refer to https://github.com/microsoft/botbuilder-python/blob/master/samples/06.using-cards/bots/rich_cards_bot.py
bot = skype_chatbot.SkypeBot(app_id, app_secret)

@app.route("/")
def hello():
    # To test whether the service is up and running
    return "Hello Flask, on Azure App Service for Linux {}".format(app_id)


@app.route('/api/messages', methods=['POST', 'GET'])
def webhook():
    # This is usually the main entry point to you chat bot which is called by Bot Chanels via POST method
    # However, GET is supported for testing purpose.
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

            bot.send_message(bot_id, bot_name, recipient, service, sender, 
                ml_prediction.response(text, sender))
        except Exception as e:
            print(e)
    if request.method == 'GET':
        question = request.args.get('q')
        answer = ml_prediction.response(question if question else 'Hi')
    return 'Code: 200. {}'.format(answer)

@app.route('/api/train', methods=['GET'])
def train():
    # Call api/train to train your bot with default intents.json. 
    # You can use different intents file by upload them manaully to server, then passing file name via param file.
    # For example: api/train?file=intents1.json
    input_file = request.args.get('file')
    intents_file = input_file if input_file else "intents.json"
    ml = Train(intents_file, MODEL_DIR)
    try:
        ml.training()
        ml_prediction.load_model()
        return "Train is completed"
    except Exception as e:
        return "Traing is failed {}".format(str(e))
