# How to setup bot
If you are trying to just use Lizard-BOT as a Tournament organizer, check [here](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/setting_up_bot_in_discord.md) for more info to invite and use Lizard-BOT.

If you wish to use the code to setup your own bot for testing or whatever, this is the documentation for you.

## 0. Preparation
The bot is currently running on a Ubuntu machine. This will be written with an assumption you are using the same operating system. Adapt as needed for other OSes
Make sure the newest version of Python is installed (bot is on 3.8.6 currently), MariaDB, and git.
For Python packages, pip install discord.py and PyMySQL.
On the Discord end, create a new application [here](https://discord.com/developers/applications) name it what you want.
In the bot sub-menu, enable member intent so you can fully use the Challonge features

![Member Intent Screen](/doc/assets/images/member_intent.png)

## 1. Clone the Repository
In the command line type:
```
git clone https://github.com/lizardman301/Lizard-bot-rsf
```
and clone the repository.

## 2. Setup database
Change your directory into the repository and open MariaDB and type:
```
source /sql/create_db.sql
```
This will create a database with all of the fields needed. Make sure the bot can actually login with full write and read for the newly created database. There are a few ways to set this up (Google is your friend here), but for this project I created a DB_user with the system_user. Do whatever works best and if it doesn't work, Google the error messages for connecting to the DB to find a solution.

## 4. Setup secret.py
In order to use this bot you will need to create a 'secret.py' with a few bits of data.
A template for it is as follows:
```python
sql_host = "localhost" # DB Server address. localhost will be the machine running the script
sql_port = 3306 # DB Server port. Default is 3306
sql_user = "root" # SQL user. root or admin work.
sql_pw = "" # SQL user's password
sql_db = "lizardbot" # DB to access. `lizardbot` is the DB 'create_db.sql' script creates
token="your-discord-token-here" # Discord Bot token
api_key="your-challonge-key-here" # Challonge api key
```
Create a file named secret.py and place it in the the /bot folder with the following info changed to match your specific needs.  You can grab your Discord token from your bot application [here](https://discord.com/developers/applications) and your Challonge key [here](https://challonge.com/settings/developer).
For more info on setting up API integration with Challonge (or Google Sheets), please review [this](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/api_integration.md)


## 5. Invite the bot to servers and run
With secret.py setup, you should be ready to start the bot. First it needs to be in a server. Go back to the [Discord developer page](https://discord.com/developers/applications), click on your bot and click on the OAuth2 tab.

![OAuth2 Screen](/doc/assets/images/OAuth2_tab.png)

Click on the bot check box and scroll down. Click on all permissions necessary. The image below shows what settings Lizard-BOT uses, but feel free to change them for your intended purposes.

![OAuth2 Screen](/doc/assets/images/bot_permissions.png)

Then go back to the OAuth screen and open the URL to add to your server! Once it is in, make sure to set it up properly (use [this](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/setting_up_bot_in_discord.md) as a reference) in the server, and you now have a new version of Lizard-BOT to test with!