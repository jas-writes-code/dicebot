#!/usr/bin/env python3
import discord

import wrangler
from discord import *
import re, json, random, time, uuid, shlex

client = Client(intents=Intents.all())

token = json.load(open('token.json'))
key = token["key"]
with open("config.json", "r") as f:
    config = json.load(f)

gifs = ["https://tenor.com/btscP.gif", "https://tenor.com/bZ6Dc.gif", "https://tenor.com/bNnGN.gif", "https://tenor.com/bt0Bu.gif", "https://tenor.com/hGCEQSyoiSD.gif", "https://tenor.com/e2krWN7CFON.gif"]

async def setInfo(message, args):
    global character
    character = None
    blocked = ["owner", "creator", "created", "aliases", "images"]
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        name = args[0]
        stat = args[1]
        value = args[2]
        if stat in blocked:
            await message.reply("You can't change those values with !set.")
            return
        character, uid = await wrangler.find(name)
        if not character:
            message.reply(f"*Error:* Character `{name}` not found.\n*Usage:* !set <name/alias/uuid> <infopoint> <value>\n*Note:* Arguments with spaces must be written 'in quotes like this'.")
            return
        if message.author.id == int(character["owner"]) or message.author.id == client.user.id:
            if stat in character["stats"]:
                config['characters'][uid]['stats'][stat] = value
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=4)
                content = f"Updated {character['name']}'s {stat} to `{value}`."
                await message.reply(content)
                return
            elif stat in character:
                config['characters'][uid][stat] = value
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=4)
                content = f"Updated {character['name']}'s {stat} to `{value}`."
                await message.reply(content)
            else: await message.reply(f"Item not found: {stat}")
        else:
            await message.reply("You're not allowed to edit other users' characters!")

async def setImages(message, args):
    global character
    character = None
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        name = args[0]
        character, uid = await wrangler.find(name)
        if not character:
            await message.reply(
                f"*Error:* Character `{name}` not found.\n*Usage:* !image <name/alias/uuid>\n*Note:* Arguments with spaces must be written 'in quotes like this'.")
            return
        if message.author.id == int(character["owner"]) or message.author.id == client.user.id:
            if len(args) == 2 and args[1] == "remove":
                config['characters'][uid]['images'] = []
                return
            if len(message.attachments) == 0:
                await message.reply(f"*Error:* No images found. Attach images to your message to include them in {character['name']}'s profile.")
                return
            for element in message.attachments:
                config['characters'][uid]['images'].append(element.url)
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            await message.reply(f"Added {len(message.attachments)} images to {character['name']}'s profile.")

async def newCharacter(message, args):
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        uid = uuid.uuid4()
        name = args[0]
        payload = {
            "uuid": str(uid),
            "name": name,
            "level": "unset",
            "class": "unset",
            "owner": message.author.id,
            "creator": message.author.id,
            "aliases": [],
            "species": "unset",
            "hist": "unset",
            "stats": {
              "int": "unset",
              "str": "unset",
              "wis": "unset",
              "cha": "unset",
              "dex": "unset",
              "con": "unset"
            },
            "images": [],
            "created": int(time.time())
        }
        config["characters"][str(uid)] = payload
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        sent = await message.reply(f"Created new character `{name}`.")
        await allInfo(sent, args)

async def stats(message, args):
    global character
    character = None
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        name = args[0]
        character, uid = await wrangler.find(name)
        if not character:
            message.reply(
                f"*Error:* Character `{name}` not found.\n*Usage:* !stats <name/alias/uuid>\n*Note:* Arguments with spaces must be written 'in quotes like this'.")
            return
        content = f"Saved roll stats for {character['name']}:\n"
        for element in character["stats"]:
            content += f"{element}: **{character['stats'][element]}**\n"
        await message.reply(content)

async def about(message, args):
    global character
    character = None
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        name = args[0]
        character, uid = await wrangler.find(name)
        if not character:
            await message.reply(f"*Error:* Character `{name}` not found.\n*Usage:* !about <name>\n*Note:* Arguments with spaces must be written 'in quotes like this'.")
            return

        owner = client.get_user(int(character["owner"]))
        creator = client.get_user(int(character["creator"]))

        content = f"**{character['name']}**\n"
        content += f"A Level {character['level']} {character['species']} {character['class']}\n\n"
        content += f"**Backstory:** \n{character['hist']}\n\n"
        content += f"*Owner: {owner.display_name}*\n"
        content += f"*Character was created <t:{character['created']}:R> by {creator.display_name}*\n"
        try:
            await message.reply(content)
        except HTTPException:
            sends = wrangler.thatstoolong(content)
            for element in sends:
                await message.channel.send(element)
        content = ""
        for element in character["images"]:
            content += element
            content += "\n"
        await message.channel.send(content)

