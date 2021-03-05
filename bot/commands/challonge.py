from discord.utils import escape_markdown # Regexing fun simplified
from pprint import pformat
from requests import get as requests_get, put as requests_put, post as requests_post
from fuzzywuzzy import fuzz as fuzzywuzzy_fuzz, process as fuzzywuzzy_process
from json import loads as json_loads

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

@register('challonge here')
@register('chal here')
async def challonge_here(command, msg, user, channel, *args, **kwargs):
    here_parts = {}

    params = msg.split(' ') # grab the info from the user
    
    # if not enough arguments, we end early
    if len(params) < 1:
        raise Exception(bold("Challonge_Report") + ": Not enough arguments. Please provide a score and a winner.")

    async with channel.typing():
        parts, tour_url = await start_challonge(command, msg, channel, kwargs['guild'])

        for part in parts:
            here_parts.update({part['participant']['display_name'].lower():part['participant']['id']})

        checkin_post = requests_post(base_url + tour_url + "/participants/" + str(here_parts[msg]) +"/check_in.json", params={'api_key':api_key})

        # Check to make sure we get a good response
        if '200' in str(checkin_post.status_code):
            # Good response. Return that the score was updated
            return "Checked in: {0}".format(bold(msg))
        elif '401' in str(checkin_post.status_code):
            # Permission error
            raise Exception(bold("Challonge_Here") + ": Lizard-BOT does not have access to the tournament")
        elif '422' in str(checkin_post.status_code):
            # Checkin period not running
            raise Exception(bold("Challonge_Here") + ": The check-in window hasn't started or is over for the tournament")
        else:
            # Some other challonge error. Print it to console and error with appropriate message
            print(checkin_post.text)
            raise Exception(bold("Challonge_Here") + ": Unknown Challonge error for <" + tour_url + ">")

        # Message showing who is not checked in and who is not in the Discord
        return 

@register('challonge report')
@register('chal report')
async def challonge_report(command, msg, user, channel, *args, **kwargs):
    match_parts = {} # Stores active participants
    matches = [] # Stores all the match elements at their root [match_obj, etc] instead of {'match': match_obj, etc}

    params = msg.split(' ') # grab the info from the user
    winner_name = ' '.join(params[1:]) # First parameter should be the score. Everything else is the match winner's name
    
    # if not enough arguments, we end early
    if len(params) < 2:
        raise Exception(bold("Challonge_Report") + ": Not enough arguments. Please provide a score and a winner.")

    async with channel.typing():
        parts, tour_url = await start_challonge(command, msg, channel, kwargs['guild']) # Get all the participants and the tournament URL
        match_get = requests_get(base_url + tour_url + "/matches.json", params={'api_key':api_key, 'state':'open'}) # Grab all the active matches for the tournament

        # If we get a good response and there are matches (aka the tournament has been started)
        if '200' in str(match_get.status_code) and match_get.json():
            # Grab every participant and get the useful information (display name and id number)
            # Originally grabbed every checked in participant but this caused issues with tournies who had no check in
            for part in parts:
                match_parts.update({part['participant']['display_name'].lower():part['participant']['id']})
            # Adjust the root of the match information and put it in an array
            for match in match_get.json():
                m = match['match']
                matches.append(m)
        else:
            # Error out if there are no active matches or if we can't get a good call to Challonge
            raise Exception(bold("Challonge_Report") + ": Error fetching matches for <{0}>. Is the tournament started?".format(tour_url))

        # Check to make sure the given winner is in the bracket
        if winner_name.lower() not in match_parts:
            raise Exception(bold("Challonge_Report") + ": {0} is not in the tournament".format(bold(winner_name)))

        # Go through every active match to find one with the winner in it
        for match in matches:
            # Check to see if the winner is in the current match that is being looped
            if not (match['player1_id'] == match_parts[winner_name.lower()] or match['player2_id'] == match_parts[winner_name.lower()]):
                # Check if we went through every match
                if match == matches[-1]:
                    # Error out that the player wasn't in any active match
                    raise Exception(bold("Challonge_Report") + ": User: {0} does not have an open match to report".format(winner_name))
                continue

            scores = params[0].split('-') # First parameter should be the score

            # Check that the score was given in the proper format
            if not len(scores) == 2:
                # Error out and show what a score should look like
                raise Exception(bold("Challonge_Report") + ": {0} is not a valid score. Example score: 2-0".format(bold(params[0])))

            try:
                # Check to see if we need to reverse the score since it has to be p1-p2
                # So if the winner is p1 and the score is p2-p1, reverse the order to be p1-p2
                # Or if the winner is p2 and the score is p2-p1, reverse the order to be p1-p2
                if (match['player1_id'] == match_parts[winner_name.lower()] and int(scores[1]) > int(scores[0])) or (match['player2_id'] == match_parts[winner_name.lower()] and int(scores[0]) > int(scores[1])):
                    scores.reverse()
            except:
                # Error out if unable to convert each score into an int e.g. a-b
                raise Exception(bold("Challonge_Report") + ": {0} is not a valid score. Example score: 2-0".format(bold(params[0])))

            # Time to send out the winner and the score
            match_put = requests_put(base_url + tour_url + "/matches/" + str(match['id']) +".json", params={'api_key':api_key, 'match[winner_id]':match_parts[winner_name.lower()], 'match[scores_csv]':'-'.join(scores)})

            # Check to make sure we get a good response
            if '200' in str(match_put.status_code):
                # Good response. Return that the score was updated
                return "Lizard-BOT reported {0} won {1}!".format(bold(winner_name), bold('-'.join(scores)))
            elif '401' in str(match_put.status_code):
                # Permission error
                raise Exception(bold("Challonge_Report") + ": Lizard-BOT does not have access to the tournament")
            else:
                # Some other challonge error. Print it to console and error with appropriate message
                print(match_put.text)
                raise Exception(bold("Challonge_Report") + ": Unknown Challonge error for <" + tour_url + ">")

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