#Downbot

import discord, os, json, platform, asyncio, subprocess, wget, psutil
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
    windows = True
    try:
        open('startscript.bat', 'r')
    except:
        wget.download('https://raw.githubusercontent.com/tweirtx/DownBot/scripts/startscript.bat')
else:
    print(platform.system())
    windows = False
    startCommand = './startscript.sh'
    try:
        open('./startscript.sh', 'r')
    except:
        wget.download('https://raw.githubusercontent.com/tweirtx/DownBot/scripts/startscript.sh')

bot = discord.ext.commands.Bot(command_prefix='#!')
loop = asyncio.AbstractEventLoop()


class startBot():
    cancelled = False
    handle = None
    in_alarm = False


async def startUp():
    await asyncio.sleep(config['time_to_wait'])
    if not startBot.cancelled:
        startBot.handle = subprocess.Popen(startCommand, shell=True)
    if startBot.cancelled:
        startBot.cancelled = False


@bot.event
async def on_member_update(before, after):
    if before.id == config['id_to_watch']:
        if after.status == discord.Status('offline'):
            for i in config['notify_id']:
                person = before.guild.get_member(i)
                await person.send("NOTICE: {} has gone offline. Starting backup process in {} seconds. "
                                  "Resolve outage or send #!cancel to cancel.".format(before.display_name, config['time_to_wait']))
            startBot.cancelled = False
            await startUp()
        elif after.status == discord.Status('online') and before.status == discord.Status('offline'):
            startBot.cancelled = True
        elif before.status == discord.Status.dnd and after.status == discord.Status.online:
            print("Primary back online registered")
            startBot.cancelled = True
        else:
            print("after.status is {} type {} and before.status is {}".format(after.status, type(after.status), before.status))


@bot.command()
async def cancel(ctx):
    if startBot.in_alarm:
        startBot.cancelled = True
        startBot.in_alarm = False
        await ctx.send("Startup cancelled")
    else:
        await ctx.send("No startup to cancel!")


@bot.command()
async def shutdown(ctx):
    startBot.in_alarm = False
    startBot.cancelled = False
    startBot.handle.kill()
    await ctx.send("Shutdown successful")


@bot.event
async def on_ready():
    print("Ready")

bot.run(config['discord_token'])
