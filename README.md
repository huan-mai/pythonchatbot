# pythonchatbot

## Requirements
You need python 3.6 or 3.7 and pip

### How to run
1. pip install -r requirement.txt
2. pip install flask
3. On Mac: `FLASK_APP=application.py flask run`. On Window: `set FLASK_APP=application.py && flask run` 
4. Then go to http://localhost:5000/api/train to train data
5. http://localhost:5000/api/messages?q=Hi to test
6. You can use MS Bot Framework Emulator to test it as well.

### How to deploy it to Azure
1. Create Azure account. You will need valid credit card for it.
2. Create resource group: e.g. "BotGroup"
3. Create **[Bot Channels Registration](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-registration?view=azure-bot-service-3.0)**
4. Get **APP_ID** and **APP_SECRET** from **Bot Channels' Settings** under Microsoft App Id.
5. Create **App Service** with python
6. Use **Deployment Center** and select your source code from github
7. Select **App Service build service**
8. Add **APP_ID** and **APP_SECRET** to **Configuration > Application settings > New application setting**
9. Go back to **Bot Channels' Settings** and update Endpoint URL e.g. https://pythonchatbot.azurewebsites.net/api/messages

