#!/usr/bin/env python3

import math
from discord import *
import re
import yaml
import random

client = discord.Client(intents=discord.Intents.all())

with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

key = config["key"]
server = config["server"]
role = config["role"]

@client.event
async def on_ready():
    print('-----')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.event
async def on_message(message):
    pattern = r"^!(\d*)x(\d+)$"
    match = re.match(pattern, message)
    if match:
        if match.group(1):
            rounds = int(match.group(1))
            total = 0
            for i in rounds:
                total = 
        else:
            oneRoundRoll
        size = int(match.group(2))
        roll = random.randint(1,size)
    else:
        print("Invalid command or extra text in the message")

async def oneRoundRoll(size):

async def multiRoundRoll(size, rounds):
    
