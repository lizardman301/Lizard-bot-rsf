# Lizard-BOT

Simple discord bot originally built for the [Online Local](https://twitter.com/theonlinelocal) (formerly r/StreetFighter) East Coast SFV weekly tournament to help players see current round and with some commands for TOs. Support for multiple channels to run multiple tournaments at once and allows for custom prefixes, round flavor text, and more. Requires discord.py and pymysql.

# How to Use

In order to get started, you need to invite Lizard-BOT to the discord server you wish to use to run tournaments.  [Invite link here.](https://discord.com/oauth2/authorize?client_id=317294414374502400&scope=bot&permissions=321600)

Immediately after the bot joins the server use the command `!edit botrole <role>` with the role of your choice to make it so that only those with that role can access the commands meant for the Tournament Organizers. From there, feel free to use all the commands listed below to adjust the bot to your needs.

For more information on setting up the bot for use in a Discord server, please see our documentation [here](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/setting_up_bot_in_discord.md)

For a more indepth guide to what each command does, please see our documentation [here](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/bot_commands.md)

### Note about Challonge

If you have a pro-community, use your custom subdomain e.g., **redditfighting** of redditfighting.challonge.com.

If you are **not** a pro-community in Challonge, you will have to find and copy the jumble of symbols that is your community's subdomain. Go to your Challonge community page, and go to community settings. Look for the part that says *Subdomain PRO* and look for the box beneath it. This is your community subdomain.

If the Challonge community tournament does not add the ["LizardBOT" Challonge account](https://challonge.com/users/LizardBOT) as a collaborator or a tournament hosted by a Challonge user, the **checkin** command **WILL** work but the **seeding** and **report** command will **NOT** work.
This is because tournaments are read-only by default. Any attempts by Lizard-BOT to updating seeding numbers or match results will fail since "LizardBOT" doesn't have permissions.

## TO Commands

These commands will only be available to be used by those with the role mentioned above.

`!challonge checkin`
Uses Challonge's API to pull participant data and checks the given bracket for users that are not checked in and users whose Challonge names are not in the server

There must be a valid Challonge link in your `!bracket` command

`!challonge seeding [number of players to seed(Must be integer greater than or equal to 1)]`
Uses Challonge's API to pull participant data and uses Google Sheets API to seed the tournament based on points in the spreadsheet and the number of players to seed

There must be a valid Challonge link in your `!bracket` command

`!disable [command]`
Using this with any command (besides !disable, !edit, and !enable) in Lizard-BOT to disable its use throughout the server.

`!edit <setting> [channel(s)] <value>`
There are multiple settings that can be edited to allow customization.

If multiple channels are listed, the setting will be updated to the same value across all listed channels.

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

`!enable [command]`
Using this with any command in Lizard-BOT to enable a previously disabled command.

`!refresh`
Sends a message to the chat to let people know to refresh the bracket page.

`!remind <time in minutes> [reason]`
Allows the admin to set a timed reminder. When used it will ping the user, with the reason for the reminder if specified, after the alloted time. Useful if you are have to handle multiple situations at once.

`!reset`
Resets the round count back to its default value when a tournament is finished.

`!round <round number>`
Changes the current round number to the new value. Can be more than just numbers if you wish to do something different. Immediately sends a status update in the chat.

## General commands

Commands everyone can use

`!botrole`
Returns the role that allows access to the administrator commands.

`!bracket`
Shows the current bracket set in the channel.

`!challonge here <player's Challonge display name>`
Uses Challonge's API to checkin the user provided.

`!challonge report <score> <winning player's Challonge display name>`
Uses Challonge's API to pull data for the open matches to update the winner and score of one open match

There must be a valid Challonge link in your `!bracket` command

`!coin-flip`
A coin is flipped and the result is returned. Either heads or tails.

`!draw [mention] <game>`
Conducts a card draw with the message sender and the user mentioned. Game will default to SFV if no game is given.
7 random characters are drawn, 2 are banned and 4 are picked.  Everything is controlled by reactions.

`!github`
Displays the link to the GitHub repository for Lizard-BOT

`!help-lizard`
Displays a list of all commands.

`!lizardbot-discord`
Displays the invite link to join the Lizard-BOT Discord Server for additional help.

`!lizardman`
Ping! Pong!

`!not-in-discord`
Repeats last part of challonge checkin command. Tells people discord nick must match challonge name.

`!pingtest`
Explains how to run a ping test using <https://testmyspeed.onl/>. Can be edited to match the rules for any tournament's specific ping test rules.

`!prefix-lizard`
Prints the prefix currently in use for Lizard-BOT.

`!randomselect [char/stage] [game]`
Returns a randomly selected character from the current the specified game. Assumes SFV if no game is given.
Current games are **3s, footsies, gbvs, mk11, samsho, sfv, t7, uni, xrd, +r**
Current stages are **llb, t7**

`!stats [command]`
Returns the list of all commands and the amount of times they have been used across all servers.  Add a command in the argument to return the count for only that command.
The stats database was started on January 22, 2021. Any past uses of commands were not counted.

`!status`
Returns the current round number in a message that can be customized.  Will let users know if a tournament has not begun.

`!stream`
Returns the stream link if one is set.

`!TOs`
Sends a message back with all the Tournament Organizers pinged, if set.

## How to set up your own instance of Lizard-BOT

Please see our documentation [here](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/new_bot_setup.md) for more information about initial configuration

## Contributers
* **Lizardman** - *Initial work, owner of bot, bug hunting* - [Twitter](https://twitter.com/lizardman301)
* **Axio** - *Initial Idea and general help*
* **Nogarremi** - *Database implementation, primary developer* - [Twitter](https://twitter.com/Nogarremi)

## Other Resources
* **[Yaksha Bot](https://github.com/ellipses/Yaksha)** - *Created by ellipses. We used this for additional ideas about proper structuring of code for ease of expandability and readability. Yaksha Bot was released under an MIT license and this bot(Lizard-bot-rsf) is released as Mozilla Public License 2.0 but to ensure ellipses is credited, the functions copied and then edited by the contributors are commented with "# Yaksha" to give credit*

If you have any further questions or concerns, feel free to contact me via discord @lizardman301#0301.
