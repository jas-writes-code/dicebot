#!/usr/bin/env python3

import math
from discord import *
import re
import json
import random

client = discord.Client(intents=discord.Intents.all())

config = json.load(open('settings.json'))

key = config["key"]

@client.event
async def on_ready():
    print('-----')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.event
async def on_message(message):
    pattern = r"^!(\d*)d(\d+)$"
    match = re.match(pattern, message)
    if match:
        if match.group(1):
            rounds = int(match.group(1))
            multiDice(match.group(2), rounds, message)
        else:
            oneRoundRoll(match.group(2), message)
        size = int(match.group(2))
        roll = random.randint(1,size)
    else:
        print("Invalid command or extra text in the message")

async def singleDice(size, message):
    user = message.author.id
    result = random.randint(1, size)
    await message.channel.send(f"<@{user}>, you rolled a **{result}**.")

async def multiDice(size, rounds, message):
    user = message.author.id
    count = 0
    rolls = []
    while count < rounds:
        result = random.randint(0, size)
        rolls.append(result)
        count += 1
    await message.channel.send(f"<@{user}>, your rolls are **{', '.join(map(str, result))}**.")
