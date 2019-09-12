#!/bin/bash

# Replace the following URL with a public GitHub repo URL
gitrepo=https://github.com/huan-mai/pythonchatbot/
webappname=pythonchatbot1
group=BotGroup1
loc=eastasia

# Create a resource group.
az group create --location $loc --name $group

# Create an App Service plan in `FREE` tier.
az appservice plan create --name $webappname --location $loc --resource-group $group --sku FREE --is-linux

# Create a web app.
#az webapp create --name $webappname --resource-group $group --plan $webappname --runtime "python|3.6"

az webapp config appsettings set -g $group -n $webappname --settings APP_ID= APP_SECRET= WEBSITE_HTTPLOGGING_RETENTION_DAYS=1

# Deploy code from a public GitHub repository. 
az webapp deployment source config --name $webappname --resource-group $group \
--repo-url $gitrepo --branch context --manual-integration

az webapp config set --resource-group $group --name $webappname --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 application:app"

# Copy the result of the following command into a browser to see the web app.
echo http://$webappname.azurewebsites.net
