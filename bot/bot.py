import discord # Discord bot needs discord library
from discord.utils import escape_markdown # Regexing fun simplified

from asyncio import sleep as asyncio_sleep # For sleeping specific threads
from json import loads as json_loads # For bringing in config file
from os import path as os_path # For bringing in config file
from random import choice as random_choice # For randomizing arrays
from traceback import print_exc as traceback_print_exc, format_exc as traceback_format_exc # For printing error messages
from sys import exc_info as sys_exc_info # For grabbing error information

# Local imports
from commands.utilities import (read_db, settings_exist) # Add some utility commands to help get guild info
import interface # The selector between bot.py and commands
from secret import token # Discord token

# New intents feature (needed to count members)
intents = discord.Intents.default()
intents.members = True

# Create the Discord client
client = discord.Client(intents=intents)

# Once bot is fully logged in, print the guilds it is in
@client.event
async def on_ready():
    print('\nLogged in as {0.user}'.format(client))
    print('-------------------------------')
    for guild in client.guilds:
        print('Joined guild %s' % guild)

# Yaksha
# Change the status displayed under the bot's name
async def change_status():
    """
    Update the "Playing x" status to display bot
    commands.
    """
    await client.wait_until_ready()
    # Every 8 hours update the status to display the number of Discord servers the bot is in
    while True:
        total = len(client.guilds)
        status = "lizard-bot.com | In {} servers!"

        # If only one server, change message to be gramatically correct
        if total == 1:
            status = status[:-2] + "!"

        # Sets the game message used to change the status
        game = discord.Game(name=status.format(total))

        # Try to change the status
        try:
            await client.change_presence(activity=game)
        except discord.HTTPException:
            # Might've gotten ratelimited so just sleep for the interval and try later.
            print('Exception when trying to change status. Trying again in 8 hours')
            pass
        await asyncio_sleep(28800)

# Yaksha
# When message is typed in any channel the bot has access to, check to see if the bot needs to respond
@client.event
async def on_message(message):
    command = 'bracket' # Pre-setting the variable for use in the try/except block below (L78)
    # If the bot is the user, do not respond
    if message.author == client.user:
        return

    # If the bot is mentioned in a message, respond with a message informing it of being a bot
    if client.user.mentioned_in(message):
        # If @everyone or @here is used, ignore
        if "@everyone" in message.content or "@here" in message.content:
            return
        # Choose from a random response, then follow with a Bot message
        responses = ["Ok", "Thanks", "Sounds good to me", "Buff Rashid", "Buff Rashid", "Beep Boop", "Yes", "No", "Good to know", "Glad to hear it", "I'll keep that in mind", "The answer lies in the heart of battle", "Go home and be a family man"]
        await message.channel.send("{0} \n**I am a Bot that plays Rashid. Mentions cause my little Rashid brain to short circuit. Did you have ~~an eagle spi~~ a command?**".format(random_choice(responses)))
        return

    try:
        # Check if the channel is in the DB
        # Add it if it isn't
        if not settings_exist(message.guild.id, message.channel.id):
            raise Exception("Lizard-BOT failed to create DB entry for: " + message.guild.name + ". Guild ID: " + message.guild.id)

        # Get prefix for the guild
        prefix = read_db('guild', 'prefix-lizard', message.guild.id)

        # Check if the attempted_cmd is !prefix-lizard and has too many args
        if (message.content.split(' ')[0] == "!prefix-lizard" or message.content.split(' ')[0] == "!prefliz") and len(message.content.split()) > 1:
            await message.channel.send("Too many arguments. Check help-lizard for more info")
            return
        # Hardcode prefix command to be accessible via !
        elif message.content.split(' ')[0] == "!prefix-lizard" or message.content.split(' ')[0] == "!prefliz":
            response = await client.interface.call_command('prefix-lizard', 0, 0, 0, guild=message.guild.id)
            if response:
                await message.channel.send(response)
            return
        # If other commands don't start with the correct prefix, do nothing
        elif not message.content.startswith(prefix):
            return
        # Check if the attempted_cmd takes arguments
        elif message.content.split(' ')[0][1:].lower() in client.no_arg_cmds and len(message.content.split()) > 1:
            await message.channel.send("Too many arguments. Check help-lizard for more info")
            return

        # Rotate through commands to see if the message matches
        for command in client.commands:
            command = command.lower() # Lower the command for easier matching
            msg = message.content # The message
            attempted_cmd = msg.split(' ')[0][1:].lower() # Get the attempted command from the beginning of the string

            if attempted_cmd in ['challonge', 'chal', 'edit'] and len(msg.split(' ')) > 1:
                attempted_cmd += ' ' + msg.split(' ')[1].lower()

            # Check if the message begins with a command
            if attempted_cmd and attempted_cmd == command:
                user = message.author # The author
                kwargs = {'guild':message.guild.id}

                # Remove the command from the start
                msg = msg[len(command)+1:].strip()

                # Check command to see if we need keyword args
                if command in ['challonge checkin', 'chal checkin']:
                    kwargs['guild_members'] = message.guild.members
                elif command in ['edit botrole', 'edit role']:
                    kwargs['guild_default_role'] = message.guild.default_role
                    kwargs['role_mentions'] = message.role_mentions
                elif command in ['edit bracket', 'edit pingtest', 'edit status', 'edit seeding', 'edit stream', 'edit tos']:
                    kwargs['channel_mentions'] = message.channel_mentions
                    if command in ['edit tos']:
                        kwargs['mentions'] = message.mentions
                elif command in ['draw']:
                    kwargs['full_msg'] = message
                    kwargs['client'] = client

                # Await the interface calling the command
                response = await client.interface.call_command(command, msg, user, message.channel, **kwargs)
                # If there is a response, send it
                if response:
                    await message.channel.send(response)
                break
    except Exception:
        string_info = str(sys_exc_info()[1]) # Error message
        function_name = string_info.split(':')[0] # The command the error message came from

        # Expected error
        # Return friendly user message
        # Additional checks needed for challonge and edit commands that have multiple subcommands
        if client.interface._func_mapping[command].__name__ in function_name.strip("*").lower() or ('challonge' in client.interface._func_mapping[command].__name__ and 'challonge' in function_name.strip("*").lower()) or ('edit' in client.interface._func_mapping[command].__name__ and 'edit' in function_name.strip("*").lower()):
            await message.channel.send(function_name.replace('_', '-') + ': ' + ':'.join(string_info.split(':')[1:]))
        elif command == 'dev':
            # Return user message
            await message.channel.send(escape_markdown(traceback_format_exc()))
            # Print error to console
            traceback_print_exc()
        else:
            # Print error to console
            traceback_print_exc()
            # If we get this far and something breaks
            # Something is very wrong. Send user generic error message
            await message.channel.send("I is broken.\nBuff Rashid and submit an issue via <https://github.com/lizardman301/Lizard-bot-rsf/issues>\nOr just tell Lizardman301. That's what I do.")

