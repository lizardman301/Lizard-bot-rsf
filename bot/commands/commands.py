from asyncio import sleep as asyncio_sleep # For sleeping specific threads
from discord import Embed, Colour # For setting up Embeds
from random import choice as random_choice # For randomizing arrays
from re import compile as re_compile # Regexing fun not simplified

# Local imports
from commands.utilities import (register, bold, get_randomselect_data, read_db, read_disable, read_stat, save_db, set_disable, set_enable) # Bring in some utilities to help the process

# All @register decorators are a product of reviewing Yaksha
# See utilities.register for more information

@register('botrole')
@register('role')
async def botrole(command, msg, user, channel, *args, **kwargs):
    botrole = await read_db('guild', 'botrole', kwargs['guild'])
    try:
        botrole_name = channel.guild.get_role(botrole).name
    except:
        botrole_name = '@everyone'

    # Pull the role name from the guild's roles
    return "The bot role is {0}".format(bold(botrole_name))

@register('bracket')
async def bracket(command, msg, user, channel, *args, **kwargs):
    # Custom message for setting a bracket
    return await read_db('channel', 'bracket', channel.id)

@register('coin-flip')
@register('flip')
@register('cf')
async def coin_flip(command, msg, user, channel, *args, **kwargs):
    # Randomize the list for coin flip
    return "The coin landed on: {0}".format(bold(random_choice(["Heads", "Tails"])))

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

    chars, games = get_randomselect_data(game)
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
    await accept_msg.add_reaction('❌')    
    await accept_msg.add_reaction('✅')

    try:
        # Wait for the reaction from the correct user
        # lambda function check for the correct reaction and the correct user
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=lambda reaction, user: user == player2 and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and reaction.message == accept_msg)
        if str(reaction.emoji) == '❌':
            raise Exception()
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
                    if not(msg_to_check == game_msg and user_to_check == player):
                        continue
                    reaction_read_emoji = reaction_read.emoji
                    number = unicode_reactions.index(reaction_read_emoji)
                    if picks[number] != 0:
                        # already banned, set as None to make it fail
                        reaction_read_emoji = None
                        card_embed.set_footer(text="{0}, that character is already banned, please choose another.".format(player.display_name))
                        await game_msg.edit(embed = card_embed)
                except Exception as ex:
                    if type(ex).__name__ == "TimeoutError":
                        await game_msg.delete()
                        raise Exception(bold("Draw") + ": {0} failed to ban a character.".format(player.display_name))
                    else:
                        # As of right now, if something else goes wrong its because a reaction its not expecting was sent, go to the next loop
                        continue
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
                    if not(msg_to_check == game_msg and user_to_check == player):
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
                except Exception as ex:
                    if type(ex).__name__ == "TimeoutError":
                        await game_msg.delete()
                        raise Exception(bold("Draw") + ": {0} failed to choose a character.".format(player.display_name))
                    else:
                        # As of right now, if something else goes wrong its because a reaction its not expecting was sent, go to the next loop
                        continue
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
    # Static message for the Lizard-BOT Github
    return await help_lizard('', '', '', '')

@register('help-lizard')
@register('helpliz')
async def help_lizard(command, msg, user, channel, *args, **kwargs):
    # Message should only have two args at most
    if len(msg.split(' ')) > 2:
        raise Exception(bold("Help_Lizard") + ": Too many arguments. " + await help_lizard('','','',''))
    help_commands = kwargs.get('help', False) # Get all the commands for the help message

    split = msg.lower().split(' ')
    cmd = ' '.join(split[0:2]) if len(split) > 1 else split[0]

    # Probably internal query from another command
    if not help_commands:
        return "For more information about the bot and its commands: <https://github.com/lizardman301/Lizard-bot-rsf>"
    # No command specified
    elif not split[0]:
        return ('Allows you to get help on a command. '
                '\nThe available commands are ```%s```' % ', '.join(list(help_commands.keys())))
    # Return the help message
    elif cmd in help_commands.keys():
        return help_commands[cmd]
    # Invalid argument
    else:
        raise Exception(bold("Help_Lizard") + ": Invalid command: " + bold(cmd) + ". Ensure you are using the full command name."
                '\nThe available commands are ```%s```' % ', '.join(list(help_commands.keys())))

