from asyncio import sleep as asyncio_sleep
from discord import Embed, Colour
from discord.utils import escape_markdown # Regexing fun simplified
from pprint import pformat
from random import random as random_random, choice as random_choice
from re import compile as re_compile
from requests import get as requests_get

# Local imports
from secret import api_key
from commands.utilities import (register, bold, get_chal_tour_id, get_random_chars, get_users, is_channel, pings_b_gone, checkin, seeding, read_db, read_stat, save_db, settings_exist, set_disable, set_enable, read_disable)

# All @register decorators are a product of reviewing Yaksha
# See utilities.register for more information

@register('botrole')
@register('role')
async def botrole(command, msg, user, channel, *args, **kwargs):
    # Pull the role name from the guild's roles
    return "The bot role is {0}".format(bold(channel.guild.get_role(read_db('guild', 'botrole', kwargs['guild'])).name))

@register('bracket')
async def bracket(command, msg, user, channel, *args, **kwargs):
    return read_db('channel', 'bracket', channel.id)

@register('coin-flip')
@register('flip')
@register('cf')
async def coin_flip(command, msg, user, channel, *args, **kwargs):
    flip = "The coin landed on: {0}"
    # Flip a coin
    if int(round(random_random()*10*2)) % 2 == 0:
        return flip.format(bold("Heads"))
    return flip.format(bold("Tails"))

