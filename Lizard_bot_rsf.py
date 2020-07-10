import discord
import asyncio
from threading import Timer
from discord.ext import commands
import re
# Cleaned up what imports I knew

import pymysql.cursors # Use for DB connections
from random import random # Use to generate random numbers
from secret import sql_host,sql_port,sql_user,sql_pw,sql_db,bot # Store secret information

client = discord.Client()

def makebold(s):
    return "**" + s + "**"

def ping_be_gone(list, guild):
    #for the list passed, it will return a list with any pings replaced with text of the ping instead
    #needs guild passed too so that it can return the equivalent nick/role names
    user_reg = '<@!\d*>'
    role_reg = '<@&\d*>'

    for i, x in enumerate(list):
        u_pings = re.fullmatch(user_reg,x)

        #match found for user pings
        if u_pings:
            #grab id and replace
            m = re.search('\d+',x)
            id = m.group(0)
            user = guild.get_member(int(id))
            #replace with nickname
            list[i] = user.display_name
            continue
       
        r_pings = re.fullmatch(role_reg,x)

        #match found for role pings
        if r_pings:
            #grab id and replace
            m = re.search('\d+',x)
            id = m.group(0)
            role = guild.get_role(int(id))
            #replace with name of role
            list[i] = role.name
            continue

    #return new list with now pings
    return list

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
def settings_exist(guild_id, chan_id):
    conn = make_conn() # Make DB connection

    try:
        with conn.cursor() as cursor:
            for level in ['guild','channel']:
                ids = [] # Store a list of all ids
                id = guild_id if level == 'guild' else chan_id # Set variable id based on what level of setting

                # Select all IDs in the DB for the given level
                sql = "SELECT " + level + "_id FROM " + level + "s"
                cursor.execute(sql)
                for row in cursor:
                    ids.append(row[level + '_id']) # Add IDs to the list

                # If the ID is not in the list
                # Add the ID to the guild/channel table
                # Add the ID to the guild/channel_settings table (This will initialize the default values)
                if id not in ids:
                    sql = "INSERT INTO " + level + "s (" + level + "_id) VALUES (%s)"
                    cursor.execute(sql, (id,))
                    
                    sql = "INSERT INTO " + level + "_settings (" + level + "_id) VALUES (%s)"
                    cursor.execute(sql, (id,))
    finally:
        conn.close() # Close the connection

    return 1 # Return truthy value for checking

# Read a setting from database for a given guild/channel
def read(level, setting, id):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Select the desired setting from the DB for the given guild/channel
            sql = "SELECT " + setting + " FROM " + level + "_settings WHERE " + level + "_id = %s"
            cursor.execute(sql, (id))
            return cursor.fetchone()[setting] # Return the value for the setting
    finally:
        conn.close() # Close the connection

# Save a setting for a given guild/channel to the database
def save(level, setting, data, id):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Update the desired setting in the DB for the given guild/channel
            sql = "UPDATE " + level + "_settings SET " + setting + " = %s WHERE " + level + "_id = %s"
            cursor.execute(sql, (data, id))
    finally:
        conn.close() # Close the connection

# Format the status message
# This is because there was two spots that did this and copypasta was too much
def round_msg(currentRound, chan_id):
    if currentRound:
            # Read the status message for a channel and make it bold
            # Currently the message must have {0} so it can fill in the current round
            return makebold(read('channel', 'status', chan_id).format(currentRound))
    else:
        return makebold("Tournament has not begun. Please wait for the TOs to start Round 1!")

