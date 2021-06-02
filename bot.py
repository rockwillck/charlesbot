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

bigScore = 0
bigStrict = 0
bigTrigger = "N/A"
bigResponse = "N/A"
bigMessage = "N/A"
@client.event
async def on_message(message):
    global bigResponse
    global bigScore
    global bigStrict
    global bigTrigger
    global bigMessage

    triggers = dbPy.getDBList("triggers")
    responses = dbPy.getDBList("responses")
    bad = dbPy.getDBList("bad")
    shyness = float(dbPy.getDBValue("shyness"))
    if message.content == ".stats":
        embedVar = Embed(title="Stats", value="One of the only commands Charles will ever fulfill.", color=Colour.blue())
        embedVar.add_field(name="Shyness", value=f"{shyness*100}%", inline=False)
        embedVar.add_field(name="Phrases", value=len(triggers), inline=False)
        embedVar.add_field(name="Servers", value=len(client.guilds), inline=False)
        x = 0
        for b in bad:
            x += int(b)
        
        avg = 1 - x/len(bad)
        embedVar.add_field(name="Average Accuracy", value=avg, inline=False)
        await message.channel.send(embed=embedVar)
        return
    elif message.content == ".bad":
        embedVar = Embed(title=":(", color=Colour.red())
        history = await message.channel.history().flatten()
        for m in history:
            if m.author == client.user:
                try:
                    i = 0
                    for r in responses:
                        if r == m.content:
                            bad[i] = int(bad[i]) + 1
                            dbPy.storeDBList("bad", bad)
                            shyness = shyness*1.01
                except:
                    pass
                else:
                    break
        await message.channel.send(embed=embedVar)
        return
    elif message.content == ".good":
        embedVar = Embed(title=":)", color=Colour.green())
        history = await message.channel.history().flatten()
        for m in history:
            if m.author == client.user:
                try:
                    i = 0
                    for r in responses:
                        if r == m.content:
                            bad[i] = int(bad[i]) - 1
                            dbPy.storeDBList("bad", bad)
                            shyness = shyness*0.99
                except:
                    pass
                else:
                    break
        await message.channel.send(embed=embedVar)
        return
    elif message.content == ".examine":
        embedVar = Embed(title="Examination!", description=f"""Last Response
```{bigResponse}```
Triggered by
```{bigTrigger}```
Score 
```{bigScore}```
Base message
```{bigMessage}```
Strictness
```{bigStrict}```
""", color=Colour.darker_gray())
        history = await message.channel.history().flatten()
        for m in history:
            if m.author == client.user:
                try:
                    bad[responses.index(m.content)] = int(bad[responses.index(m.content)]) + 1
                    dbPy.storeDBList("bad", bad)
                    shyness = shyness*1.01
                    break
                except:
                    pass
        await message.channel.send(embed=embedVar)
        return
    elif message.content == ".help":
        embedVar = Embed(title="Help", color=Colour.purple())
        embedVar.add_field(name=".stats", value="See Ch@rles's stats.", inline=False)
        embedVar.add_field(name=".examine", value="Examine the last message Ch@rles sent.", inline=False)
        embedVar.add_field(name=".good", value="Reward Ch@rles for good behavior.", inline=False)
        embedVar.add_field(name=".bad", value="Punish Ch@rles for bad behavior..", inline=False)
        await message.channel.send(embed=embedVar)
        return

    if message.author.bot:
        return
    top = ""
    topS = 0
    i = 0
    for trigger in triggers:
        score = 0
        for t in trigger.lower().split():
            if t in message.content.lower():
                score += 1
            score -= int(bad[i])*0.1
        if score > topS:
            trigger2 = trigger
            top = responses[i]
            topS = score

        i += 1

    if topS > (len(message.content.split()) - 10*(1 - shyness)):
        try:
            await message.channel.trigger_typing()
            await asyncio.sleep(math.floor(len(top)/10))
            prob = (random.randint(0, 1000))/1000
            if prob > shyness:
                await message.reply(top, mention_author=random.choice([True, False, False, False, False, False, False, False]))
            else:
                await message.channel.send(top)
            shyness = shyness*0.99999
            dbPy.storeDBValue("shyness", shyness)
        except:
            for channel in message.guild.channels:
                try:
                    scream = ""
                    for x in range(random.randint(8, 15)):
                        scream += random.choice(["a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G"])
                    exclamations = "!"*random.randint(0,3)
                    if topS > (len(message.content.split()) - 2*(1 - shyness)):
                        await channel.send(f"{scream} I can't talk in <#{message.channel.id}> and I have something perfect to say" + exclamations)
                    break
                except:
                    pass
        else:
            bigTrigger = trigger2
            bigStrict = (len(message.content.split()) - 10*(1 - shyness))
            bigScore = topS
            bigResponse = top
            bigMessage = message.content
    else:
        def check(m):
            global msg

            if m.author != message.author and m.author.bot != True and m.channel == message.channel:
                msg = m.content
                return True

        await client.wait_for('message', check=check)
        triggers.append(message.content.replace("\n", "; "))
        responses.append(msg.replace("\n", ";"))
        bad.append(0)
        dbPy.storeDBList("triggers", triggers)
        dbPy.storeDBList("responses", responses)
        dbPy.storeDBList("bad", bad)

client.run(TOKEN)