# Lizard-BOT

Simple discord bot originally built for the r/streetfighter East Coast online weekly tournament to help players see current round and with some commands for TOs. Support for multiple channels to run multiple tournaments at once and allows for custom prefixes, round flavor text, and more. Requires discord.py and pymysql.

# How to Use

In order to get started, you need to invite Lizard-BOT to the discord server you wish to use to run tournaments.  [Invite link here.](https://discord.com/oauth2/authorize?client_id=317294414374502400&scope=bot&permissions=321600)

Immediately after the bot joins the server use the command `!edit bot_role <role>` with the role of your choice to make it so that only those with that role can access the commands meant for the Tournament Organizers. From there, feel free to use all the commands listed below to adjust the bot to your needs.

## TO Commands

These commands will only be available to be used by those with the role mentioned above.

`!bot_role`
Returns the role that allows access to the administrator commands.

`!edit <setting> <value>`

There are multiple settings that can be edited to allow customization.

 * bot_role
	 * This role determines what role is needed to access the TO Commands
	 * New value must be a ping to the role desired
	 * Default value: @everyone
 * prefix
	 * Allows you to change the prefix for commands
	 * Useful if you use multiple bots that may have similar commands and prefixes
	 * Default Value: !
 * status
	 * Allows you to change the flavor text of the !round and !status commands for individual channels
	 * Text uses {0} as a marker for where the round count will be added
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

`!prefix-lizard`
Prints the prefix currently in use for lizardbot.

`!remind <time in minutes> [reason]`
Allows the user to set a timed reminder. When used it will ping the user, with the reason for the reminder if specified, after the alloted time. Useful if you are have to handle multiple situations at once.

`!refresh`
Sends a message to the chat to let people know to refresh the bracket page.

`!reset`
Resets the round count back to its default value when a tournament is finished.

`!round <round number>`
Changes the current round number to the new value. Can be more than just numbers if you wish to do something different. Immediately sends a status update in the chat.

## General commands
Commands everyone can use

`!help-lizard`
Links back to this page.

`!status`
Returns the current round number in a message that can be customized.  Will let users know if a tournament has not begun.

`!stream`
Returns the stream link, if one is set.

`!TOs`
Sends a message back with all the Tournament Organizers pinged, if set.

## Contributers
* **Nogaremmi** - *Database implentation* - [Twitter](https://twitter.com/Nogarremi)
* **Lizardman** - *Initial work, owner of bot, bug hunting* - [Twitter](https://twitter.com/lizardman301)
* **Axio** - *Initial Idea and general help*

If you have any further questions or concerns, feel free to contact me via discord @lizardman301#0301.