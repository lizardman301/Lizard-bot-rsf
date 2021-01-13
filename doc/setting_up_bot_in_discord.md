# Setting up Lizard-BOT in your Discord server
This guide will go over the process of setting up Lizard-BOT in your server so you can use it for all your TOing needs.

## 1. Invite Lizard-BOT to your server
Go to [here](https://Discord.com/oauth2/authorize?client_id=317294414374502400&scope=bot&permissions=321600) to invite the bot to your server.  Select your server, click continue, and then authorize. Lizard-BOT should now be in your Discord server

![Select server](/doc/assets/images/select_server.png) ![Authorize bot](/doc/assets/images/authorize_bot.png)

## 2. Setup the botrole

**THIS IS HIGHLY IMPORTANT WHEN SETTING UP, DO NOT SKIP**
Preferably setup a channel beforehand that only the admins and bots can access (you don't want to have the bot setup messing up your chats with information others do not need to see)

As soon as Lizard-BOT is in the server you must edit the botrole in order to set which people can access the TO commands of the bot and who are able to modify it.  In this example server, I use @TOs as the role for who can access those commands.
Type in `!edit botrole <role>` with the role of your choice. If done properly, Lizard-BOT will respond and let you know the botrole is updated. By default, @everyone is the role so you want to change this **immediately** during setup so that no one can needlessly use the commands.

![New botrole command](/doc/assets/images/new_botrole.png)

If you want to test to make sure this is working accurately, have a user without the botrole attempt to do the command `!reset`. A person without the role will get a permission denied message while a person with the @TOs role is able to trigger the command.

![Botrole test example](/doc/assets/images/botrole_test.png)

With that setup properly, you can now modify the bot as you please.

## 3. Edit basic commands and settings

Now you will want to start editing the bot to fit your tournament.  You will be using the `!edit` command for all of this and you must have the role the bot was given in order to make any of these changes. Below is a list of things that can be edited. Be aware some commands are only channel specific e.g., updating the bracket in channel #bracket-1 will not have the bracket updated for the rest of the server. You can provide multiple channels to edit at the same time if you wish.

`!edit [channel(s)] <setting> <value>`
There are multiple settings that can be edited to allow customization.

If multiple channels are listed, the setting will be updated to the same value across all listed channels.

##### Server-wide
 * botrole
	 * This role determines what role is needed to access the TO Commands
	 * New value must be a ping to the role desired
	 * Default value: @everyone
 * challonge
	 * Specifies the Challonge subdomain to check for tournaments
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
 * TOs
	 * Allows you to list all Tournament Organizers involved
	 * Recommended to make it ping each individual TO
	 * Unique for each channel
	 * Default value:

Below is a simple example of how to use the !edit command to setup your bot for the basic commands such as !bracket, !stream, and !TOs.  It is recommended to use a separate channel hidden from the rest of the server in order not to have all this info spam your regular users.

![Editing bot commands](/doc/assets/images/edit_example1.png) ![Testing new bot commands](/doc/assets/images/edit_example2.png)

Use these commands and more to customize the bot to your needs!

## 4. Adding Challonge functionality to the bot
If you are using Challonge, you'll have access to the !challonge checkin and !challonge seeding commands.  In order to use these commands, you will have to do a bit more setup for your tournament.

First make sure the full Challonge link exists in your !bracket command for your tournament. Next, if you are running the Discord from a community, you need to give Lizard-BOT the subdomain for your community with `!edit challonge <subdomain>`.

If you have a pro-community, use your custom subdomain. If you are not a pro-community in Challonge, you will have to find and copy the jumble of symbols that is your community's subdomain. Go to your Challonge community page, and go to community settings. Look for the part that says *Subdomain PRO* and look for the box beneath it. This is your community subdomain. Copy it and use `!edit challonge <subdomain>` to inform Lizard-BOT of your subdomain.

![Community Subdomain Location](/doc/assets/images/challonge_subdomain.png)

With this setup you can now use the !challonge checkin command and the bot will post a list of people not checked in on Challonge and a list of people's usernames that it cannot find in Discord. The bot will attempt to ping users it can find in Discord who are not checked in. It looks for users in Discord by looking for nicknames in Discord that match Challonge nicknames for that specific tournament. It is recommended for players to change their Challonge and Discord nickname to be the same.

If you want to setup seeding, read the [seeding_with_sheets.md](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md) to set that up. This will involve setting up a Google sheets document the bot can see and giving the Bot admin permissions in your Challonge tournament/community.

## 5. How to use the bot for your tournaments
With the bot setup, you can now use it to help your tournaments. Below will be an example of the bot in use during one of the weekly [Online Local](https://twitter.com/theonlinelocal) Tournaments with explanations for what is happening.

![Start of Checkin and bracket command](/doc/assets/images/onlinelocal1.png)
The use of another bot, Carl-Bot, announces the start of checkin. The `!bracket` command is used so that players can access the bracket page.  The Challonge link in !bracket also allows the TO to use Challonge commands.

![Using !challonge checkin](/doc/assets/images/onlinelocal2.png)
Checkin lasts for an hour and the `!challonge checkin` command is used multiple times to let people know to check in. If players have listened and are using the same nickname in both Challonge and Discord, they will be pinged if they are not checked in. If the bot can not find them, they are marked as not in Discord. Players are often confused by not being marked not in Discord. Many times the players in this list will speak up to let the TOs know they are in fact in the Discord. This is the perfect opportunity to ask them to change their nickname in order to match their Challonge info.

![Using !challonge seeding](/doc/assets/images/onlinelocal3.png)
The Online Local uses a point system for all the tournaments throughout the year. This allows them a perfect opportunity to seed based off these points. They have already linked the Google sheets document and Lizard-BOT has permissions in the Challonge community, so all they need to do is use `!challonge seeding 32` to seed the top 32 people. If they had a smaller event, they can easily change the number of people to be seeded.  The bot seeds in Challonge and then lists the people who were seeded in Discord.

For information to set up a Google Sheets to store points, please review [this](https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md)

![Using !refresh](/doc/assets/images/onlinelocal4.png)
After the bracket is seeded and the everything is finalized, the bracket must be refreshed on the players' end so they can see the finalized bracket. The `!refresh` command easily lets people know to do this.

![Using !round](/doc/assets/images/onlinelocal5.png)
With the bracket started in Challonge, it's time to let the players know to start the matches.  The TO picks one or two matches to be played on stream and then tells the rest of the players to play the first two rounds of the bracket with the `!round` command.  This command will accept any string, not just single numbers, so it easily allows one to designate multiple rounds to play.  If a TO wanted to change the instructions in the command, they can use `!edit status <new status>` to have different instructions appear.  Use `{0}` in the new status to mark where the round count should be displayed.

![Using !status](/doc/assets/images/onlinelocal6.png)
Throughout the tournament, players can use the `!status` command in order to see if they are able to play their next match. The format of the message is the same as the `!round` command, but it is unable to modify the current round count.

![Using !remind](/doc/assets/images/onlinelocal7.png)
A lot of things need to be remembered for a tournament, so TOs can use the `!remind <minutes> <reason>` command in order to have the bot remind them about anything.  Usually this is used to give a timer to players who haven't showed up in order to DQ them, but there are plenty of other uses for it.

![Using !round again](/doc/assets/images/onlinelocal8.png)
The `!round` command is used throughout the tournament to let players know when to play their next matches. For the Online Local, once it reaches top 8, it is no longer needed since the rest of the event is ran on stream. After this event finishes, `!reset` is used to reset the round count, and then the `!bracket` command is changed to have the URL for the next week's event.

If you have any questions for setting up Lizard-BOT or questions about the bot in general, contact lizardman via [twitter](https://twitter.com/lizardman301) or on Discord via DM (lizardman301#0301).