#Downbot

import discord, os, json, platform, asyncio

config = {
	'discord_token': "Put Discord API Token here.",
    'id_to_watch': "Put the ID you want DownBot to watch here",
    'notify_id': [],
    'time_to_wait': 120
}
config_file = 'config.json'

if os.path.isfile(config_file):
	with open(config_file) as f:
		config.update(json.load(f))

with open('config.json', 'w') as f:
	json.dump(config, f, indent='\t')

if platform.platform() == "Windows":
    startscript = "startscript.bat"
else:
    print(platform.platform())
    startscript = "startscript.sh"

bot = discord.Client()
loop = asyncio.AbstractEventLoop()

async def startUp():
    os.system(startscript)

@bot.event()
async def on_member_update(self, member):
    configmemberid = member.guild.get_member(config[id_to_watch])
    if member.id == configmemberid.id:
        task = await loop.call_later(config['time_to_wait'], startUp)
        loop.create_task(shutdown(task))
        print("Debug: alarm raised")
    else:
        print("Debug: event detected but no alarm raised")

@bot.command()
async def shutdown(task):
    print("Debugging: task shut down")
    await task.cancel()


bot.run(config['discord_token'])