@register('lizardbot-discord')
@register('lizdiscord')
async def lizdiscord(command, msg, user, channel, *args, **kwargs):
    # Static message for the our help discord
    return "To reach out and ask questions about the bot, join https://discord.gg/94Pyh6KZTw"

@register('not-in-discord')
@register('nid')
async def not_in_discord(command, msg, user, channel, *args, **kwargs):
    # Static message for why a user would be reported as not in Discord for a Challonge tournament
    return bold("Your Discord nickname must match your challonge. If it does *NOT*, you will show as *NOT IN DISCORD*")

@register('lizardman')
@register('ping')
@register('liz')
async def ping(command, msg, user, channel, *args, **kwargs):
    # Lizard-BOT's version of an !ping command
    print("Pinged by {0}".format(user))
    return "Fuck you, Lizardman"

@register('pingtest')
@register('pt')
async def pingtest(command, msg, user, channel, *args, **kwargs):
    # Custom message used to teach users how to do a ping test
    return await read_db('channel', 'pingtest', channel.id)

@register('prefix-lizard')
@register('prefliz')
async def prefix(command, msg, user, channel, *args, **kwargs):
    # Gets the prefix set for a guild
    return "The prefix is: {0}".format(await read_db('guild', 'prefix-lizard', kwargs['guild']))

@register('randomselect')
@register('random')
@register('rs')
async def randomselect(command, msg, user, channel, *args, **kwargs):
    if len(msg.split(' ')) > 2:
        raise Exception(bold("RandomSelect") + ": Too many arguments. " + await help_lizard('','','',''))
    # Start with randomselect basis to get characters
    random_type = ''
    game = msg.split(' ')[-1].lower()

    if msg.split(' ')[0].lower() != '':
        random_type = msg.split(' ')[0].lower()
    if random_type == "char" or (random_type == game and random_type != 'stage'):
        random_type = "character"

    if random_type == "character":
        if game in ["character", "char"]:
            # No game to be found so default to sfv
            game = 'sfv'
        elif msg.split(' ')[-1].lower() != '':
            game = msg.split(' ')[-1].lower()
        elif msg.split(' ')[-1].lower() == '':
            # No game to be found so default to sfv
            game = 'sfv'

    data, games = get_randomselect_data(game, random_type=random_type)

    if not data:
        raise Exception(bold("RandomSelect") + ": Invalid game: {0}. Valid games are: {1}".format(bold(game), bold(', '.join(games))))

    if random_type == "stage":
            return "{0} Your randomly selected stage is: {1}".format(user.mention, bold(random_choice(data)))
    return "{0} Your randomly selected character is: {1}".format(user.mention, bold(random_choice(data)))

@register('stats')
async def stats(command, msg, user, channel, *args, **kwargs):
    cmd = msg.split(' ')[0].lower() if msg.split(' ')[0] else ''
    func_map = kwargs['func_map'] if cmd else []
    if len(msg.split(' ')) > 1:
        raise Exception(bold("Stats") + ": Too many arguments. " + await help_lizard('','','',''))
    elif cmd and cmd not in ['challonge', 'edit'] and cmd not in func_map:
        raise Exception(bold("Stats") + ": Invalid Subcommand. " + await help_lizard('','','',''))
    stats = await read_stat(cmd,func_map)

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
    currentRound = await read_db('channel', 'round', channel.id)
    if currentRound:
        # Read the status message for a channel and make it bold
        # Currently the message must have {0} so it can fill in the current round
        try:
            message = await read_db('channel', 'status', channel.id)
            return bold(message.format(currentRound))
        except:
            raise Exception(bold("Status") + ": Round message includes invalid {}. Please correct the status message to include only {0}")
    return bold("Tournament has not begun. Please wait for the TOs to start Round 1!")

