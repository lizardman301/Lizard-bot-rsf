from asyncio import sleep as asyncio_sleep
from discord import Embed, Colour
from discord.utils import escape_markdown # Regexing fun simplified
from pprint import pformat
from random import random as random_random, choice as random_choice
from re import compile as re_compile
from requests import get as requests_get

# Local imports
from secret import api_key
from commands.commands import (help_lizard, not_in_discord)
from commands.utilities import (register, bold, get_chal_tour_id, get_users, checkin, seeding, read_db)

# All @register decorators are a product of reviewing Yaksha
# See utilities.register for more information

base_url = "https://api.challonge.com/v1/tournaments/"

async def start_challonge(command, msg, channel, guild): # Base url to access Challonge's API
    try:
        tour_url = get_chal_tour_id(await read_db('channel', 'bracket', channel.id)) # Grab tour_url from bracket command
    except:
        raise Exception(bold("Challonge") + ": Bracket link is missing. Try setting the bracket command")

    subdomain = await read_db('guild', 'challonge', guild) # Server's subdomain with Challonge

    # Properly add the subdomain to the bracket url
    if subdomain:
        tour_url = subdomain + '-' + tour_url

    # Get the participants for the tournament
    parts_get = requests_get(base_url + tour_url + "/participants.json", params={'api_key':api_key})
    if '200' in str(parts_get.status_code):
        return parts_get.json(), tour_url
    elif '404' in str(parts_get.status_code):
        raise Exception(bold("Challonge") + ": Lizard-BOT can not find tournament: " + tour_url)
    else:
        print(parts_get.text)
        raise Exception(bold("Challonge") + ": Unknown Challonge error for " + tour_url)

@register('challonge checkin')
@register('chal checkin')
async def challonge_checkin(command, msg, user, channel, *args, **kwargs):
    if msg:
        raise Exception(bold("Challonge_Checkin") + ": Too many arguments. " + await help_lizard('','','',''))

    async with channel.typing():
        parts, tour_url = await start_challonge(command, msg, channel, kwargs['guild'])
        not_checked_in_parts, not_discord_parts = checkin(parts, get_users(kwargs['guild_members']))

        # Message showing who is not checked in and who is not in the Discord
        return"**NOT CHECKED IN:** {0}\n**NOT IN DISCORD:** {1}\n".format(', '.join(not_checked_in_parts), ', '.join(not_discord_parts)) + await not_in_discord(0,0,0,0)

@register('challonge seeding')
@register('challonge seed')
@register('chal seeding')
@register('chal seed')
async def challonge_seeding(command, msg, user, channel, *args, **kwargs):
    if len(msg.split(' ')) > 1:
        raise Exception(bold("Challonge_Seeding") + ": Too many arguments. " + await help_lizard('','','',''))

    async with channel.typing():
        parts, tour_url = await start_challonge(command, msg, channel, kwargs['guild'])
        # If msg has 3 params left 3rd one must be seed number
        # Else, seed whole bracket
        try:
            if not msg:
                seed_num = 0
            elif int(msg.split(' ')[-1]) <= 0:
                raise
            else:
                seed_num = int(msg.split(' ')[-1])
        except:
            raise Exception(bold("Challonge_Seeding") + ": Seeding number must be a positive integer or 0 for everybody")

        # Get Google Sheets ID
        sheet_id = await read_db('channel', 'seeding', channel.id)

        # If seeding hasn't been set, inform user
        if not sheet_id:
            raise Exception(bold("Challonge_Seeding") + ": There is no seeding sheet for this channel. Please view <https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md> for a walkthrough")

        seeds = seeding(sheet_id, parts, base_url + '/' + tour_url, seed_num)

        # Seeding takes place in different method
        await channel.send("**SEEDING:**\n {0}".format(',\n'.join(escape_markdown(pformat(seeds))[1:-1].split(', '))))

        # Final message that seeding is complete
        return bold("SEEDING IS NOW COMPLETE!\nPLEASE REFRESH YOUR BRACKETS\nWAIT FOR THE ROUND 1 ANNOUNCEMENT TO START PLAYING")