# Yaksha
# Main thread the kicks off the initial setup and starts the bot
def main():
    client.commands, client.admin_commands, client.no_arg_cmds = [], [], [] # Init
    client.help = {} # Init

    # Pull in a separate config
    config = json_loads(open(os_path.join(os_path.dirname(__file__), 'commands/bots.json')).read())

    # Grab our commands from the json
    commands = list(config.get('common_commands', {}).copy().values())
    commands.extend(config.get('admin_commands', {}).values())
    no_arg_cmds = config.get('no_arg_commands', []).copy()

    # Sort the raw json into the appropriate variables
    # For every entry in commands loop over the child array
    for aliases in commands:
        # For every child in the child array, sort it to the appropriate variable for later
        for alias in aliases:
            # If the child item is the last item(the help message), move on to the next command
            if alias == aliases[-1]:
                break
            # Elif the full command doesn't take args, have the aliases not accept args
            elif aliases[0] in no_arg_cmds:
                client.no_arg_cmds.append(alias.lower())
            # Add the help message for each alias
            client.help.update({alias.lower():aliases[-1]})
            # Add the command and aliases as valid commands
            client.commands.append(alias)

    # Admin commands
    commands = config.get('admin_commands', {}).copy().values()

    # For every admin command in commands loop over the child array
    for aliases in commands:
        # For every child in the child array, sort it to the appropriate variable for later
        for alias in aliases:
            # Add the command and aliases as admin commands
            client.admin_commands.append(alias)

    # Dev commands
    client.dev_commands = list(config.get('dev_commands', []).copy())
    for command in client.dev_commands:
        client.commands.append(command)

    # Start our interface for our commands and Discord
    client.interface = interface.Interface(client.admin_commands, client.dev_commands, client.help)

    # Start loop for status change
    client.loop.create_task(change_status())

    # Start the bot
    client.run(token)

# If main is here, run main
if __name__ == '__main__':
    main()