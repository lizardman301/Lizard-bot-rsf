import tormysql

from discord.utils import escape_markdown # Regexing fun simplified
from pymysql import connect as pymysql_connect # Use for DB connections
from pymysql.cursors import DictCursor as pymysql_DictCursor # Use for DB connections
from json import loads as json_loads, dumps as json_dumps
from os import path as os_path
from re import search as re_search, compile as re_compile # Process strings
from requests import put as requests_put # HTTP functions

# Local imports
from secret import (sql_host,sql_port,sql_user,sql_pw,sql_db, api_key, chal_user) # Store secret information
from commands.sheets.sheets import sheets # Talk to Google Sheets API

_callbacks = {} # Yaksha

# DB connection pool for every individual connection to the DB
pool = tormysql.ConnectionPool(
    max_connections = 30, #max open connections
    idle_seconds = 60, #connection idle timeout time, 0 is not timeout
    wait_connection_timeout = 10, #wait connection timeout
    host = sql_host,
    port = sql_port,
    user = sql_user,
    passwd = sql_pw,
    db = sql_db,
    cursorclass=tormysql.cursor.DictCursor,
    autocommit=True,
    charset = "utf8"
)

# Yaksha
def register(command):
    '''
    _Registers_ each function with by storing the command its name
    into a dict.
    '''
    def decorator(func):
        print('Registering %s with command %s' % (func.__name__, command))
        #print('Qual name: %s | Module: %s' % (func.__qualname__, func.__module__))
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

def get_chal_tour_id(bracket_msg):
    # designed to return the tournament identifier if it exists in the database bracket text
    # returns empty string otherwise
    regex = r"[-a-zA-Z0-9@:%._\+~#=]{0,256}\.?challonge\.com\/[a-zA-Z0-9_]+" # regex for <community_url>.challonge.com/<tournament identifier> or challonge.com/<tournament identifier>
    url = ""
    tour_id = ""

    # find first match and make that the url to work off of
    # if no match, return empty string immediately
    matches = re_search(regex, bracket_msg) 
    if matches:
        url = matches.group(0)
    else:
        raise Exception("No bracket link set")

    # get the identifer from the back part of the url
    # should only be one slash so we split on that
    # get the last group in order to get the tournament identifier
    tour_id = url.split("/", 1)[-1]
    return tour_id # return it

def get_random_chars(game):
    rs_info = json_loads(open(os_path.join(os_path.dirname(__file__), 'rs.json')).read())
    games = list(rs_info.copy().keys())

    if game not in games:
        return [], games
    return rs_info.get(game, []).copy()[0:-1], games

# Get all users in a Discord
def get_users(users):
    userDict = {}

    # Get their distinct name and their nickname
    for user in users:
        userDict.update({user.name + '#' + str(user.discriminator): [user.display_name.lower(), user.mention]})

    return userDict

# Perform regex to find out if a string is a Discord channel
def is_channel(channel):
    reg = re_compile('<#\d*>')
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
    users = list(users.values()) # Discord server usernames and mentions
    not_discord_parts = [] # Used for people missing from the server
    not_checked_in_parts = [] # Used for people not checked in
    usernames = [] # Discord server usernames
    mentions = [] # Discord server mentions

    for user in users:
        usernames.append(user[0])
        mentions.append(user[1])

    # Check each participant to see if they are in the server and checked in
    for p in parts:
        p = p['participant']

        name_lower = p['display_name'].lower()# Participant name in lowercase
        name_escaped = escape_markdown(p['display_name']) # Participant name with escaped markdown characters
        challonge_name_lower = p['challonge_username'].lower() if p['challonge_username'] else p['display_name'].lower() # Challonge user name in lowercase

        # If participant not checked in, add them to the bad list
        if not p['checked_in']:
            not_checked_in_parts.append(name_escaped)

        # If participant not in the Discord, add them to the bad list
        # We check to see if the name exists in any PART of the user list
        if not (any(name_lower in u for u in usernames)) and not (any(challonge_name_lower in u for u in usernames)):
            not_discord_parts.append(name_escaped)

        '''
        (IF name is in Discord server
        AND name is not checked_in)
        AND
        (IF the name or challonge name exists in any part of a Users name)
        Ping the first user
        '''

        if (name_escaped not in not_discord_parts and name_escaped in not_checked_in_parts) and (any(name_lower in u for u in usernames) or any(challonge_name_lower in u for u in usernames)):
            # Get the match for the user if they exist in the discord
            match = [u for u in usernames if (name_lower in u) or (challonge_name_lower in u)]
            # Update the not_checked_in list  to use the user @mention instead of their name
            not_checked_in_parts[not_checked_in_parts.index(name_escaped)] = mentions[usernames.index(match[0])]

    # Sort alphabetically
    not_checked_in_parts.sort()
    not_discord_parts.sort()

    return not_checked_in_parts, not_discord_parts