@register('draw')
async def draw(command, msg, user, channel, *args, **kwargs):
    full_msg = kwargs['full_msg']
    char_num = 7
    client = kwargs['client']
    unicode_reactions = ["1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣"]
    player1 = user

    if len(msg.split(' ')) > 2:
        raise Exception(bold("Draw") + ": Too many arguments. " + await help_lizard('','','',''))
    # No mention or too many, Raise exception
    elif not full_msg.mentions or len(full_msg.mentions) > 1:
        raise Exception(bold("Draw")+ ": You must mention exactly one user to draw against.")

    player2 = full_msg.mentions[0]

    if player1 == player2:
        raise Exception(bold("Draw")+ ": You are not allowed to draw against yourself.")

    # Start with randomselect basis to get characters
    try:
        game = msg.split(' ')[1].lower()
    except:
        # No game to be found so default to sfv
        game = 'sfv'

    chars, games = get_random_chars(game)
    if not chars:
        raise Exception(bold("Draw") + ": Invalid game: {0}. Valid games are: {1}".format(bold(game), bold(', '.join(games))))

    if len(chars) < char_num:
        # If we have a game with an amount of characters less than the number of cards drawn, it will never create a list
        raise Exception(bold("Draw")+ ": Invalid game: {0}. The game selected has too few characters to function with this command.".format(bold(game)))

    # Initial accept embed
    accept_embed = Embed(title="Card Draw", colour=Colour(0x0fa1dc))
    accept_embed.set_footer(text="Do you agree to a draw, {0}?".format(player2.display_name))
    try:
        accept_msg = await channel.send(embed=accept_embed)
    except:
        raise Exception(bold("Draw") + ": Error sending embed to chat. Give Lizard-BOT the permission: " + bold("Embed Links"))

    await accept_msg.add_reaction('✅')

    try:
        # Wait for the reaction from the correct user
        # lambda function check for the correct reaction and the correct user
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=lambda reaction, user: user == player2 and str(reaction.emoji) == '✅' and reaction.message == accept_msg)
    except:
        await accept_msg.delete()
        raise Exception(bold("Draw") + ": The draw was not accepted.")

    # if we got here, draw was accepted

    # randomly choose player order
    order = random_choice([[player1,player2,player1,player2,player2,player1],[player2,player1,player2,player1,player1,player2]])
    # declare an Array of 0s to mark all cards as not picked
    # -1 means a card ban, 1 means a card draw
    picks = [0] * char_num

    #create new embed
    card_embed = Embed(title="Card Draw", colour=Colour(0x0fa1dc))

    # Declare list and fill with the amount of random characters
    # Make it so that it has to be all different characters
    characters_list = []
    while len(characters_list) < char_num:
        new_char = random_choice(chars)
        # Only add to the list if it is a new character
        if not new_char in characters_list:
            characters_list.append(new_char)
    # Add characters to ban
    for i, c in enumerate(characters_list):
        card_embed.add_field(name="Char {0}".format(i+1), value=c, inline=True)

    await accept_msg.delete()
    try:
        game_msg = await channel.send(embed=card_embed)
    except:
        raise Exception(bold("Draw") + ": Error sending embed to chat. Give Lizard-BOT the permission: " + bold("Embed Links"))

    # Add reactions for pick/ban purposes
    for reaction in unicode_reactions:
        await game_msg.add_reaction(reaction)

    # Create lists for the picked characters
    p1_chars = []
    p2_chars = []

    for it, player in enumerate(order):
        user_to_check = None
        msg_to_check = None
        reaction_read = None
        reaction_read_emoji = None
        number = None

        # first two are bans
        if it < 2:
            card_embed.set_footer(text="{0}, select a character to ban.".format(player.display_name))
            await game_msg.edit(embed = card_embed)

            while not(user_to_check == player) or not(msg_to_check == game_msg) or reaction_read_emoji not in unicode_reactions:
                try:
                    reaction_read, user_to_check  = await client.wait_for('reaction_add', timeout=60.0)
                    msg_to_check = reaction_read.message
                    if not(msg_to_check == game_msg):
                        continue
                    reaction_read_emoji = reaction_read.emoji
                    number = unicode_reactions.index(reaction_read_emoji)
                    if picks[number] != 0:
                        # already banned, set as None to make it fail
                        reaction_read_emoji = None
                        card_embed.set_footer(text="{0}, that character is already banned, please choose another.".format(player.display_name))
                        await game_msg.edit(embed = card_embed)
                except:
                    await game_msg.delete()
                    raise Exception(bold("Draw") + ": {0} failed to ban a character.".format(player.display_name))
            # mark character as banned
            picks[number] = -1
            # Strikethrough char on embed
            card_embed.set_field_at(number, name="Char {0}".format(number+1), value = "~~{0}~~".format(characters_list[number]))

        else:
            card_embed.set_footer(text="{0}, select a character to pick.".format(player.display_name))
            if it == 4:
                # Remind them gently they get to pick another character in a row if they are the 2nd player
                card_embed.set_footer(text="{0}, select another character to pick.".format(player.display_name))
            await game_msg.edit(embed = card_embed)

            while not(user_to_check == player) or not(msg_to_check == game_msg) or reaction_read_emoji not in unicode_reactions:
                try:
                    reaction_read, user_to_check  = await client.wait_for('reaction_add', timeout=60.0)
                    msg_to_check = reaction_read.message
                    if not(msg_to_check == game_msg):
                        continue
                    reaction_read_emoji = reaction_read.emoji
                    number = unicode_reactions.index(reaction_read_emoji)
                    if picks[number] == -1:
                        # already banned, set as None to make it fail
                        reaction_read_emoji = None
                        card_embed.set_footer(text="{0}, that character is already banned, please choose another.".format(player.display_name))
                        await game_msg.edit(embed = card_embed)
                    elif picks[number] == 1:
                        # already banned, set as None to make it fail
                        reaction_read_emoji = None
                        card_embed.set_footer(text="{0}, that character is already chosen, please choose another.".format(player.display_name))
                        await game_msg.edit(embed = card_embed)
                except:
                    await game_msg.delete()
                    raise Exception(bold("Draw") +  ": {0} failed to choose a character.".format(player.display_name))
            # mark character as picked
            picks[number] = 1
            # edit embed to bold character
            card_embed.set_field_at(number, name="Char {0}".format(number+1), value = "__"+bold(characters_list[number])+"__")
            # assign character chosen to 
            if player == player1:
                p1_chars.append(characters_list[number])
            else:
                p2_chars.append(characters_list[number])
    # create new embed
    chosen_embed = Embed(title="Final Picks", colour=Colour(0x0fa1dc))
    chosen_embed.add_field(name=player1.display_name, value=", ".join(p1_chars))
    chosen_embed.add_field(name=player2.display_name, value=", ".join(p2_chars))
    await game_msg.delete()
    await channel.send(embed=chosen_embed)
    return "Card draw finished"

@register('github')
@register('lizardbot')
async def github(command, msg, user, channel, *args, **kwargs):
    return await help_lizard('', '', '', '')

