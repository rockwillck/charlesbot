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
    shyness = float(dbPy.getDBValue("shyness"))
    if message.author.bot:
        return
    top = ""
    topS = 0
    i = 0
    for trigger in triggers:
        score = 0
        if trigger.lower() in message.content.lower() or message.content.lower() in trigger.lower():
            score += abs(len(message.content) - len(trigger))/(len(message.content) + 1)*len(triggers)
        if score > topS:
            top = responses[i]
            topS = score

        i += 1

    if topS > (len(triggers)/(len(triggers) - shyness)):
        try:
            await message.channel.trigger_typing()
            await asyncio.sleep(math.floor(len(top)/10))
            prob = (random.randint(0, 1000))/1000
            print(prob)
            print(shyness)
            if prob > shyness:
                await message.reply(top, mention_author=random.choice([True, False, False, False, False, False, False, False]))
            else:
                await message.channel.send(top)
            shyness = shyness*0.99999
            dbPy.storeDBValue("shyness", shyness)
        except Exception as e:
            print(e)
            for channel in message.guild.channels:
                try:
                    scream = ""
                    for x in range(random.randint(8, 15)):
                        scream += random.choice(["a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G"])
                    exclamations = "!"*random.randint(0,3)
                    await channel.send(f"{scream} I can't talk in <#{message.channel.id}> and I have something perfect to say" + exclamations)
                    break
                except:
                    pass
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