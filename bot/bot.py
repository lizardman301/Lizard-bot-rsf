import discord
import json
import os

# Local imports
from commands.utilities import (read_db, settings_exist)
import interface
from secret import token

client = discord.Client()

@client.event
async def on_ready():
    print('\nLogged in as {0.user}'.format(client))
    print('-------------------------------')
    for guild in client.guilds:
        print('Joined guild %s' % guild)


# Yaksha
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the channel is in the DB
    # Add it if it isn't
    if not settings_exist(message.guild.id, message.channel.id):
        await chan.send("Oops, I'm broken")
        print("Oops, I'm broken")

    # Get prefix for the guild
    prefix = read_db('guild', 'prefix-lizard', message.guild.id)

    if not message.content.startswith(prefix):
        return

    for command in client.commands.keys():
        command = command.lower() # Lower the command for easier matching
        msg = message.content # The message
        user = message.author # The author
        attempted_cmd = msg.split(' ')[0][1:].lower() # Get the attempted command from the beginning of the string

        # Check if the message begins with a command
        if attempted_cmd and attempted_cmd == command:
            # Remove the command from the start
            msg = msg[len(command)+1:].strip()
            
            # Await the interface calling the command
            response = await client.interface.call_command(command, msg, user, message.channel, guild=message.guild.id, full_msg=message)
            
            # If there is a response, send it
            if response:
                await message.channel.send(response)
            break

# Yaksha
def main():
    # Pull in a seperate config
    config = json.loads(open(os.path.join(os.path.dirname(__file__), 'commands/bots.json')).read())

    # Grab our commands
    client.commands = config.get('common_commands', {}).copy()
    client.commands.update(config.get('admin_commands', {}))

    client.admin_commands = config.get('admin_commands', {}).copy()

    client.subcommands = config.get('challonge_subcommands', {}).copy()
    client.subcommands.update(config.get('edit_subcommands', {}))

    client.config = config

    # Start our interface for our commands and Discord
    client.interface = interface.Interface(client.admin_commands)

    # Start the bot
    client.run(token)

# If main is here, run main
if __name__ == '__main__':
    main()