@register('stream')
async def stream(command, msg, user, channel, *args, **kwargs):
    # Custom message for a stream
    return await read_db('channel', 'stream', channel.id)

@register('tos')
async def TOs(command, msg, user, channel, *args, **kwargs):
    tos = await read_db('channel', 'tos', channel.id)
    # If we get a value back, return TOs
    if tos:
        return tos
    return "There are no TOs associated with this channel."

# Admin Commands

@register('disable')
async def disable(command, msg, user, channel, *args, **kwargs):
    params = msg.lower().split(' ')

    if len(msg.split(' ')) > 2:
        raise Exception(bold("Disable") + ": Too many arguments. " + await help_lizard('','','',''))

    to_disable = ' '.join(params[0:2]) # could be expanded to do more

    if not to_disable:
        # No command provided
        raise Exception(bold("Disable") + ": No command provided")
    elif to_disable == "list":
        # Optional arg to list disabled commands
        current_list = await read_disable(kwargs['guild'])
        return "Current disabled commands are: **{0}**".format(", ".join(current_list))

    try:
        # get the actual function name
        function_name = kwargs['func_map'][to_disable].__name__
    except:
        # Not a valid command in the first place, don't disable
        raise Exception(bold("Disable") + ": That is not a command in Lizard-BOT and cannot be disabled")

    try:
        # Disable function name
        current_list = await set_disable(kwargs['guild'],function_name)
    except Exception as e:
        if str(e) == "Command already disabled.":
            raise Exception(bold("Disable") + ": Cannot disable an already disabled command")
        elif str(e) == "Cannot disable important command.":
            raise Exception(bold("Disable") + ": Cannot disable an essential command")

    return "{0} has been disabled. Current disabled commands are: **{1}**".format(to_disable, ", ".join(current_list))

@register('enable')
async def enable(command, msg, user, channel, *args, **kwargs):
    params = msg.lower().split(' ')

    if len(msg.split(' ')) > 2:
        raise Exception(bold("Enable") + ": Too many arguments. " + await help_lizard('','','',''))

    to_enable = ' '.join(params[0:2]) # could be expanded to do more

    if not to_enable:
        # No command provided
        raise Exception(bold("Enable") + ": No command provided")

    try:
        function_name = kwargs['func_map'][to_enable].__name__
    except:
         # Check if command is in the disable list, if so return that name
         # Used for commands that were disabled but changed in an update
         disable_list = await read_disable(kwargs['guild'])
         if to_enable in disable_list:
             function_name = to_enable
         else:
            raise Exception(bold("Enable") + ": " + bold(to_enable) + " is not a command in Lizard-BOT and cannot be enabled")

    try:
        return "{0} has been enabled. Current disabled commands are: **{1}**".format(to_enable, ', '.join(await set_enable(kwargs['guild'], function_name)))
    except Exception as e:
        if str(e) == "Command is not disabled.":
            raise Exception(bold("Enable") + ": Cannot enable a command that is not disabled.")
        elif str(e) == "There is nothing disabled.":
            raise Exception(bold("Enable") + ": There is currently nothing disabled.")

@register('refresh')
async def refresh(command, msg, user, channel, *args, **kwargs):
    # Static message to yell at users to refresh
    return bold("REFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS")

@register('remind')
async def remind(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')
    try:
        time = int(params[0]) # time is in minutes

        # Time must be positive
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
    # Reset the round command
    await save_db('channel', 'round', '', channel.id)
    return "Round has been reset."

@register('round')
async def round_lizard(command, msg, user, channel, *args, **kwargs):
    # Message must be less than 50 characters
    if len(msg) > 50:
        raise Exception(bold("Round_Lizard") + ": Custom round number must be less then 50 characters")
    await save_db('channel', 'round', msg, channel.id)
    try:
        return await status('status', msg, user, channel)
    except:
        raise Exception(bold("Round_Lizard") + ": Round message includes invalid {}. Please correct the status message to include only {0}")