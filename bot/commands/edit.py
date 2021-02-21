from re import compile as re_compile

# Local imports
from commands.commands import (help_lizard)
from commands.utilities import (register, bold, is_channel, pings_b_gone, save_db, settings_exist)

# All @register decorators are a product of reviewing Yaksha
# See utilities.register for more information


def channel_processing(params, channel_mentions):
    command_channels = {} # Stores channels to iterate over

    # Check for multi-channel changes at message start
    # Check for channel mentions
    if channel_mentions:
        # for each parameter in the msg
        for param in params:
            # Check if that parameter is a channel
            if is_channel(param):
                # for each channel in the channel mentions
                for chnl in channel_mentions:
                    # Check if the param channel id is the same as the channel mention id and that it is a text channel
                    if chnl.id == is_channel(param) and 'text' in chnl.type:
                        # Add the id and mention value to loop over later
                        command_channels.update({chnl.id: chnl.mention}) # Save channel for later
            else:
                break
        # For all the channels remove them from parameters
        for chnl in command_channels:
            params.remove(command_channels[chnl]) # Remove the channel from the params

    return params, command_channels

#@register('edit')
async def edit(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')
    full_msg = kwargs['full_msg'] # Allows us to access the role_mentions
    command_channels = {} # Stores channels to iterate over

    # Check for multi-channel changes at message start
    # Check for channel mentions
    if full_msg.channel_mentions:
        # for each parameter in the msg
        for param in params:
            # Check if that parameter is a channel
            if is_channel(param):
                # for each channel in the channel mentions
                for chnl in full_msg.channel_mentions:
                    # Check if the param channel id is the same as the channel mention id and that it is a text channel
                    if chnl.id == is_channel(param) and 'text' in chnl.type:
                        # Add the id and mention value to loop over later
                        command_channels.update({chnl.id: chnl.mention}) # Save channel for later
            else:
                break
        # For all the channels remove them from parameters
        for chnl in command_channels:
            params.remove(command_channels[chnl]) # Remove the channel from the params
            
    params[0] = params[0].lower() # Make sure the command we are editing is in lowercase
    editable_command = params[0] # The command we are editing
    if editable_command not in kwargs['edit_subs']:
        raise Exception(bold("Edit") + ": Invalid Subcommand. " + await help_lizard('','','',''))

    params.remove(editable_command) # Remove the command from the params
    # Rejoin the rest of the parameters with spaces
    db_message = ' '.join(params) # The message we send to the Database
    channel_message = ' '.join(params) # The message that gets sent

    # Grab just the BigInt part of bot_role
    if editable_command in ['botrole']:
        return "fuck"
    elif editable_command in ['tos'] and (not full_msg.mentions and params):
            raise Exception(bold("Edit") + ": Invalid user mention. Try @'ing somebody")
    # Remove the bot pinging TOs on the confirmation message
    elif editable_command in ['tos']:
        mentions = pings_b_gone(full_msg.mentions)
        db_message = ' '.join(mentions.values()) # Put mention values into the database
        channel_message = ' '.join(mentions.keys()) # Send usernames back to the channel
    # Check if the Sheets ID matches what Google specified
    elif editable_command in ['seeding']:
        reg = re_compile('[a-zA-Z0-9-_]+')
        if not params:
            pass
        elif not reg.fullmatch(params[0]) or len(params[0]) > 80:
            raise Exception(bold("Edit") + ": Invalid Sheets spreadsheet ID. Please view <https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md> for a walkthrough")
    # Check if prefix is a singular character
    elif editable_command in ['prefix-lizard'] and not len(db_message) == 1:
        raise Exception(bold("Edit") + ": Lizard-BOT prefix must be a singular character.")
    # Check if the status message contains {0}
    elif editable_command in ['status'] and not db_message.count('{0}') > 0:
        raise Exception(bold("Edit") + ": Status message must include {0} to substitute the round number")
    # Check if bracket, pingtest, status, and stream are small enough to store and send into Discord channels
    elif editable_command in ['bracket','pingtest','status','stream'] and len(db_message) > 1945:
        raise Exception(bold("Edit") + ": Message is too long to be stored. Shorten your message to 1945 characters or less")

    # Check for guild settings, channel settings, or multi channel settings
    if editable_command in ['botrole', 'challonge','prefix-lizard']:
        await save_db('guild', editable_command, db_message, kwargs['guild']) # Save the new message to the proper setting in a given guild
    elif command_channels:
        # For each channel, save the setting
        for chnl in command_channels: 
            # We have to double check that the channel is in the DB
            if await settings_exist(kwargs['guild'], chnl):
                await save_db('channel', editable_command, db_message, chnl) # Save the new message to the proper setting in a given channel
        return "All listed channels had the {0} updated to {1}".format(bold(editable_command), bold(channel_message))
    else:
        await save_db('channel', editable_command, db_message, channel.id) # Save the new message to the proper setting in a given channel

    return "The new {0} is: {1}".format(bold(editable_command), bold(channel_message)) # Print the new message for a given setting

@register('edit botrole')
@register('edit role')
async def edit_botrole(command, msg, user, channel, *args, **kwargs):
    editable_command = 'botrole'
    role_mentions = kwargs['role_mentions']
    default_role = kwargs['guild_default_role']

    # Rejoin the rest of the parameters with spaces
    db_message = msg # The message we send to the Database
    channel_message = msg # The message that gets sent

    if not role_mentions or len(role_mentions) > 1:
        # Allow @everyone to be a botrole
        if not msg:
            db_message = str(default_role.id)
            channel_message = default_role.name
        else:
            raise Exception(bold("Edit") + " : Too few/many role mentions for botrole. Try again with only one role mentioned")
    elif role_mentions:
        db_message = str(role_mentions[0].id)
        channel_message = role_mentions[0].name

    await save_db('guild', editable_command, db_message, kwargs['guild'])
    return "The new {0} is: {1}".format(bold(editable_command), bold(channel_message)) # Print the new message for a given setting

@register('edit bracket')
@register('edit pingtest')
@register('edit status')
@register('edit stream')
async def edit_channel_strings(command, msg, user, channel, *args, **kwargs):
    editable_command = command.split(' ')[1]
    params = msg.split(' ')
    channel_mentions = kwargs['channel_mentions']
    params, command_channels = channel_processing(params, channel_mentions)

    # Rejoin the rest of the parameters with spaces
    message = ' '.join(params) # The message we send to the Database

    # Check if the status message contains {0}
    if editable_command in ['status'] and not message.count('{0}') > 0:
        raise Exception(bold("Edit") + ": Status message must include {0} to substitute the round number")
    elif len(message) > 1945:
        raise Exception(bold("Edit") + ": Message is too long to be stored. Shorten your message to 1945 characters or less")

    if command_channels:
        # For each channel, save the setting
        for chnl in command_channels: 
            # We have to double check that the channel is in the DB
            if await settings_exist(kwargs['guild'], chnl):
                await save_db('channel', editable_command, message, chnl) # Save the new message to the proper setting in a given channel
        return "All listed channels had the {0} updated to {1}".format(bold(editable_command), bold(message))
    else:
        await save_db('channel', editable_command, message, channel.id) # Save the new message to the proper setting in a given channel
    return "The new {0} is: {1}".format(bold(editable_command), bold(message)) # Print the new message for a given setting

@register('edit challonge')
async def edit_challonge(command, msg, user, channel, *args, **kwargs):
    editable_command = command.split(' ')[1]

    # Check if prefix is a singular character
    if len(msg) > 60:
        raise Exception(bold("Edit") + ": Challonge Subdomain is too long. Are you sure that is a challonge subdomain?")

    await save_db('guild', editable_command, msg, kwargs['guild'])
    return "The new {0} is: {1}".format(bold(editable_command), bold(msg)) # Print the new message for a given setting

@register('edit prefix-lizard')
async def edit_prefix(command, msg, user, channel, *args, **kwargs):
    editable_command = command.split(' ')[1]

    # Check if prefix is a singular character
    if not len(msg) == 1:
        raise Exception(bold("Edit") + ": Lizard-BOT prefix must be a singular character.")

    await save_db('guild', editable_command, msg, kwargs['guild'])
    return "The new {0} is: {1}".format(bold(editable_command), bold(msg)) # Print the new message for a given setting

@register('edit seeding')
async def edit_seeding(command, msg, user, channel, *args, **kwargs):
    editable_command = command.split(' ')[1]
    params = msg.split(' ')
    channel_mentions = kwargs['channel_mentions']
    params, command_channels = channel_processing(params, channel_mentions)

    # Rejoin the rest of the parameters with spaces
    message = ' '.join(params) # The message we send to the Database

    # Check if the Sheets ID matches what Google specified
    reg = re_compile('[a-zA-Z0-9-_]+')
    if not message:
        message = ''
    elif not reg.fullmatch(params[0]) or len(params[0]) > 80:
        raise Exception(bold("Edit") + ": Invalid Sheets spreadsheet ID. Please view <https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md> for a walkthrough")

    if command_channels:
        # For each channel, save the setting
        for chnl in command_channels: 
            # We have to double check that the channel is in the DB
            if await settings_exist(kwargs['guild'], chnl):
                await save_db('channel', editable_command, message, chnl) # Save the new message to the proper setting in a given channel
        return "All listed channels had the {0} updated to {1}".format(bold(editable_command), bold(message))
    else:
        await save_db('channel', editable_command, message, channel.id) # Save the new message to the proper setting in a given channel
    return "The new {0} is: {1}".format(bold(editable_command), bold(message)) # Print the new message for a given setting

@register('edit tos')
async def edit_tos(command, msg, user, channel, *args, **kwargs):
    editable_command = command.split(' ')[1]
    params = msg.split(' ')
    mentions = kwargs['mentions']
    channel_mentions = kwargs['channel_mentions']
    params, command_channels = channel_processing(params, channel_mentions)

    if (not mentions and params[0]):
            raise Exception(bold("Edit") + ": Invalid user mention. Try @'ing somebody")
    
    # Remove the bot pinging TOs on the confirmation message
    mentions_pingless = pings_b_gone(mentions)
    db_message = ' '.join(mentions_pingless.values()) # Put mention values into the database
    channel_message = ' '.join(mentions_pingless.keys()) # Send usernames back to the channel

    if command_channels:
        # For each channel, save the setting
        for chnl in command_channels: 
            # We have to double check that the channel is in the DB
            if await settings_exist(kwargs['guild'], chnl):
                await save_db('channel', editable_command, db_message, chnl) # Save the new message to the proper setting in a given channel
        return "All listed channels had the {0} updated to {1}".format(bold(editable_command), bold(channel_message))
    else:
        await save_db('channel', editable_command, db_message, channel.id) # Save the new message to the proper setting in a given channel
    return "The new {0} is: {1}".format(bold(editable_command), bold(channel_message)) # Print the new message for a given setting