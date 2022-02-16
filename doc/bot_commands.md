# In-depth Guide to Lizard-BOT commands
This is an extension of the original short list on the [main Github page](https://github.com/lizardman301/Lizard-bot-rsf). The purpose of this extension is to go more in depth on how each command can be used.
If a command is followed by arguments, `<argument>` will indicated a mandatory argument while `[argument]` will indicate an optional argument.
If a command is restricted, it can only be used by people who have the assigned botrole.
Shorter names for commands will be listed with shortcuts.
All commands will assume the prefix of `!` is used.

## `!botrole`
![!botrole example](/doc/assets/images/botrole.png)

Restricted: No

Shortcuts: `!role`

When used the botrole will return the name of the role that currently is used to restrict access to certain commands.

## `!bracket`
![!botrole example](/doc/assets/images/bracket.png)

Restricted: No

Shortcuts: None

Shows the current bracket set in the channel. Can include text also besides just bracket link.  If a Challonge link is in the text, the `!challonge` commands can automatically use the links.

## `!challonge checkin`
![!challonge checkin example](/doc/assets/images/challonge_checkin.png)

Restricted: Yes

Shortcuts: `!chal checkin`

There must be a valid Challonge link in your `!bracket` command

If you are a community you must set a subdomain using `!edit challonge <subdomain>`.
If you have a pro-community, use your custom subdomain e.g., redditfighting of redditfighting.challonge.com.
If you are not a pro-community in Challonge, you will have to find and copy the jumble of symbols that is your community's subdomain. Go to your Challonge community page, and go to community settings. Look for the part that says Subdomain PRO and look for the box beneath it. This is your community subdomain.

 * Checks the given bracket for users that are not checked in and users whose Challonge names are not in the Discord server
 * Players will be found based on their Challonge nickname existing as a Discord nickname
 * Tells players to change their Discord nickname to match their Challonge nick for best usage

## `!challonge here <player's Challonge display name>`
![!challonge here example](/doc/assets/images/challonge_here.png)

Restricted: No

Shortcuts: `!chal here`

There must be a valid Challonge link in your `!bracket` command

If you are a community you must set a subdomain using `!edit challonge <subdomain>`.
If you have a pro-community, use your custom subdomain e.g., redditfighting of redditfighting.challonge.com.
If you are not a pro-community in Challonge, you will have to find and copy the jumble of symbols that is your community's subdomain. Go to your Challonge community page, and go to community settings. Look for the part that says Subdomain PRO and look for the box beneath it. This is your community subdomain.

* Uses Challonge's API to checkin the user provided.

If the Challonge community tournament does not add the ["LizardBOT" Challonge account](https://challonge.com/users/LizardBOT) as a collaborator or a tournament hosted by a Challonge user, this command will **NOT** work.
This is because tournaments are read-only by default. Any attempts by Lizard-BOT to check in a player will fail since "LizardBOT" doesn't have permission to make changes.

## `!challonge report <score> <winning player's Challonge display name>`
![!challonge report example](/doc/assets/images/challonge_report.png)

Restricted: No

Shortcuts: `!chal report`

There must be a valid Challonge link in your `!bracket` command

If you are a community you must set a subdomain using `!edit challonge <subdomain>`.
If you have a pro-community, use your custom subdomain e.g., redditfighting of redditfighting.challonge.com.
If you are not a pro-community in Challonge, you will have to find and copy the jumble of symbols that is your community's subdomain. Go to your Challonge community page, and go to community settings. Look for the part that says Subdomain PRO and look for the box beneath it. This is your community subdomain.

* Uses Challonge's API to pull data for the open matches to update the winner and score of one open match

If the Challonge community tournament does not add the ["LizardBOT" Challonge account](https://challonge.com/users/LizardBOT) as a collaborator or a tournament hosted by a Challonge user, this command will **NOT** work.
This is because tournaments are read-only by default. Any attempts by Lizard-BOT to update match results will fail since "LizardBOT" doesn't have permission to make changes.

## `!challonge seeding [number of players to seed(Must be integer greater than or equal to 1)]`
![!challonge seeding example](/doc/assets/images/challonge_seeding.png)

Restricted: Yes

Shortcuts: `!challonge seed, !chal seeding, !chal seed`

There must be a valid Challonge link in your `!bracket` command

If you are a community you must set a subdomain using `!edit challonge <subdomain>`.
If you have a pro-community, use your custom subdomain e.g., redditfighting of redditfighting.challonge.com.
If you are not a pro-community in Challonge, you will have to find and copy the jumble of symbols that is your community's subdomain. Go to your Challonge community page, and go to community settings. Look for the part that says Subdomain PRO and look for the box beneath it. This is your community subdomain.

If the number of players to seed is not specified, this will seed the whole bracket.

 * Seeds the tournament based on points in the spreadsheet and the number of players to seed
 * Read more about setting up seeding [here]((https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md)

If the Challonge community tournament does not add the ["LizardBOT" Challonge account](https://challonge.com/users/LizardBOT) as a collaborator or a tournament hosted by a Challonge user, this command will **NOT** work.
This is because tournaments are read-only by default. Any attempts by Lizard-BOT to update the seeding will fail since "LizardBOT" doesn't have permission to make changes.

## `!coin-flip`
![!coin-flip example](/doc/assets/images/coin-flip.png)

Restricted: No

Shortcuts: `!flip` `!cf`

The bot will flip a coin (metaphorically speaking) and return either heads or tails.
Fun fact: If 4 heads show up in a row, a Gief player just won a round by SPD'ing 4 times.

## `!disable [command]`
![!disable example](/doc/assets/images/disable.png)

Restricted: Yes

Shortcuts: None

Using this with any command (besides !disable, !edit, and !enable) in Lizard-BOT to disable its use throughout the server.  Useful if people are abusing a command or it is unneccessary for what you are running.  Use !enable to undo this action. This will disable all versions of the command (IE disabling !liz will disable !lizardman and !ping also). If you provide 'list' as a command, it will list the current disabled commands.

PS If you disable any variation of !lizardman I will be very sad.

## `!draw [mention] <game>`
![!draw example](/doc/assets/images/draw.png)

Restricted: No

Shortcuts: None

Conducts a card draw with the message sender and the user mentioned. Game will default to SFV if no game is given.
First the other user must accept the draw. The player that goes first is randomly chosen by the bot.
Then 7 random characters are drawn, 2 are banned and 4 are picked.  Everything is controlled by reactions with the order given by the bot.

## `!edit <setting> [channel(s)] <value>`
![!edit example](/doc/assets/images/edit_example1.png)

Restricted: Yes

Shortcuts: None

Allows you to edit responses/settings for Lizard-BOT.
There are multiple settings that can be edited to allow customization.
If no channel is specified, changes for channel specific edits will affect only the channel the command is sent in.
If multiple channels are listed, the setting will be updated to the same value across all listed channels.
Server-wide edit commands do not require a channel to be specified.
##### Server-wide
 * botrole <@role>
	 * This role determines what role is needed to access the TO Commands
	 * New value must be a ping to the role desired
	 * Default value: @everyone
 * challonge <subdomain>
	 * Specifies the Challonge subdomain to check for tournaments
	 * Necessary for Challonge integration
	 * Default Value:
 * prefix-lizard <single character to use as a prefix>
	 * Allows you to change the prefix for commands
	 * Useful if you use multiple bots that may have similar commands and prefixes
	 * Default Value: !

##### Channel-Specific
 * bracket <string>
	 * Allows you to add a link to a bracket for users to view
	 * Unique for each channel
	 * Default value: 'There is no bracket set for this channel'
 * lobby <string>
	 * Allows you to add lobby information (like for a Strive tourney)
	 * Unique for each channel
	 * Default value: 'There is no lobby information set for this channel
 * pingtest <string>
	 * Allows you to add a link to a speedtest and instructions for how to prefer a speedtest
	 * Unique for each channel
	 * Default value: Use <https://testmyspeed.onl/> for ping tests.
 * seeding <Sheets ID>
	 * Allows you to set the Google Sheets spreadsheet ID to be used to check points
	 * Please see: [Our Documentation](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md) for instructions on creating/adapting a spreadsheet
	 * Unique for each channel
	 * Default value:
 * status <string>
	 * Allows you to change the flavor text of the !round and !status commands for individual channels
	 * Text uses {0} as a marker for where the round count will be added
	 * Unique for each channel
	 * Default value: Winner's Round {0} can play! Losers can play till top 8 losers side. If you have a bye Round {0}, Please Wait!
 * stream <string>
	 * Allows you to add a stream link for users to easily access without prior knowledge or pinging an admin
	 * Unique for each channel
	 * Default value: There are no streams set for this channel
 * TOs <@user>
	 * Allows you to list all Tournament Organizers involved
	 * Recommended to make it ping each individual TO
	 * Unique for each channel
	 * Default value:


## `!enable [command]`
![!enable example](/doc/assets/images/enable.png)

Restricted: Yes

Shortcuts: None

Using this with any command in Lizard-BOT to enable a previously disabled command.

## `!glossary <term>`
![!glossary example](/doc/assets/images/glossary.png)

Restricted: No

Shortcuts: `!g`

Looks up a term using the https://glossary.infil.net/ glossary. Returns the homepage if no term is provided.

## `!github`
![!github example](/doc/assets/images/github.png)

Restricted: No

Shortcuts: `!lizardbot`

Returns the link to the Lizard-BOT repository on GitHub

## `!help-lizard [command]`
![!help-lizard example](/doc/assets/images/help-lizard.png)

Restricted: No

Shortcuts: `!helpliz`

Returns the list of commands for Lizard-BOT. Providing a command in the argument will return a short description for that command.

## `!lizardbot-discord`
![!lizardbot-discord example](/doc/assets/images/lizardbot-discord.png)

Restricted: No

Shortcuts: `!lizdiscord`

Displays the invite link to join the Lizard-BOT Discord Server for additional help.

## `!lizardman`
![!lizardman example](/doc/assets/images/lizardman.png)

Restricted: No

Shortcuts: `!ping` `!liz`

Ping! Pong! with some zest.  Used to check if Lizard-BOT is currently running and to leave feedback for Lizardman.

## `!lobby`
![!lobby example](/doc/assets/images/lobby.png)

Restricted: No

Shortcuts: None

Displays set lobby information for the channel.


## `!not-in-discord`
![!not-in-discord example](/doc/assets/images/not-in-discord.png)

Restricted: No

Shortcuts: `!nid`

Repeats the same message at the end of `!challonge checkin` to let users know their Discord nickname must match their Challonge nickname.

## `!pingtest`
![!pingtest example](/doc/assets/images/pingtest.png)

Restricted: No

Shortcuts: `!pt`

Explains how to run a ping test using <https://testmyspeed.onl/>. Can be edited to match the rules for any tournament's specific ping test rules.  Recommended to include short instructions to specificy exactly how to conduct the ping test with your opponent.

## `!prefix-lizard`
![!prefix-lizard example](/doc/assets/images/prefix-lizard.png)

Restricted: No

Shortcuts: `!prefliz`

Prints the prefix currently in use for Lizard-BOT. Will always respond to the "!" prefix.

## `!randomselect [character/stage] [game]`
![!randomselect example](/doc/assets/images/randomselect.png)

Restricted: No

Shortcuts: `!random` `!rs`

Returns a randomly selected character or stage from the game in the arguments. Will return a SFV character if no game is given. Assumes character if character or stage is not specified.
If a game that does not exist is provided as an argument, it will return the list of acceptable games.
Current games are **3s, footsies, gbvs, mk11, samsho, sfv, strive, t7, uni, xrd, +r**
Current stages are **llb, t7**

## `!refresh`
![!refresh example](/doc/assets/images/refresh.png)

Restricted: Yes

Shortcuts: None

Lizard-BOT will spam the channel with a message telling players to refresh their bracket pages.  Use this after seeding is finished or when the tournament has started.

## `!remind <time in minutes> [reason]`
![!remind example](/doc/assets/images/remind.png)

Restricted: Yes

Shortcuts: None

Lizard-BOT will set a timer and remind the user who sent the command after the timer is done (with a specified reason if provided).

## `!reset`
![!reset example](/doc/assets/images/reset.png)

Restricted: Yes

Shortcuts: None

This will reset the round count for the current channel back to 0. Using stats after will result in a message saying the tournament hasn't started.
Use after each tourney, so that the round count from the last tourney does not carry over.

## `!round <round number>`
![!round example](/doc/assets/images/round.png)

Restricted: Yes

Shortcuts: None

Changes the current round number to the new value. Can be more than just numbers if you wish to do something different. Immediately sends a status update in the chat.
You can change the specific flavor text with `!edit status`

## `!stats [command]`
![!stats example](/doc/assets/images/stats.png)

Restricted: No

Shortcuts: None

Returns the usage for Lizard-BOT commands. If you provide a command as an argument it will return usage for just that command.
Usage is across all servers.

## `!status`
![!status example](/doc/assets/images/status.png)

Restricted: No

Shortcuts: None

Returns the current round number in a message that can be customized. Round count is set by the `!round` command and uses flavor text from the `status` setting.

## `!stream`
![!stream example](/doc/assets/images/stream.png)

Restricted: No

Shortcuts: None

Returns the stream link if one is set. Can be more than just a link, add flavor text if you wish!

## `!TOs`
![!TOs example](/doc/assets/images/TOs.png)

Restricted: No

Shortcuts: None

Sends a message back with all the Tournament Organizers pinged once set. TOs are specific to each channel.