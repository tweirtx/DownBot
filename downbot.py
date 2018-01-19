#Downbot

import discord, os, json, platform, asyncio
from discord.ext.commands import Bot

config = {
	'discord_token': "Put Discord API Token here.",
    'id_to_watch': 0,
    'notify_id': [],
    'time_to_wait': 120
}
config_file = 'config.json'

if os.path.isfile(config_file):
	with open(config_file) as f:
		config.update(json.load(f))

with open('config.json', 'w') as f:
	json.dump(config, f, indent='\t')

if platform.system() == "Windows":
    startscript = "startscript.bat"
else:
    print(platform.system())
    startscript = "./startscript.sh"

bot = discord.ext.commands.Bot(command_prefix='#!')
loop = asyncio.AbstractEventLoop()

async def startUp():
    os.system(startscript)

@bot.event
async def on_member_update(before, after):
    if before.id == config['id_to_watch']:
        task = loop.call_later(config['time_to_wait'], startUp)
        await loop.create_task(shutdown(task))
        print("Debug: alarm raised")
    else:
        print("Debug: event detected but no alarm raised")

@bot.command()
async def shutdown(task):
    print("Debugging: task shut down")
    await task.cancel()

@bot.event
async def on_ready():
    print("Ready")

bot.run(config['discord_token'])