def seeding(sheet_id, parts, url, seed_num):
    player_points = [] # Stores "player point_value" for sorting later

    # Get dict of associated players and their points
    players_to_points = sheets(sheet_id)

    # Check each participant and if they have points
    for p in parts:
        p = p['participant']

        # If player has points and is active (checked in), add to list for later sorting
        if (p['challonge_username'] in players_to_points) and p['checked_in']:
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
    for player in finished_seeding:
        for p in parts:
            p = p['participant']

            # If Challonge user equals the username we have for seeding
            # Then, update seed number with their index location
            if p['challonge_username'] == finished_seeding[player].split(' ')[0]:
                response = requests_put(url + "/participants/" + str(p['id']) + ".json", headers={"User-Agent":"Lizard-BOT"}, auth=(chal_user, api_key), params={'participant[seed]':player})
                if '200' in str(response.status_code):
                    continue
                elif '401' in str(response.status_code):
                    raise Exception(bold("Challonge") + ": Lizard-BOT does not have access to that tournament")
                else:
                    print(response.text)
                    raise Exception(bold("Challonge") + "Unknown Challonge error for <" + url + ">")

    # Return seeding list
    return finished_seeding

# Check if the guild/channel is in the table
# If not, add it the guilds, channels, and settings tables
async def settings_exist(guild_id, chan_id):
    async with await pool.Connection() as conn:
        try:
            async with conn.cursor() as cursor:
                for level in ['guild','channel']:
                    ids = [] # Store a list of all ids
                    id = guild_id if level == 'guild' else chan_id # Set variable id based on what level of setting

                    # Select all IDs in the DB for the given level
                    sql = "SELECT " + level + "_id FROM " + level + "s"
                    await cursor.execute(sql)
                    for row in cursor:
                        ids.append(row[level + '_id']) # Add IDs to the list

                    # If the ID is not in the list
                    # Add the ID to the guild/channel table
                    # Add the ID to the guild/channel_settings table (This will initialize the default values)
                    if id not in ids:
                        sql = "INSERT INTO " + level + "s (" + level + "_id) VALUES (%s)"
                        await cursor.execute(sql, (id,))

                        sql = "INSERT INTO " + level + "_settings (" + level + "_id) VALUES (%s)"
                        await cursor.execute(sql, (id,))
        except:
            return 0 # Falsy value to fail

        return 1 # Return truthy value for checking

# Read a setting from database for a given guild/channel
async def read_db(level, setting, id):
    async with await pool.Connection() as conn:
        try:
            async with conn.cursor() as cursor:
                # Select the desired setting from the DB for the given guild/channel
                sql = "SELECT `" + setting + "` FROM " + level + "_settings WHERE " + level + "_id = %s"
                await cursor.execute(sql, (id))
                return cursor.fetchone()[setting] # Return the value for the setting
        except:
            raise Exception("Column likely doesn't exist. Did you set up/update the database tables?")

# Save a setting for a given guild/channel to the database
async def save_db(level, setting, data, id, **kwargs):
    async with await pool.Connection() as conn:
        try:
            async with conn.cursor() as cursor:
                # Update the desired setting in the DB for the given guild/channel
                if kwargs:
                    id = kwargs['commandChannel']
                sql = "UPDATE " + level + "_settings SET `" + setting + "` = %s WHERE " + level + "_id = %s"
                await cursor.execute(sql, (data, id))
        except:
            raise Exception("Column likely doesn't exist. Did you set up/update the database tables?")