@register('help-lizard')
@register('helpliz')
async def help_lizard(command, msg, user, channel, *args, **kwargs):
    if len(msg.split(' ')) > 2:
        raise Exception(bold("Help_Lizard") + ": Too many arguments. " + await help_lizard('','','',''))
    help_commands = kwargs.get('help', False)

    split = msg.lower().split(' ')
    cmd = ' '.join(split[0:2]) if len(split) > 1 else split[0]

    if not help_commands:
        return "For more information about the bot and its commands: <https://github.com/lizardman301/Lizard-bot-rsf>"
    elif not split[0]:
        return ('Allows you to get help on a command. '
                '\nThe available commands are ```%s```' % ', '.join(list(help_commands.keys())))
    elif cmd in help_commands.keys():
        return help_commands[cmd]
    else:
        raise Exception(bold("Help_Lizard") + ": Invalid command: " + bold(cmd) + ". Ensure you are using the full command name."
                '\nThe available commands are ```%s```' % ', '.join(list(help_commands.keys())))

@register('lizardbot-discord')
@register('lizdiscord')
async def lizdiscord(command, msg, user, channel, *args, **kwargs):
    return "To reach out and ask questions about the bot, join https://discord.gg/94Pyh6KZTw"

@register('not-in-discord')
@register('nid')
async def not_in_discord(command, msg, user, channel, *args, **kwargs):
    return bold("Your Discord nickname must match your challonge. If it does *NOT*, you will show as *NOT IN DISCORD*")

@register('lizardman')
@register('ping')
@register('liz')
async def ping(command, msg, user, channel, *args, **kwargs):
    print("Pinged by {0}".format(user))
    return "Fuck you, Lizardman"

@register('pingtest')
@register('pt')
async def pingtest(command, msg, user, channel, *args, **kwargs):
    return read_db('channel', 'pingtest', channel.id)

@register('prefix-lizard')
@register('prefliz')
async def prefix(command, msg, user, channel, *args, **kwargs):
    return "The prefix is: {0}".format(read_db('guild', 'prefix-lizard', kwargs['guild']))

@register('randomselect')
@register('random')
@register('rs')
@register('stageselect')
async def randomselect(command, msg, user, channel, *args, **kwargs):
    if (command == 'stageselect' and len(msg.split(' ')) > 0) or len(msg.split(' ')) > 1:
        raise Exception(bold("RandomSelect") + ": Too many arguments. " + await help_lizard('','','',''))
    # Start with randomselect basis to get characters
    # If using stageselect, make it t7stages
    if command == 'stageselect':
            game = 't7stages'
    else:
        if msg.split(' ')[0].lower() != '':
            game = msg.split(' ')[0].lower()
        else:
            # No game to be found so default to sfv
            game = 'sfv'

    chars, games = get_random_chars(game)
    if not chars:
        raise Exception(bold("RandomSelect") + ": Invalid game: {0}. Valid games are: {1}".format(bold(game), bold(', '.join(games))))
    if game == "t7stages":
            return "{0} Your randomly selected stage is: {1}".format(user.mention, bold(random_choice(chars)))
    return "{0} Your randomly selected character is: {1}".format(user.mention, bold(random_choice(chars)))

@register('stats')
async def stats(command, msg, user, channel, *args, **kwargs):
    cmd = msg.split(' ')[0].lower() if msg.split(' ')[0] else ''
    func_map = kwargs['func_map'] if cmd else []
    if len(msg.split(' ')) > 1:
        raise Exception(bold("Stats") + ": Too many arguments. " + await help_lizard('','','',''))
    elif cmd and cmd not in func_map:
        raise Exception(bold("Stats") + ": Invalid Subcommand. " + await help_lizard('','','',''))
    stats = read_stat(cmd,func_map)

    embed = Embed(title="Stats!", colour=Colour(0x0fa1dc))
    embed.set_author(name="Lizard-BOT", url="https://github.com/lizardman301/Lizard-bot-rsf", icon_url="https://raw.githubusercontent.com/lizardman301/Lizard-bot-rsf/master/doc/assets/images/cmface.png")
    embed.set_footer(text="People use this bot? Wild.")
    for stat in stats:
        embed.add_field(name=stat, value=stats[stat])

    try:
        await channel.send(embed=embed)
    except:
        raise Exception(bold("Stats") + ": Error sending embed to chat. Give Lizard-BOT the permission: " + bold("Embed Links"))

    return ''

@register('status')
async def status(command, msg, user, channel, *args, **kwargs):
    currentRound = read_db('channel', 'round', channel.id)
    if currentRound:
        # Read the status message for a channel and make it bold
        # Currently the message must have {0} so it can fill in the current round
        try:
            return bold(read_db('channel', 'status', channel.id).format(currentRound))
        except:
            raise Exception(bold("Status") + ": Round message includes invalid {}. Please correct the status message to include only {0}")
    return bold("Tournament has not begun. Please wait for the TOs to start Round 1!")

