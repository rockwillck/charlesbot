# bot.py
import os
import random

import discord
from discord import Colour
from discord import Embed
from dotenv import load_dotenv
import dbPy
import asyncio
import math

dbPy.initiate()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    triggers = dbPy.getDBList("triggers")
    responses = dbPy.getDBList("responses")
    if message.author.bot:
        return
    top = ""
    topS = 0
    i = 0
    for trigger in triggers:
        score = 0
        if trigger.lower() in message.content.lower() or message.content.lower() in trigger.lower():
            score += (abs(len(message.content) - len(trigger))/len(message.content))*len(triggers)
        if score > topS:
            top = responses[i]
            topS = score

        i += 1

    if topS > (len(triggers)/(len(triggers) - 1)):
        await message.channel.send(top)
    else:
        def check(m):
            global msg

            if m.author != message.author and m.author.bot != True and m.channel == message.channel:
                msg = m.content
                return True

        await client.wait_for('message', check=check)
        triggers.append(message.content)
        responses.append(msg)
        dbPy.storeDBList("triggers", triggers)
        dbPy.storeDBList("responses", responses)


client.run(TOKEN)