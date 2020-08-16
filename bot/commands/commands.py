import asyncio
import json
import random
import re
import requests

# Local imports
from secret import api_key
from commands.utilities import (register, bold, get_users, is_channel, pings_b_gone, checkin, seeding, read_db, save_db, settings_exist)

# All @register decorators are a product of reviewing Yaksha
# See utilities.register for more information

@register('bracket')
async def bracket(command, msg, user, channel, *args, **kwargs):
    return read_db('channel', command, channel.id)

@register('help-lizard')
async def help_lizard(command, msg, user, channel, *args, **kwargs):
    return "For more information about the bot and its commands: https://github.com/lizardman301/Lizard-bot-rsf"

@register('lizardman')
async def ping(command, msg, user, channel, *args, **kwargs):
    print("Pinged by {0}".format(user))
    return "Fuck you, Lizardman"

@register('pingtest')
async def pingtest(command, msg, user, channel, *args, **kwargs):
    return "To initiate a ping test, both players go to https://testmyspeed.onl/ and choose a common server between each players location. Send the results of both tests to the TO."

@register('status')
async def status(command, msg, user, channel, *args, **kwargs):
    currentRound = read_db('channel', 'round', channel.id)
    if currentRound:
        # Read the status message for a channel and make it bold
        # Currently the message must have {0} so it can fill in the current round
        return bold(read_db('channel', command, channel.id).format(currentRound))
    return bold("Tournament has not begun. Please wait for the TOs to start Round 1!")

@register('stream')
async def stream(command, msg, user, channel, *args, **kwargs):
    return read_db('channel', command, channel.id)

@register('tos')
async def TOs(command, msg, user, channel, *args, **kwargs):
    tos = read_db('channel', command, channel.id)
    # If we get a value back, return TOs
    if tos:
        return tos
    return "Oops, there is no TO associated with this channel. Please try somewhere else."

# Admin Commands

@register('botrole')
async def botrole(command, msg, user, channel, *args, **kwargs):
    # Pull the role name from the user's roles
    for role in user.roles:
        if role.id == read_db('guild', command, kwargs['guild']):
            return "The bot role is {0}".format(bold(role.name))

@register('challonge')
async def challonge(command, msg, user, channel, *args, **kwargs):
    async with channel.typing():
        base_url = "https://api.challonge.com/v1/tournaments/" # Base url to access Challonge's API
        subcommand = msg.split(' ')[0].lower() # The function trying to be accomplished
        tour_url = msg.split(' ')[1] # Bracket to pull from
        subdomain = read_db('guild', command, kwargs['guild']) # Server's subdomain with Challonge

        # Properly add the subdomain to the bracket url
        if subdomain:
            tour_url = subdomain + '-' + tour_url

        # Get the participants for the tournament
        parts_get = requests.get(base_url + tour_url + "/participants.json", params={'api_key':api_key})
        if '200' in str(parts_get.status_code):
            parts = parts_get.json() # Convert response from json to Python Dictionary

            # If Checkin
            if subcommand in 'checkin':
                not_checked_in_parts, not_discord_parts = checkin(parts, get_users(kwargs['full_msg']))

                # Message showing who is not checked in and who is not in the Discord
                return_msg = "**NOT CHECKED IN:** {0}\n**NOT IN DISCORD:** {1}".format(', '.join(not_checked_in_parts), ', '.join(not_discord_parts))

            # If Seeding
            elif subcommand in 'seeding':
                # If msg has 3 params left 3rd one must be seed number
                # Else, seed whole bracket
                seed_num = int(msg.split(' ')[2]) if len(msg.split(' ')) > 2 else 0

                # Get Google Sheets ID
                sheet_id = read_db('channel', subcommand, channel.id)

                # If seeding hasn't been set, inform user
                if not sheet_id:
                    return "There is no seeding sheet for this channel. Please view https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md for a walkthrough"
                
                # Seeding takes place in different method
                await channel.send("**SEEDING:**\n {0}".format(',\n'.join(seeding(sheet_id, parts, base_url + '/' + tour_url,seed_num)[1:-1].split(', '))))

                # Final message that seeding is complete
                return_msg = bold("SEEDING IS NOW COMPLETE!\nPLEASE REFRESH YOUR BRACKETS\nWAIT FOR THE ROUND 1 ANNOUNCEMENT TO START PLAYING")

            # Bad command catching
            else:
                return_msg = "Invalid Challonge subcommand"

            return return_msg # Return the final message

