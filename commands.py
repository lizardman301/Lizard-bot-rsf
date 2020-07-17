from utilities import (pings_b_gone, bold, read_db, save_db, register, get_callbacks)
import asyncio
import random

# All @register() are a product of reviewing Yaksha
# See utilities.register for more information

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


@register('botrole')
async def botrole(command, msg, user, channel, *args, **kwargs):
    for role in user.roles:
        if role.id == read_db('guild', command, kwargs['guild']):
            return "The bot role is {0}".format(bold(role.name))

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

    editable_command = params[0].lower() # lower the command we are editing
    params.remove(editable_command)

    # Grab just the BigInt part of bot_role
    if editable_command in ['botrole']:
        params[0] = str(full_msg.role_mentions[0].id)
        # Allow @everyone to be a botrole
        if '@everyone' in params:
            params[0] = kwargs['guild'].default_role.id

    new_msg = ' '.join(params) # Rejoin the rest of the parameters with spaces

    # If editable command is a guild command, save to guild settings
    # Else save to channel_settings
    if editable_command in ['botrole','prefix-lizard']:
        save_db('guild', editable_command, new_msg, kwargs['guild']) # Save the new message to the proper setting in a given guild
    else:
        save_db('channel', editable_command, new_msg, channel.id) # Save the new message to the proper setting in a given channel

    # Remove the bot pinging TOs on the confirmation message
    if editable_command in ['tos']:
        mentions = []
        for mention in full_msg.mentions:
            mentions.append(mention.name) # Remove the bot pinging the TO
        new_msg = ' '.join(mentions)

    return "The new {0} is: {1}".format(bold(editable_command), bold(new_msg)) # Print the new message for a given setting

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
