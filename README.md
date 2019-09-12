# pythonchatbot

## Requirements
You need python 3.6 or 3.7 and pip

### How to run
1. pip install -r requirements.txt
2. pip install flask
3. On Mac: `FLASK_APP=application.py flask run`. On Window: `set FLASK_APP=application.py && flask run` 
4. Then go to http://localhost:5000/api/train to train data
5. http://localhost:5000/api/messages?q=Hi to test
6. You can use MS Bot Framework Emulator to test it as well. Use URL: http://localhost:5000/api/messages to connect if you want to test it locally.

### How to deploy it to Azure

#### Manual steps:
1. Create Azure account. You will need valid credit card for it.
2. Create resource group: e.g. "BotGroup"
3. Create **[Bot Channels Registration](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-registration?view=azure-bot-service-3.0)**
4. Get **APP_ID** and **APP_SECRET** from **Bot Channels' Settings** under Microsoft App Id.
5. Create **App Service** with python
6. Use **Deployment Center** and select your source code from github
7. Select **App Service build service**
8. Add **APP_ID** and **APP_SECRET** to **Configuration > Application settings > New application setting**
9. Go back to **Bot Channels' Settings** and update Endpoint URL e.g. https://pythonchatbot.azurewebsites.net/api/messages

#### Automation steps via Azure CLI:
1. Install azure-cli
2. az login
3. open az_deploy.sh and update **gitrepo, webappname and group**
```
gitrepo=https://github.com/huan-mai/pythonchatbot/
webappname=pythonchatbot1
group=BotGroup1
```
4. chmod +x ./az_deploy.sh
5. ./az_deploy.sh

### Troubleshooting
1. If you get `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed` error when running `pip install` command, download the pem file from http://curl.haxx.se/ca/cacert.pem, then run the command with `--cert` parameter. Example: `pip --cert /path/to/cacert.pem install linkchecker`
(Reference: https://stackoverflow.com/questions/25981703/pip-install-fails-with-connection-error-ssl-certificate-verify-failed-certi/26062583)