# Returns a coin flip
def flip():
    if (int(round(random()*10*2)) % 2) == 0:
        return "Heads" # Return terminates the function so no need for an else block
    return "Tails"

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    chan = message.channel # Makes it easier to send 
    chan_id = chan.id # Channel ID to make it easier to grab
    guild_id = message.guild.id

    # Check if the channel is in the DB
    # Add it if it isn't
    if not settings_exist(guild_id, chan_id):
        await chan.send("Oops, I'm broken")
        print("Oops, I'm broken")

    prefix = read('guild', 'prefix', guild_id) # Get prefix for the channel

    regexs = {'can we play':round_msg(read('channel', 'round', chan_id), chan_id), 'checking in':makebold('MAKE SURE TO CHECK IN ON CHALLONGE')}
    for regex in regexs:
        p = re.compile(regex+'.*')
        #check for "can we play" in a message
        results = p.fullmatch(message.content.lower())
        if results:
            await chan.send(regexs[regex])

    if not message.content.startswith(prefix):
        return

    # Double slice to lower to save lines
    # Help people accidentally typing caps
    command = message.content.split(' ')[0][1:].lower()

    if len(message.content.split(' ')) > 1:
        params = message.content.split(' ')[1:]

        # If the command isn't edit
        # Strip the @
        if command not in 'edit':
            params = ping_be_gone(params,message.guild)
    else:
        # Empty list if no parameters
        params = []

    bot_role = read('guild', 'bot_role', guild_id) # Grab the role id that should have access to the administrative commands

    # If no bot_role specified (like a new channel)
    # Set bot_role equal to @everyone
    if not bot_role:
        for role in message.author.roles:
            if role.name == '@everyone':
                bot_role = role.id
                break

    # Administrative commands
    if bot_role in [y.id for y in message.author.roles]:
        # Print the name of the bot role
        if command == 'bot_role':
            # The role id # means little to people
            # Do some logic to check the author roles to find
            # the bot role id and the name associated with it
            for role in message.author.roles:
                if role.id == bot_role:
                    await chan.send("The bot_role is {0}".format(makebold(role.name)))
                    break

        # Print the prefix for lizardbot
        elif command == 'prefix-lizard':
            await chan.send("The prefix is {0}".format(makebold(read('guild', 'prefix', guild_id))))

        elif command == 'coin-flip':
            await chan.send("The coin landed on: {0}".format(flip()))

        #reset round to 0
        elif command == "reset":
            await chan.send("Resetting round count...")
            print("Round count reset.")

            # Save current round to an empty string
            save('channel', 'round', "", chan_id)

        #set what round winners can play
        elif command == "round":
            if len(params) < 1:
                await chan.send("Usage: !round <round number>")
            else:
                # Save round
                save('channel', 'round', " ".join(params), chan_id)
                print("Round is now {0}".format(" ".join(params)))

                # Display the round message
                await chan.send(round_msg(read('channel', 'round', chan_id), chan_id))

        #annoy people to refresh brackets
        elif command == "refresh":
            await chan.send(makebold("REFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS"))

        #remind message author after a certain period of time (minutes)
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

            # sends message back to confirm reminder
            await message.channel.send(msg)
            print("Reminding {0} in {1} minutes for {2}...".format(user,time,reason))

            # wait message time
            await asyncio.sleep(60 * time)
            if len(reason) == 0:
                msg = makebold("{0} its been {1} minutes, you have been reminded!".format(user.mention,time))
            else:
                msg = makebold("{0} its been {1} minutes, don't forget \"{2}\"!").format(user.mention,time,reason)

            await chan.send(msg)
            print("{0} has been reminded after {1} minutes.".format(user,time))

        # Allows the TOs to edit certain messaging
        elif command == "edit":
            editable_command = params[0].lower() # lower the command we are editing
            
            # Grab just the BigInt part of bot_role
            if editable_command == 'bot_role':
                params[1] = str(message.role_mentions[0].id)

            new_msg = ' '.join(params[1:]) # Rejoin the rest of the parameters with spaces

            # If editable command is a guild command, save to guild settings
            # Else save to channel_settings
            if editable_command in ['bot_role','prefix']:
                save('guild', editable_command, new_msg, guild_id) # Save the new message to the proper setting in a given guild
            else:
                save('channel', editable_command, new_msg, chan_id) # Save the new message to the proper setting in a given channel

            # Remove the bot pinging TOs on the confirmation message
            if editable_command in ['tos']:
                new_msg = ' '.join(ping_be_gone(params[1:], message.guild)) # Remove the bot pinging the TO

            await chan.send("The new {0} is: {1}".format(makebold(editable_command), makebold(new_msg))) # Print the new message for a given setting

    #General use commands
    if command == "lizardman":
        print("Pinged by {0}".format(message.author))
        await chan.send("Fuck you, Lizardman")

    #allows players to see what round it was
    elif command == "status":
        # Get the current round
        await chan.send(round(read('channel', 'round', chan_id), chan_id))

    elif command == "stream":
        # Read the stream message for a channel
        await chan.send(read('channel', command, chan_id))

    # Ping the TO for the current channel
    elif command == "tos":
        # Read users/roles to ping
        tos = read('channel', command, chan_id)

        # If read() return a truthy value
        # Set message equal to value
        # Else print default message
        if tos:
            msg = tos
        else:
            msg = "Oops, there is no TO associated with this channel. Please try somewhere else."
        await chan.send(msg)

    #lists all commands
    elif command == "help-lizard":
        await chan.send("For more information about the bot and its commands: https://github.com/lizardman301/Lizard-bot-rsf")

# Have the bot listen for commands
client.run(bot)