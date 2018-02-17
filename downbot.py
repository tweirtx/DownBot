#Downbot

import discord, os, json, platform, asyncio, subprocess, wget
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
    try:
        open('startscript.bat', 'r')
    except:
        wget.download('https://raw.githubusercontent.com/tweirtx/DownBot/scripts/startscript.bat')
else:
    print(platform.system())
    startscript = "./startscript.sh"
    try:
        open('startscript.sh', 'r')
    except:
        wget.download('https://raw.githubusercontent.com/tweirtx/DownBot/scripts/startscript.sh')

bot = discord.ext.commands.Bot(command_prefix='#!')
loop = asyncio.AbstractEventLoop()


class startBot():
    cancelled = False
    handle = None


async def startUp():
    await asyncio.sleep(config['time_to_wait'])
    if not startBot.cancelled:
        subprocess.call(startscript)
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
            startBot.handle = startUp()
            await startBot.handle
        elif after.status == discord.Status('online') and before.status == discord.Status('offline'):
            startBot.cancelled = True
        elif before.status == discord.Status.dnd and after.status == discord.Status.online:
            print("Primary back online registered")
            await startBot.handle.cancel()
        else:
            print("after.status is {} type {} and before.status is {}".format(after.status, type(after.status), before.status))


@bot.command()
async def cancel(ctx):
    startBot.cancelled = True
    await ctx.send("Startup cancelled")


@bot.command()
async def shutdown(ctx):
    startBot.cancelled = False
    await startBot.handle.cancel()
    await ctx.send("Shutdown successful")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.event
async def on_ready():
    print("Ready")

bot.run(config['discord_token'])