async def setAlias(message, args):
    global character
    character = None
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        name = args[0]
        alias = args[1]
        character, uid = await wrangler.find(name)
        if not character:
            message.reply(
                f"*Error:* Character `{name}` not found.\n*Usage:* !alias <name/alias/uuid> <alias> remove ( <-- optional)\n*Note:* Arguments with spaces must be written 'in quotes like this'.")
            return
        if message.author.id == int(character["owner"]):
            if len(args) == 3:
                if args[2] == "remove":
                    for element in character['aliases']:
                        if element == alias:
                            config['characters'][uid]['aliases'].remove(element)
                            with open("config.json", "w") as f:
                                json.dump(config, f, indent=4)
                            await message.reply(f"Removed alias `{alias}` from {character['name']}'s alias list.")
                            return
            config['characters'][uid]["aliases"].append(alias)
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            await message.reply(f"Added `{alias}` to {character['name']}'s alias list.")
        else:
            await message.reply("You're not allowed to edit other users' characters!")

async def allInfo(message, args):
    global character
    character = None
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        name = args[0]
        character, uid = await wrangler.find(name)
        if not character:
            message.reply(f"*Error:* Character `{name}` not found.\n*Usage:* !dump <name/alias/uuid>\n*Note:* Arguments with spaces must be written 'in quotes like this'.")
            return
        if message.author.id == int(character["owner"]) or message.author.id == client.user.id:
            await message.reply(f"```json\n{json.dumps(character, indent=4)}```")
        else:
            await message.reply("You may only request raw data for characters you own!")

async def changeOwner(message, args):
    global character
    character = None
    async with message.channel.typing():
        with open("config.json", "r") as f:
            config = json.load(f)
        name = args[0]
        newID = args[1]
        character, uid = await wrangler.find(name)
        if not character:
            message.reply(
                f"*Error:* Character `{name}` not found.\n*Usage:* !transfer <name/alias/uuid> <new owner id>\n*Note:* Arguments with spaces must be written 'in quotes like this'.")
            return
        newOwner = client.get_user(int(newID))
        if type(newOwner) != discord.User:
            await message.reply(f"*Error:* User with ID `{newID}` not found.\n*Usage:* !transfer <name/alias/uuid> <new owner id>\n*Note:* You must have Discord Developer Settings enabled to find User IDs..")
            return
        if message.author.id == int(character["owner"]) or message.author.id == client.user.id:
            if len(args) == 2:

                content = f"**Are you sure?**\n"
                content += f"You are about to transfer ownership of your character {character['name']} to {newOwner.display_name}!\n"
                content += f"This is potentially VERY destructive and can only be undone if {newOwner.display_name} transfers the character back to you.\n"
                content += f"If you want to continue, type `!transfer {name} {newID} YES`"
                await message.reply(content)
            if len(args) == 3:

                if args[2] == "YES":
                    config['characters'][uid]["owner"] = newID
                    with open("config.json", "w") as f:
                        json.dump(config, f, indent=4)
                    await message.reply(f"Transferred ownership of {character['name']} to {newOwner.display_name}.")
        else:
            await message.reply("You're not allowed to transfer other users' characters!")

async def listCommands(message, args):
    content = "**CharacterDB Commands:**\n\n"
    for element in config["commands"]:
        item = config["commands"][element]
        content += f"**!{element}:** {item['info']}\n"
        content += f"Takes arguments: {item['args']}"
        if item['safety']:
            content += "\n*This command can only be executed by the character owner.*"
        content += "\n\n"
    await message.reply(content)

async def listCharacters(message, args):
    with open("config.json", "r") as f:
        config = json.load(f)
    if len(args) == 0:
        targetID = message.author.id
    else:
        targetID = args[0]
    try:
        target = client.get_user(int(targetID))
    except ValueError:
        await message.reply(f"*Error:* User with ID {targetID} not found.\n*Usage:* !list <optional User ID>\n*Note:* You must have Discord Developer Settings enabled to find User IDs.")
        return
    if type(target) != discord.User:
        message.reply(f"*Error:* User with ID {targetID} not found.\n*Usage:* !list <optional User ID>\n*Note:* You must have Discord Developer Settings enabled to find User IDs.")
        return
    content = f"**Characters owned by {target.display_name}:**\n\n"
    count = 0
    for element in config["characters"]:
        item = config["characters"][element]
        if str(item['owner']) == str(target.id):
            count += 1
            content += f"**{item['name']}**\n"
            content += f"A Level {item['level']} {item['species']} {item['class']}\n"
            content += f"`{item['uuid']}`\n\n"
    content += f"*{target.display_name} has {count} saved character(s).*"
    try:
        await message.reply(content)
    except HTTPException:
        sends = wrangler.thatstoolong(content)
        for element in sends:
            await message.channel.send(element)

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
        count_str = match.group(1)
        size_str = match.group(2)
        count = int(count_str) if count_str not in ("", "-") else 1
        size = int(size_str)
        if size < 1 or count < 1:
            gif = random.randint(0, len(gifs) - 1)
            await message.channel.send(gifs[gif])
            return
        elif size == 1:
            await message.channel.send("You rolled a 1. What did you expect?")
            return
        elif count > 1:
            await multiDice(size, count, message)
        else:
            await singleDice(size, message)
    else:
        if not message.author.bot or message.author.system:
            if message.content.startswith("!"):
                parts = shlex.split(message.content.strip())
                cmd = parts[0].lstrip("!")
                args = parts[1:]
                if cmd in config["commands"]:
                    action_name = config["commands"][cmd]["command"]
                    func = globals().get(action_name)
                    if callable(func):
                        await func(message, args)
                    else:
                        print(f"No function defined for action '{action_name}'")


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
