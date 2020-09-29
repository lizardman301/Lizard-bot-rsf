import asyncio
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
async def change_status():
    """
    Update the "Playing x" status to display bot
    commands.
    """
    await client.wait_until_ready()
    while True:
        sum = len(client.guilds)
        status = "Now in {} servers!"

        if sum == 1:
            status = status[:-2] + "!"

        game = discord.Game(name=status.format(sum))

        try:
            await client.change_presence(activity=game)
        except discord.HTTPException:
            # Might've gotten ratelimited so just sleep for the
            # interval and try later.
            print('Exception when trying to change status. Trying again in 4 hours')
            pass
        await asyncio.sleep(14400)

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

    # Hardcode prefix to be accessible via !
    if message.content.startswith("!prefix-lizard") or message.content.startswith("!prefliz"):
        response = await client.interface.call_command('prefix-lizard', 0, 0, 0, guild=message.guild.id)
        if response:
            await message.channel.send(response)
        return
    # If other commands don't start with the correct prefix, do nothing
    elif not message.content.startswith(prefix):
        return

    for command in client.commands:
        command = command.lower() # Lower the command for easier matching
        msg = message.content # The message
        attempted_cmd = msg.split(' ')[0][1:].lower() # Get the attempted command from the beginning of the string

        # Check if the message begins with a command
        if attempted_cmd and attempted_cmd == command:
            user = message.author # The author
            kwargs = {'guild':message.guild.id}

            # Remove the command from the start
            msg = msg[len(command)+1:].strip()

            if command in ['challonge', 'chal', 'edit']:
                kwargs['full_msg'] = message

            # Await the interface calling the command
            response = await client.interface.call_command(command, msg, user, message.channel, **kwargs)

            # If there is a response, send it
            if response:
                await message.channel.send(response)
            break

# Yaksha
def main():
    client.commands, client.admin_commands = [], []
    client.help = {}

    # Pull in a separate config
    config = json.loads(open(os.path.join(os.path.dirname(__file__), 'commands/bots.json')).read())

    # Grab our commands
    commands = list(config.get('common_commands', {}).copy().values())
    commands.extend(config.get('admin_commands', {}).values())
    for aliases in commands:
        for alias in aliases:
            if alias == aliases[-1]:
                client.help.update({aliases[0]:alias})
                break
            client.commands.append(alias)

    commands = config.get('admin_commands', {}).copy().values()
    for aliases in commands:
        for alias in aliases:
            client.admin_commands.append(alias)

    client.challonge_subcommands = config.get('challonge_subcommands', {}).copy()
    for subcmd in client.challonge_subcommands:
        for info in client.challonge_subcommands[subcmd]:
            if info == client.challonge_subcommands[subcmd][-1]:
                client.help.update({"challonge " + subcmd:info})
                break

    client.edit_subcommands = config.get('edit_subcommands', {}).copy()
    for subcmd in client.edit_subcommands:
        for info in client.edit_subcommands[subcmd]:
            if info == client.edit_subcommands[subcmd][-1]:
                client.help.update({"edit " + subcmd:info})
                break

    client.config = config

    # Start our interface for our commands and Discord
    client.interface = interface.Interface(client.admin_commands, client.edit_subcommands,client.help)

    client.loop.create_task(change_status())

    # Start the bot
    client.run(token)

# If main is here, run main
if __name__ == '__main__':
    main()