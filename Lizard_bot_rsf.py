
import discord
import asyncio
import datetime
import operator
import pickle
from datetime import datetime
from threading import Timer
from discord.ext import commands

client = discord.Client()

prefix = '!'

def makebold(s):
    return "**" + s + "**"

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('-------------------------------')

    #remind people about rr

#variables that we use
currentRound = 0

#restore previous data stored in a pickle file
with open('data.pkl', 'rb') as f:
    currentRound = pickle.load(f)

def save_data():
    #saves data to a pickle file incase something goes wrong and computer goes down
    global currentRound
    with open("data.pkl", "wb") as f:
        pickle.dump([currentRound],f)

@client.event
async def on_message(message):
    global currentRound

    if message.author == client.user:
        return

    if not message.content.startswith(prefix):
        return

    command = message.content.split(' ')[0]
    command = command[1:]
    if len(message.content.split(' ')) > 1:
        params = message.content.split(' ')[1:]
    else:
        #create empty list
        params = [];

    #TO only commands
    if "TOs" in [y.name for y in message.author.roles]:
        #reset round count to 0
        if command == "reset":
            msg = "Resetting round count..."

            currentRound = 0
            await message.channel.send(msg)
            print("Round count reset.")
            #save after every update
            save_data()

        #set what round winners can play
        elif command == "round":
            if len(params) < 1:
                msg = "Usage: !round <round number>"
                await message.channel.send(msg)
            else:
                currentRound = params[0]
                msg = makebold("Winner's Round {0} can play! Losers can play till top 8 losers side. If you have a bye Round {0}, Please Wait!".format(currentRound))
                await message.channel.send(msg)
                print("Round is now {0}".format(currentRound))
                #save after every update
                save_data()

        #annoy people to refresh brackets
        elif command == "refresh":
            msg = makebold("REFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS")
            await message.channel.send(msg)
        
        #remind message author after a ceratin period of time (minutes)
        elif command == "remind":
            #time is in minutes
            msg = ""
            time = int(params[0])
            reason = ""
            #specific reason if provided
            if len(params) > 1:
                r_list = params[1:]
                reason = " ".join(r_list)

            user = message.author
            if len(reason) == 0:
                msg = "OK! I will ping you in {0} minutes to remind you about something.".format(time)
            else:
                msg = "OK! I will ping you in {0} minutes to remind you about \"{1}\"".format(time,reason)
            await message.channel.send(msg)
            print("Reminding {0} in {1} minutes for {2}...".format(user,time,reason))
            
            #wait message time
            await asyncio.sleep(60 * time)
            if len(reason) == 0:
                msg = makebold("{0} its been {1} minutes, you have been reminded!".format(user.mention,time))
            else:
                msg = makebold("{0} its been {1} minutes, don't forget \"{2}\"!").format(user.mention,time,reason)
            print("{0} has been reminded after {1} minutes.".format(user,time))
            await message.channel.send(msg)

    #General use commands
    if command == "ping-lizard":
        print(message.author.id)
        if message.author.id == 198958659986784256:
            msg = "Fuck you, Lizardman"
        else:
            msg = "Pong!"

        await message.channel.send(msg);

    #allows players to see what round it was
    elif command == "status":
        if currentRound == 0:
            msg = makebold("Tournament has not begun. Please wait for the TOs to start Round 1!")
        else:
            msg = makebold("Winner's side Round {0} is allowed to play! Losers can play till top 8.".format(currentRound))
        await message.channel.send(msg)

    #lists all commands
    elif command == "help-lizard":
        msg = "Player commands ```\n{0}current-round``` \nTO commands ```{0}ping-lizard\n{0}refresh\n{0}remind <time> [reason] \n{0}reset \n{0}round <#> ```"
        await message.channel.send(msg)




client.run('MzE3Mjk0NDE0Mzc0NTAyNDAw.XbOmWw.mnyrpCOCAgykBhGyhmlEivttsVo')