@register('stream')
async def stream(command, msg, user, channel, *args, **kwargs):
    return read_db('channel', 'stream', channel.id)

@register('tos')
async def TOs(command, msg, user, channel, *args, **kwargs):
    tos = read_db('channel', 'tos', channel.id)
    # If we get a value back, return TOs
    if tos:
        return tos
    return "There are no TOs associated with this channel."

# Admin Commands

@register('challonge')
@register('chal')
async def challonge(command, msg, user, channel, *args, **kwargs):
    async with channel.typing():
        base_url = "https://api.challonge.com/v1/tournaments/" # Base url to access Challonge's API
        subcommand = msg.split(' ')[0].lower() # The function trying to be accomplished

        if not subcommand:
                raise Exception(bold("Challonge") + ": Lack of arguments. " + await help_lizard('','','',''))

        if len(msg.split(' ')) > 3:
            raise Exception(bold("Challonge") + ": Too many arguments. " + await help_lizard('','','',''))

        try:
            if msg.split(' ')[1].isdigit():
                raise Exception("Bracket link is only digits.")
            tour_url = msg.split(' ')[1] # Bracket to pull from
        except:
            tour_url = get_chal_tour_id(read_db('channel', 'bracket', channel.id)) # no bracket provided, give it one from DB
            if not tour_url: # no bracket found still, return so we dont have issues
                raise Exception(bold("Challonge") + ": Bracket link is missing. Try setting the bracket command or including it in the command")

        subdomain = read_db('guild', 'challonge', kwargs['guild']) # Server's subdomain with Challonge

        # Properly add the subdomain to the bracket url
        if subdomain:
            tour_url = subdomain + '-' + tour_url

        # Get the participants for the tournament
        parts_get = requests_get(base_url + tour_url + "/participants.json", params={'api_key':api_key})
        if '200' in str(parts_get.status_code):
            parts = parts_get.json() # Convert response from json to Python Dictionary

            # If Checkin
            if subcommand == 'checkin':
                not_checked_in_parts, not_discord_parts = checkin(parts, get_users(kwargs['full_msg']))

                # Message showing who is not checked in and who is not in the Discord
                return_msg = "**NOT CHECKED IN:** {0}\n**NOT IN DISCORD:** {1}\n".format(', '.join(not_checked_in_parts), ', '.join(not_discord_parts)) + await not_in_discord(0,0,0,0)

            # If Seeding
            elif subcommand == 'seeding':
                # If msg has 3 params left 3rd one must be seed number
                # Else, seed whole bracket
                try:
                    if msg.split(' ')[-1] == subcommand or msg.split(' ')[-1] in tour_url:
                        seed_num = 0
                    elif not msg.split(' ')[-1].isdigit() and not int(msg.split(' ')[-1]) >= 0:
                        raise
                    else:
                        seed_num = int(msg.split(' ')[-1])
                except:
                    raise Exception(bold("Challonge") + ": Seeding number must be a positive integer or 0 for everybody")

                # Get Google Sheets ID
                sheet_id = read_db('channel', 'seeding', channel.id)

                # If seeding hasn't been set, inform user
                if not sheet_id:
                    raise Exception(bold("Challonge") + ": There is no seeding sheet for this channel. Please view <https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md> for a walkthrough")

                seeds = seeding(sheet_id, parts, base_url + '/' + tour_url,seed_num)

                # Seeding takes place in different method
                await channel.send("**SEEDING:**\n {0}".format(',\n'.join(escape_markdown(pformat(seeds))[1:-1].split(', '))))

                # Final message that seeding is complete
                return_msg = bold("SEEDING IS NOW COMPLETE!\nPLEASE REFRESH YOUR BRACKETS\nWAIT FOR THE ROUND 1 ANNOUNCEMENT TO START PLAYING")

            # Bad command catching
            else:
                raise Exception(bold("Challonge") + ": Invalid Challonge subcommand. " + await help_lizard('','','',''))

            return return_msg # Return the final message
        elif '404' in str(parts_get.status_code):
            raise Exception(bold("Challonge") + ": Lizard-BOT can not find tournament: " + tour_url)
        else:
            print(parts_get.text)
            raise Exception(bold("Challonge") + ": Unknown Challonge error for " + tour_url)

