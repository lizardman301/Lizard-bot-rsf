# How to setup bot
If you are trying to just use Lizard-bot as a Tournament organizer, check __ for more info to invite and use Lizard-bot.

If you wish to use the code to setup your own bot for testing or whatever, this is the file for you.

## 0. Preperation
Bot is currently running on a Ubuntu machine so this will be written assuming you are using that.
Make sure the newest version of python is installed (bot is on 3.8.6 currently), mariadb, and git.
For python packages, pip install discord.py and pymysql.
On the discord end, create a new application [here](https://discord.com/developers/applications) name it what you want.
In the bot sub-menu, enable member intent so you can fully use the challonge features

![Member Intent Screen](/doc/assets/images/member_intent.png)

## 1. Clone the Repository
In the command line type:
```
git clone https://github.com/lizardman301/Lizard-bot-rsf
```
and clone the repository.

## 2. Setup database
CD into the repository and open mariadb and type:
```
source /sql/create_db.sql
```
This will create a database with all of the fields needed. You will need to make sure the bot can actually login as root into the database.  There are a few ways to set this up (google is your friend here), but for this project I created a DB_user with the system_user. Do whatever works best and if it doesn't work, google the error messages for connecting to the DB to find a solution.

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
Create a file named secret.py and play it in the the bot folder with the following info changed to match your specific needs.  You can grab your discord token from your bot application [here](https://discord.com/developers/applications) and your challonge key [here](https://challonge.com/settings/developer).


## 5. Invite the bot to servers and run
With secret.py setup, you should be ready to start the bot.  First it needs to be in a server. Go back to the [Discord developer page](https://discord.com/developers/applications), click on your bot and click on the OAuth2 tab.

![OAuth2 Screen](/doc/assets/images/OAuth2_tab.png)

Click on the bot check box and scroll down. Click on all permissions necessary. The image below shows what settings Lizard-bot uses, but feel free to change them for your intended purposes.

![OAuth2 Screen](/doc/assets/images/bot_permissions.png)

Then go back to the OAuth screen and open the url to add to your server! Once it is in, make sure to set it up properly (use __ as a reference) in the server, and you now have a new version of Lizard-bot to test with!