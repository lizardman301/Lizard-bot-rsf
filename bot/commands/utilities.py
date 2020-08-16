from discord.utils import escape_markdown # Regexing fun simplified
import pymysql.cursors # Use for DB connections
import re # Process strings
import requests # HTTP functions

# Local imports
from secret import (sql_host,sql_port,sql_user,sql_pw,sql_db, api_key) # Store secret information
from commands.sheets.sheets import sheets # Talk to Google Sheets API

_callbacks = {} # Yaksha

# Yaksha
def register(command):
    '''
    _Registers_ each function with by storing the command its name
    into a dict.
    '''
    def decorator(func):
        print('Registering %s with command %s' % (func.__name__, command))
        _callbacks[command] = (func.__qualname__, func.__module__)
        return func
    return decorator

# Yaksha
def get_callbacks():
    '''
    Simple getter that returns the dictionary containing
    the registered functions. Might be better to make
    registration into a class instead.
    '''
    return _callbacks

# Add Markdown for bold
def bold(string):
    return "**" + string + "**"

# Get all users in a Discord
def get_users(msg):
    users = msg.guild.members
    userDict = {}

    # Get their distinct name and their nickname
    for user in users:
        userDict.update({user.name + '#' + str(user.discriminator): user.display_name.lower()})

    return userDict

# Perform regex to find out if a string is a Discord channel
def is_channel(channel):
    reg = re.compile('<#\d*>')
    if reg.fullmatch(channel):
        return int(channel[2:][:-1]) # Return only the channel ID
    return 0

# Simplify removing pings more
def pings_b_gone(mentions):
    mention_list = {} # Empty dict to store values in

    # For each mention, get the name and the mention value
    for mention in mentions:
        # Check for nickname
        if mention.display_name:
            mention_list.update({mention.display_name: mention.mention})
            continue
        mention_list.update({mention.name: mention.mention})

    return mention_list

def checkin(parts, users):
    not_discord_parts = [] # Used for people missing from the server
    not_checked_in_parts = [] # Used for people not checked in
    match_md = r'((([_*]).+?\3[^_*]*)*)([_*])'

    # Check each participant to see if they are in the server and checked in
    for p in parts:
        p = p['participant']

        # If participant not checked in, add them to the bad list
        if not p['checked_in']:
            not_checked_in_parts.append(escape_markdown(p['name']))

        # If participant not in the Discord, add them to the bad list
        if p['name'].lower() not in users.values() or p['challonge_username'].lower() not in users.values():
            not_discord_parts.append(escape_markdown(p['name']))

    return not_checked_in_parts, not_discord_parts

def seeding(sheet_id, parts, url, seed_num):
    player_points = [] # Stores "player point_value" for sorting later

    # Get dict of associated players and their points
    players_to_points = sheets(sheet_id)
    
    if isinstance(players_to_points, str):
        return players_to_points

    # Check each participant and if they have points
    for p in parts:
        p = p['participant']

        # If player has points, add to list for later sorting
        if p['challonge_username'] in players_to_points:
            player_points.append(p['challonge_username'] + ' ' + players_to_points[p['challonge_username']])

    # Players are listed by highest points and then alphabetically
    # Truncated by how many we are seeding
    # First sort is done on the player name, players with names higher in the alphabet win ties
    # Second sort is done on the point value
    player_points = sorted(sorted(player_points, key=lambda part: part.split(' ')[0].lower()), key=lambda part: int(part.split(' ')[1]), reverse=True)[0:seed_num if 0 < seed_num <= len(player_points) else len(player_points)]

    # Associate seeding number with the player
    finished_seeding ={}
    for x in range(len(player_points)):
        finished_seeding.update({x+1: player_points[x]})

    # Check if player is in sorted, truncated list and update their seed number
    for p in parts:
        p = p['participant']

        for player in finished_seeding:
            # If Challonge user equals the username we have for seeding
            # Then, update seed number with their index location
            if p['challonge_username'] == finished_seeding[player].split(' ')[0]:
                response = requests.put(url + "/participants/" + str(p['id']) + ".json", params={'api_key':api_key, 'participant[seed]':player})
                if '401' in str(response.status_code):
                    return "Lizard-BOT does not have access to that tournament"

    # Return seeding list
    return finished_seeding

# Create a connection to the database
def make_conn():
    return pymysql.connect(host=sql_host, port=sql_port, user=sql_user, password=sql_pw, db=sql_db, charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

# Check if the guild/channel is in the table
# If not, add it the guilds, channels, and settings tables
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
    except Exception:
        return 0 # Falsy value to fail
    finally:
        conn.close() # Close the connection

    return 1 # Return truthy value for checking

# Read a setting from database for a given guild/channel
def read_db(level, setting, id):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Select the desired setting from the DB for the given guild/channel
            sql = "SELECT `" + setting + "` FROM " + level + "_settings WHERE " + level + "_id = %s"
            cursor.execute(sql, (id))
            return cursor.fetchone()[setting] # Return the value for the setting
    finally:
        conn.close() # Close the connection

# Save a setting for a given guild/channel to the database
def save_db(level, setting, data, id, **kwargs):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Update the desired setting in the DB for the given guild/channel
            if kwargs:
                id = kwargs['commandChannel']
            sql = "UPDATE " + level + "_settings SET `" + setting + "` = %s WHERE " + level + "_id = %s"
            cursor.execute(sql, (data, id))
    finally:
        conn.close() # Close the connection