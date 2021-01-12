# Lizard-BOT

Simple discord bot originally built for the [Online Local](https://twitter.com/theonlinelocal) (formerly r/Streetfighter) East Coast SFV weekly tournament to help players see current round and with some commands for TOs. Support for multiple channels to run multiple tournaments at once and allows for custom prefixes, round flavor text, and more. Requires discord.py and pymysql.

# How to Use

In order to get started, you need to invite Lizard-BOT to the discord server you wish to use to run tournaments.  [Invite link here.](https://discord.com/oauth2/authorize?client_id=317294414374502400&scope=bot&permissions=321600)

Immediately after the bot joins the server use the command `!edit botrole <role>` with the role of your choice to make it so that only those with that role can access the commands meant for the Tournament Organizers. From there, feel free to use all the commands listed below to adjust the bot to your needs.

### Note about Challonge

If the Challonge community that organizes the tournaments does **NOT** have a dedicated subdomain, e.g. challonge.com/communities/1c9ef6d4805d8a3071631f4f, then **Challonge's API** will **ALWAYS** be unable to find the tournament.
None of the Challonge integration will work until the community becomes a ["Pro" community](https://challonge.com/communities/about#pro-features) and sets a custom subdomain, e.g. redditfighting.challonge.com

If the Challonge community tournament does not add the ["LizardBOT" Challonge account](https://challonge.com/users/LizardBOT) as a collaborator or a tournament hosted by a Challonge user, the checkin command **WILL** work but the seeding command will **NOT** work.
This is because tournaments are read-only by default. Any attempts by Lizard-BOT to updating seeding numbers will fail since "LizardBOT" doesn't have permissions.

## TO Commands

These commands will only be available to be used by those with the role mentioned above.

`!botrole`
Returns the role that allows access to the administrator commands.

`!challonge <subcommand> <bracket URL identifier> [OPTIONALS]`
Uses Challonge's API to pull data into Discord

Bracket URL identifier is what comes at the end of the URL
For example
	redditfighting.challonge.com/wwyi8jhk
	Bracket URL identifier = wwyi8jhk


##### Subcommands
**Subcommands are still actively being implemented**

 * checkin
	 * Checks the given bracket for users that are not checked in and users whose Challonge names are not in the server
 * seeding <bracket url> [number of players to seed(Must be integer greater than or equal to 1)]
	 * Seeds the tournament based on points in the spreadsheet and the number of players to seed

`!coin-flip`
A coin is flipped and the result is returned. Either heads or tails.

`!edit [channel(s)] <setting> <value>`
There are multiple settings that can be edited to allow customization.

If multiple channels are listed, the setting will be updated to the same value across all listed channels.

##### Server-wide
 * botrole
	 * This role determines what role is needed to access the TO Commands
	 * New value must be a ping to the role desired
	 * Default value: @everyone
 * challonge
	 * Specifies the challonge subdomain to check for tournaments
	 * Necessary for Challonge integration
	 * Default Value:
 * prefix-lizard
	 * Allows you to change the prefix for commands
	 * Useful if you use multiple bots that may have similar commands and prefixes
	 * Default Value: !

##### Channel-Specific
 * bracket
	 * Allows you to add a link to a bracket for users to view
	 * Unique for each channel
	 * Default value: 'There is no bracket set for this channel'
 * seeding
	 * Allows you to set the Google Sheets spreadsheet ID to be used to check points
	 * Please see: [Our Documentation](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md) for instructions on creating/adapting a spreadsheet
	 * Unique for each channel
	 * Default value:
 * status
	 * Allows you to change the flavor text of the !round and !status commands for individual channels
	 * Text uses {0} as a marker for where the round count will be added
	 * Unique for each channel
	 * Default value: Winner's Round {0} can play! Losers can play till top 8 losers side. If you have a bye Round {0}, Please Wait!
 * stream
	 * Allows you to add a stream link that users can ping to get a link of
	 * Unique for each channel
	 * Default value: There are no streams set for this channel
 * tos
	 * Allows you to list all Tournament Organizers involved
	 * Recommended to make it ping each individual TO
	 * Unique for each channel
	 * Default value:

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

`!bracket`
Shows the current bracket set in the channel.

`!help-lizard`
Displays a list of all commands.

`!lizardman`
Ping! Pong!

`!not-in-discord`
Repeats last part of challonge checkin command. Tells people discord nick must match challonge name.

`!pingtest`
Explains how to run a ping test using <https://testmyspeed.onl/> and a common server.

`!prefix-lizard`
Prints the prefix currently in use for Lizard-BOT.

`!randomselect`
Returns a randomly selected character from the current SFV cast. Useful if running a random select tourney.

`!status`
Returns the current round number in a message that can be customized.  Will let users know if a tournament has not begun.

`!stream`
Returns the stream link if one is set.

`!TOs`
Sends a message back with all the Tournament Organizers pinged, if set.

## Contributers
* **Lizardman** - *Initial work, owner of bot, bug hunting* - [Twitter](https://twitter.com/lizardman301)
* **Axio** - *Initial Idea and general help*
* **Nogarremi** - *Database implentation, primary developer* - [Twitter](https://twitter.com/Nogarremi)

## Other Resources
* **[Yaksha Bot](https://github.com/ellipses/Yaksha)** - *Created by ellipses. We used this for additional ideas about proper structuring of code for ease of expandability and readability. Yaksha Bot was released under an MIT license and this bot(Lizard-bot-rsf) is released as Mozilla Public License 2.0 but to ensure ellipses is credited, the functions copied and then edited by the contributors are commented with "# Yaksha" to give credit*

If you have any further questions or concerns, feel free to contact me via discord @lizardman301#0301.
