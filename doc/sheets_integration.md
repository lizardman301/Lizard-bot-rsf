# Lizard-BOT integration with Challonge and Google Sheets

Lizard-BOT uses 2 different APIs to help obtain data used for various functions
1. [Challonge API](https://api.challonge.com/v1)
2. [Google Sheets API](https://developers.google.com/sheets/api)

Getting the bot to use both these tools requires some hidden files containing API authentication info
This guide purpose is to explain how to obtain API authentication info and where to store it

## Challonge

Start with Challonge. It's simpler.

### 1. Getting API access

Time to get started with Google
1. Create Challonge account for the bot
2. Go to account dropdown in the upper right and choose 'Settings'
3. Click on the 'Developer API' tab
4. Generate a new API key (Do ***NOT*** share this with anybody or accidentally upload it to a public git repo)

### 2. Adding API key to the program

Account created, API key obtained. Now, put it to use
Lizard-BOT has a non-upload file call secret.py in the bot\ folder
1. Edit bot\secret.py
2. Add 'api_key ="INSERT API KEY" to the file
3. Save file

#### That's it for adding Challonge API 

## Google Sheets API

Big Google gets a little complicated but still not super difficult

### 1. Getting API access

Time to get started with Google
1. Create Google account for the bot
2. Go to <https://console.developers.google.com/apis/dashboard> and accept the Terms and Conditions
3. Create a new project and name it appropriately
4. Click on 'Enable APIs and Services'
5. Search for 'Google Sheets API'
6. Click on it and then, enable the Google Sheets API

### 2. Creating a Service account

Time to make an account to use the API
1. Go to APIs & Service > Credentials
2. Click on Create Credentials > Service Account
3. Name it appropriately. Do **NOT** add any permissions or user access
4. Click Done

### 2. Adding Service Account to the program

The Service account has been created. Time to use it
1. Edit the new service account
2. Create a new key in JSON format
3. Save file as 'credentials.json'
4. Store file in the bot\commands\sheets\ folder

#### Google Sheets API is done

### That's all the integration needed! Good Job!