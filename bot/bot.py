import asyncio
import discord
import json
import os
import random

# Local imports
from commands.utilities import (read_db, settings_exist)
import interface
from secret import token

# New intents feature (needed to count members)
intents = discord.Intents.default()
intents.members = True

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
        status = "Now in {} servers!"

        if total == 1:
            status = status[:-2] + "!"

        game = discord.Game(name=status.format(total))

        try:
            await client.change_presence(activity=game)
        except discord.HTTPException:
            # Might've gotten ratelimited so just sleep for the interval and try later.
            print('Exception when trying to change status. Trying again in 8 hours')
            pass
        await asyncio.sleep(28800)

# Yaksha
# When message is typed in any channel the bot has access to, check to see if the bot needs to respond
@client.event
async def on_message(message):
    # If the bot is the user, do not respond
    if message.author == client.user:
        return

    # If the bot is mentioned in a message, respond with a message informing it of being a bot
    if client.user.mentioned_in(message):
        # If @everyone or @here is used, ignore
        if "@everyone" in message.content or "@here" in message.content:
            return
        # Choose from a random response, then follow with a Bot message
        responses = ["Ok", "Thanks", "Sounds good to me", "Buff Rashid", "Beep Boop", "Yes", "No", "Good to know", "Glad to hear it", "I'll keep that in mind", "The answer lies in the heart of battle", "Go home and be a family man"]
        await message.channel.send("{0} \n**I am a Bot and cannot respond to mentions**".format(random.choice(responses)))

    # Check if the channel is in the DB
    # Add it if it isn't
    if not settings_exist(message.guild.id, message.channel.id):
        await chan.send("Oops, I'm broken")
        print("Lizard-BOT failed to create DB entry for: " + message.guild.name + ". Guild ID: " + message.guild.id)

    # Get prefix for the guild
    prefix = read_db('guild', 'prefix-lizard', message.guild.id)

    # Hardcode prefix command to be accessible via !
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

        if attempted_cmd in client.no_arg_cmds and len(msg.split()) > 1:
            await message.channel.send("Too many arguments. Check help-lizard for more info")
            return

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
                if type(discord.Embed()) == type(response):
                    await message.channel.send(embed=response)
                    break
                await message.channel.send(response)
            break

# Yaksha
# Main thread the kicks off the initial setup and starts the bot
def main():
    client.commands, client.admin_commands, client.no_arg_cmds = [], [], []
    client.help = {}

    # Pull in a separate config
    config = json.loads(open(os.path.join(os.path.dirname(__file__), 'commands/bots.json')).read())

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
                client.no_arg_cmds.append(alias)
            # Add the help message for each alias
            client.help.update({alias:aliases[-1]})
            # Add the command and aliases as valid commands
            client.commands.append(alias)

    commands = config.get('admin_commands', {}).copy().values()

    # For every admin command in commands loop over the child array
    for aliases in commands:
        # For every child in the child array, sort it to the appropriate variable for later
        for alias in aliases:
            # Add the command and aliases as admin commands
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

    # Start our interface for our commands and Discord
    client.interface = interface.Interface(client.admin_commands, client.edit_subcommands, client.help)

    # Start loop for status change
    client.loop.create_task(change_status())

    # Start the bot
    client.run(token)

# If main is here, run main
if __name__ == '__main__':
    main()