import discord
import asyncio
from threading import Timer
from discord.ext import commands
# Cleaned up what imports I knew

import pymysql.cursors # Use for DB connections
from secret import sql_host,sql_port,sql_user,sql_pw,sql_db,bot # Store secret information

client = discord.Client()

prefix = '\\' # My test server has a carl-bot with !/? prefixes

def makebold(s):
    return "**" + s + "**"

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('-------------------------------')

# Create a connection to the database
def make_conn():
    return pymysql.connect(host=sql_host, port=sql_port, user=sql_user, password=sql_pw, db=sql_db, charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

# Check if the channel is in the table
# If not, add it the channels and settings tables
# chan_id int channel ID
def settings_exist(chan_id):
    conn = make_conn() # Make DB connection
    channels = [] # Store a list of our channels

    try:
        with conn.cursor() as cursor:
            # Select all channel IDs in the DB
            sql = "SELECT chan_id FROM channels" 
            cursor.execute(sql)
            for row in cursor:
                channels.append(row['chan_id']) # Add IDs to the list

            # If the ID is not in the list
            # Add the ID to the channels table
            # Add the ID to the settings table (This will initialize the default values)
            if chan_id not in channels:
                sql = "INSERT INTO channels (chan_id) VALUES (%s)"
                cursor.execute(sql, (chan_id,))
                
                sql = "INSERT INTO settings (chan_id) VALUES (%s)"
                cursor.execute(sql, (chan_id,))
    finally:
        conn.close() # Close the connection

    return 1 # Return truthy value for checking

# Read a setting from database for a given chanel
def read(setting, chan_id):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Select the desired setting from the DB for the given channel
            sql = "SELECT " + setting + " FROM settings WHERE chan_id = %s"
            cursor.execute(sql, (chan_id))
            return cursor.fetchone()[setting] # Return the value for the setting
    finally:
        conn.close() # Close the connection

def save(setting, data, chan_id):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Update the desired setting in the DB for the given channel
            sql = "UPDATE settings SET " + setting + " = %s WHERE chan_id = %s"
            cursor.execute(sql, (data, chan_id))
    finally:
        conn.close() # Close the connection

@client.event
async def on_message(message):
    chan_id = message.channel.id
    
    # Check if the channel is in the DB
    # Add it if it isn't
    if not settings_exist(chan_id):
        msg ="Oops, I'm broken"
        print(msg)

    # Get the current round
    currentRound = read('round', chan_id)

    if message.author == client.user:
        return

    if not message.content.startswith(prefix):
        return

    # Double slice to save a line
    command = message.content.split(' ')[0][1:]
    
    if len(message.content.split(' ')) > 1:
        params = message.content.split(' ')[1:]
    else:
        #create empty list
        params = [];

    #TO only commands
    if "TOs" in [y.name for y in message.author.roles]:
        #reset round count to 0
        if command == "reset":
            msg = "Resetting round count..."

            print("Round count reset.")
            
            # Set current round to 0
            save('round', 0, chan_id)

        #set what round winners can play
        elif command == "round":
            if len(params) < 1:
                msg = "Usage: !round <round number>"
            else:
                currentRound = params[0]

                # Display the round message
                msg = makebold(read('round_msg', chan_id).format(currentRound))
                print("Round is now {0}".format(currentRound))
                
                # Save round
                save('round', currentRound, chan_id)

        #annoy people to refresh brackets
        elif command == "refresh":
            msg = makebold("REFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS")

        #remind message author after a ceratin period of time (minutes)
        elif command == "remind":
            #time is in minutes
            msg = ""
            time = int(params[0])
            reason = ""
            #specific reason if provided
            if len(params) > 1:
                r_list = params[1:]
                reason = " ".join(r_list)

            user = message.author
            if len(reason) == 0:
                msg = "OK! I will ping you in {0} minutes to remind you about something.".format(time)
            else:
                msg = "OK! I will ping you in {0} minutes to remind you about \"{1}\"".format(time,reason)

            print("Reminding {0} in {1} minutes for {2}...".format(user,time,reason))

            #wait message time
            await asyncio.sleep(60 * time)
            if len(reason) == 0:
                msg = makebold("{0} its been {1} minutes, you have been reminded!".format(user.mention,time))
            else:
                msg = makebold("{0} its been {1} minutes, don't forget \"{2}\"!").format(user.mention,time,reason)

            print("{0} has been reminded after {1} minutes.".format(user,time))

        # Allows the TOs to edit certain messaging
        elif command == "edit":
            # Edit params[0] to match the DB column name for the round message
            # Where possible match command names to the DB column names
            if params[0] == 'round':
                params[0]= 'round_msg'

            new_msg = ' '.join(params[1:]) # Rejoin the rest of the parameters with spaces
            save(params[0], new_msg, chan_id) # Save the new message to the proper setting in a given channel
            msg = "The new {0} message is: {1}".format(params[0],makebold(new_msg)) # Print the new message for a given setting

    #General use commands
    if command == "ping-lizard":
        msg = "Pong!"

    #allows players to see what round it was
    elif command == "status":
        if currentRound == 0:
            msg = makebold("Tournament has not begun. Please wait for the TOs to start Round 1!")
        else:
            # Read the status message for a channel and make it bold
            # Currently the message must have {0} so it can fill in the current round
            msg = makebold(read(command, chan_id).format(currentRound))

    elif command == "stream":
        # Read the stream message for a channel
        msg = read(command, chan_id)

    #lists all commands
    elif command == "help-lizard":
        msg = "Player commands ```\n{0}current-round``` \nTO commands ```{0}ping-lizard\n{0}refresh\n{0}remind <time> [reason] \n{0}reset \n{0}round <#> ```"

    # Send message to chat
    # Also removed from the end of every command block to cut down on repeated lines
    await message.channel.send(msg)

# Have the bot listen for commands
client.run(bot)
