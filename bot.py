#!/usr/bin/env python3

from discord import *
import re
import json
import random

client = Client(intents=Intents.all())

config = json.load(open('token.json'))

key = config["key"]

@client.event
async def on_ready():
    print('-----')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    print("The bot works -- this terminal will not provide further feedback unless there is an error. It's safe to detatch this window.")
@client.event
async def on_message(message):
    pattern = r"^!(\d*)d(\d+)$"
    content = message.content
    match = re.match(pattern, content)
    if match:
        size = int(match.group(2))
        if match.group(1) and int(match.group(1)) > 1:
            rounds = int(match.group(1))
            await multiDice(size, rounds, message)
        else:
            await singleDice(size, message)

async def singleDice(size, message):
    try:
        user = message.author.id
        result = random.randint(1, size)
        await message.channel.send(f"<@{user}>, you rolled a **{result}**.")
    except errors.HTTPException:
        await message.channel.send("That's too much, and would probably break discord. Sorry!")

async def multiDice(size, rounds, message):
    try:
        user = message.author.id
        rolls = []
        for x in range(rounds):
            result = random.randint(1, size)
            rolls.append(result)
        await message.channel.send(f"<@{user}>, your rolls are **{', '.join(map(str, rolls))}**.")
    except errors.HTTPException:
        await message.channel.send("That's too much, and would probably break discord. Sorry!")

client.run(str(key))
