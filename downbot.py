#Downbot

import discord, os, json, platform

config = {
	'discord_token': "Put Discord API Token here.",
    'id_to_watch': "Put the ID you want DownBot to watch here",
    'notify_id': []
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

@bot.event()
async def on_member_update(self, member):
    configmemberid = member.guild.get_member(config[id_to_watch])
    if member.id == configmemberid.id:
        print("Debug: alarm raised")
    else:
        print("Debug: event detected but no alarm raised")