@register('disable')
async def disable(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')

    if len(msg.split(' ')) > 1:
        raise Exception(bold("Disable") + ": Too many arguments. " + await help_lizard('','','',''))

    to_disable = params[0].lower() # could be expanded to do more

    if not to_disable:
        # No command provided
        raise Exception(bold("Disable") + ": No command provided")
    elif to_disable == "list":
        # Optional arg to list disabled commands
        current_list = read_disable(kwargs['guild'])
        return "Current disabled commands are: **{0}**".format(", ".join(current_list))

    try:
        # get the actual function name
        function_name = kwargs['func_map'][to_disable].__name__
    except:
        # Not a valid command in the first place, don't disable
        raise Exception(bold("Disable") + ": That is not a command in Lizard-BOT and cannot be disabled")

    try:
        # Disable function name
        current_list = set_disable(kwargs['guild'],function_name)
    except Exception as e:
        if str(e) == "Command already disabled.":
            raise Exception(bold("Disable") + ": Cannot disable an already disabled command")
        elif str(e) == "Cannot disable important command.":
            raise Exception(bold("Disable") + ": Cannot disable an essential command")

    return "{0} has been disabled. Current disabled commands are: **{1}**".format(to_disable, ", ".join(current_list))

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
        if not full_msg.role_mentions or len(full_msg.role_mentions) > 1:
            raise Exception(bold("Edit") + " : Too few/many role mentions for botrole. Try again with only one role mentioned")
        elif full_msg.role_mentions:
            db_message = str(full_msg.role_mentions[0].id)
            channel_message = full_msg.role_mentions[0].name
        # Allow @everyone to be a botrole
        elif not params:
            db_message = str(full_msg.guild.default_role.id)
            channel_message = full_msg.guild.default_role.name
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

@register('enable')
async def enable(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')

    if len(msg.split(' ')) > 1:
        raise Exception(bold("Enable") + ": Too many arguments. " + await help_lizard('','','',''))

    to_enable = params[0].lower() # could be expanded to do more

    if not to_enable:
        # No command provided
        raise Exception(bold("Enable") + ": No command provided")

    try:
        function_name = kwargs['func_map'][to_enable].__name__
    except:
         # Not a valid command in the first place
         raise Exception(bold("Enable") + ": " + bold(to_enable) + " is not a command in Lizard-BOT and cannot be enabled")

    try:
        current_list = set_enable(kwargs['guild'], function_name)
    except Exception as e:
        if str(e) == "Command is not disabled.":
            raise Exception(bold("Enable") + ": Cannot enable a command that is not disabled.")
        elif str(e) == "There is nothing disabled.":
            raise Exception(bold("Enable") + ": There is currently nothing disabled.")

    return "{0} has been enabled. Current disabled commands are: **{1}**".format(to_enable, ', '.join(current_list))

@register('refresh')
async def refresh(command, msg, user, channel, *args, **kwargs):
    return bold("REFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS")

@register('remind')
async def remind(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')
    try:
        time = int(params[0]) #time is in minutes
        if time < 1:
            raise
    except:
        raise Exception(bold("Remind") + ": Invalid time. Please try again with a positive whole value for minutes")
    reason = ""
    #specific reason if provided
    if len(params) > 1:
        reason = " ".join(params[1:])
        if len(reason) > 1900:
            raise Exception(bold("Remind") + ": Message is too long to be sent back through Discord. Shorten your message to 1900 characters or less")

    if reason:
        formatted_msg = "OK! I will ping you in {0} minutes to remind you about \"{1}\"".format(time,reason)
    else:
        formatted_msg = "OK! I will ping you in {0} minutes to remind you about something.".format(time)

    # sends message back to confirm reminder
    await channel.send(formatted_msg)

    # wait message time
    await asyncio_sleep(60 * time)
    if reason:
        formatted_msg = bold("{0}: It has been {1} minutes, don't forget \"{2}\"!").format(user.mention,time,reason)
    else:
        formatted_msg = bold("{0}: It has been {1} minutes, you have been reminded!".format(user.mention,time))

    await channel.send(formatted_msg)

@register('reset')
async def reset(command, msg, user, channel, *args, **kwargs):
    save_db('channel', 'round', '', channel.id)
    return "Round has been reset."

@register('round')
async def round_lizard(command, msg, user, channel, *args, **kwargs):
    if len(msg) > 50:
        raise Exception(bold("Round_Lizard") + ": Custom round number must be less then 50 characters")
    save_db('channel', 'round', msg, channel.id)
    try:
        return await status('status', msg, user, channel)
    except:
        raise Exception(bold("Round_Lizard") + ": Round message includes invalid {}. Please correct the status message to include only {0}")