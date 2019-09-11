# pythonchatbot

## Requirements
You need python 3.7 and pip

### How to run
1. pip install -r requirement.txt
2. pip install flask
3. FLASK_APP=application.py flask run
4. Then go to http://localhost:5000/api/train to train data
5. http://localhost:5000/api/messages?q=Hi to test
6. You can use MS Bot Framework Emulator to test it as well.

### How to deploy it to Azure
1. Create Azure account
2. Create resource group: e.g. "BotGroup"
3. Create Bot Channels Registration
4. get APP_ID and APP_SECRET from Bot Channels Registration's settings under Microsoft App Id.
5. Create 'App Service' with python
6. Use 'Deployment Center' and select github
7. Select 'App Service build service'
8. Add APP_ID and APP_SECRET to 'Configuration > Application settings > New application setting'