@register('coin-flip')
async def coin_flip(command, msg, user, channel, *args, **kwargs):
    flip = "The coin landed on: {0}"
    # Flip a coin
    if int(round(random.random()*10*2)) % 2 == 0:
        return flip.format(bold("Heads"))
    return flip.format(bold("Tails"))

@register('edit')
async def edit(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')
    full_msg = kwargs['full_msg'] # Allows us to access the role_mentions
    command_channels = {} # Stores channels to iterate over

    # Check for multi-channel changes at message start
    if full_msg.channel_mentions:
        for param in params:
            if is_channel(param):
                for chnl in full_msg.channel_mentions:
                    if chnl.id == is_channel(param) and 'text' in chnl.type:
                        command_channels.update({chnl.id: chnl.mention}) # Save channel for later
            else:
                break
        for chnl in command_channels:
            params.remove(command_channels[chnl]) # Remove the channel from the params

    editable_command = params[0].lower() # Lower the command we are editing
    params.remove(editable_command) # Remove the command from the params

    # Rejoin the rest of the parameters with spaces
    db_message = ' '.join(params) # The message we send to the Database
    channel_message = ' '.join(params) # The message that gets sent

    # Grab just the BigInt part of bot_role
    if editable_command in ['botrole']:
        # Allow @everyone to be a botrole
        if '@everyone' in params:
            db_message = str(full_msg.guild.default_role.id)
        else:
            db_message = str(full_msg.role_mentions[0].id)
    # Remove the bot pinging TOs on the confirmation message
    elif editable_command in ['tos']:
        mentions = pings_b_gone(full_msg.mentions)
        db_message = ' '.join(mentions.values()) # Put mention values into the database
        channel_message = ' '.join(mentions.keys()) # Send usernames back to the channel
    elif editable_command in ['seeding']:
        reg = re.compile('[a-zA-Z0-9-_]+')
        if not reg.fullmatch(params[0]):
            return "Invalid Sheets spreadsheet ID. Please view https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md for a walkthrough"

    # Check for guild settings, channel settings, or multi channel settings
    if editable_command in ['botrole','prefix-lizard']:
        save_db('guild', editable_command, db_message, kwargs['guild']) # Save the new message to the proper setting in a given guild
    elif command_channels:
        # For each channel, save the setting
        for chnl in command_channels: 
            # We have to double check that the channel is in the DB
            if settings_exist(kwargs['guild'], chnl):
                save_db('channel', editable_command, db_message, chnl) # Save the new message to the proper setting in a given channel
        return "All listed channels had the {0} updated to {1}".format(bold(editable_command), bold(channel_message))
    else:
        save_db('channel', editable_command, db_message, channel.id) # Save the new message to the proper setting in a given channel

    return "The new {0} is: {1}".format(bold(editable_command), bold(channel_message)) # Print the new message for a given setting

@register('prefix-lizard')
async def prefix(command, msg, user, channel, *args, **kwargs):
    return "The prefix is: {0}".format(read_db('guild', command, kwargs['guild']))

@register('refresh')
async def refresh(command, msg, user, channel, *args, **kwargs):
    return bold("REFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS")

@register('remind')
async def remind(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')
    time = int(params[0]) #time is in minutes
    reason = ""
    #specific reason if provided
    if len(params) > 1:
        reason = " ".join(params[1:])

    if reason:
        formatted_msg = "OK! I will ping you in {0} minutes to remind you about \"{1}\"".format(time,reason)
    else:
        formatted_msg = "OK! I will ping you in {0} minutes to remind you about something.".format(time)

    # sends message back to confirm reminder
    await channel.send(formatted_msg)
    print("Reminding {0} in {1} minutes for {2}...".format(user,time,reason))

    # wait message time
    await asyncio.sleep(60 * time)
    if reason:
        formatted_msg = bold("{0}: It has been {1} minutes, don't forget \"{2}\"!").format(user.mention,time,reason)
    else:
        formatted_msg = bold("{0}: It has been {1} minutes, you have been reminded!".format(user.mention,time))

    await channel.send(formatted_msg)
    print("{0} has been reminded after {1} minutes.".format(user,time))

@register('reset')
async def reset(command, msg, user, channel, *args, **kwargs):
    save_db('channel', 'round', '', channel.id)
    return "Round has been reset."

@register('round')
async def round_lizard(command, msg, user, channel, *args, **kwargs):
    save_db('channel', command, msg, channel.id)
    return await status('status', msg, user, channel)