# Read a stat from database for a given command
async def read_stat(command, func_map):
    stats = {}

    async with await pool.Connection() as conn:
        async with conn.cursor() as cursor:
            # Update the desired setting in the DB for the given guild/channel
            if command:
                if 'challonge' in command or 'edit' in command:
                    function = command.split('_')[0]
                else:
                    function = func_map[command].__name__

                sql = "SELECT command, used FROM stats WHERE command = %s"
                await cursor.execute(sql, (function))
            else:
                sql = "SELECT command, used FROM stats"
                await cursor.execute(sql)
            for row in cursor:
                row_command = row['command']
                if row_command in ['ping']:
                    row_command = 'lizardman'
                elif row_command in ['round_lizard']:
                    row_command = 'round'
                elif row_command in ['prefix']:
                    row_command = 'prefix-lizard'
                elif row_command in ['stats']:
                    row['used'] += 1
                stats.update({row_command.replace('_', '-'):row['used']})

    return stats

# Increment a command usage in the database
async def stat_up(command):
    if 'challonge' in command or 'edit' in command:
        command = command.split('_')[0]

    async with await pool.Connection() as conn:
        async with conn.cursor() as cursor:
            # Check to see if the command already has been used
            sql = "SELECT used FROM stats WHERE command = %s"
            await cursor.execute(sql, (command))
            result = cursor.fetchone()

            # Check the result for how many times a command was used
            if result:
                # Add another use for an existing command
                sql = "UPDATE stats SET used = %s WHERE command = %s"
                await cursor.execute(sql, (result['used']+1,command))
            else:
                # Add a command into the database
                sql = "INSERT INTO stats (command) VALUES (%s)"
                await cursor.execute(sql, (command))

async def read_disable(server):
    #Get setting from DB
    disabled_list = []

    async with await pool.Connection() as conn:
        async with conn.cursor() as cursor:
            # Select the disabled list for the server from the table
            # Return as a python list
            sql = "SELECT `disabled_list` FROM guild_settings WHERE guild_id = %s"
            await cursor.execute(sql, (server))
            disabled_list=json_loads(cursor.fetchone()['disabled_list']) # Return the value for the setting

    return disabled_list

async def set_disable(server, command):
    # List of commands you cannot disable
    dont_disable =["disable","edit","enable","prefix"]

    if command.split('_')[0] in dont_disable:
        # Command is one that is not allowed to be disabled
        raise Exception("Cannot disable important command.")

    # Get current disable list first
    disabled_list = await read_disable(server)

    if command in disabled_list:
        # Already disabled, return error
        raise Exception("Command already disabled.")

    # Add new command
    disabled_list.append(command)
    # Sort alphabetically
    disabled_list = sorted(disabled_list)

    # Set new list in db

    async with await pool.Connection() as conn:
        try:
            async with conn.cursor() as cursor:
                # Update the table with the new disabled list as a json dump
                sql = "UPDATE guild_settings SET disabled_list = %s WHERE guild_id = %s"
                await cursor.execute(sql, (json_dumps(disabled_list),server))
        except:
            # Something went completely wrong here if a new row wasn't created in disabled_list
            raise Exception("Could not save list to table")

    return disabled_list #in case you need it.

async def set_enable(server, command):
    # Get current disable list first
    disabled_list = await read_disable(server)
    if not disabled_list:
        # List is empty
        raise Exception("There is nothing disabled.")
    elif command not in disabled_list:
        # Already disabled, return error
        raise Exception("Command is not disabled.")

    # Remove command
    disabled_list.remove(command)

    # Set new list in db
    async with await pool.Connection() as conn:
        try:
            async with conn.cursor() as cursor:
                # Update the table with the new disabled list as a json dump
                sql = "UPDATE guild_settings SET disabled_list = %s WHERE guild_id = %s"
                await cursor.execute(sql, (json_dumps(disabled_list),server))
        except:
            # Something went completely wrong here if a new row wasn't created in disabled_list
            raise Exception("Could not save list to table")

    return disabled_list #in case you need it.