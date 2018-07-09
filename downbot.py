"""Provides a Discord bot redundancy system"""

import os
import json
import platform
import asyncio
import subprocess
import wget
import discord
from discord.ext.commands import Bot

CONFIG = {
    'discord_token': "Put Discord API Token here.",
    'id_to_watch': 0,
    'notify_id': [],
    'time_to_wait': 120,
    'directory': 'Put the COMPLETE path of the folder the bot is in here',
    'start_command': 'Put the command to start the bot here'
}
CONFIG_FILE = 'CONFIG.json'

if os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        CONFIG.update(json.load(f))

with open('CONFIG.json', 'w') as f:
    json.dump(CONFIG, f, indent='\t')

print(platform.system())
START_COMMAND = CONFIG['start_command']
try:
    open('./startscript.sh', 'r')
except FileNotFoundError:
    wget.download('https://raw.githubusercontent.com/tweirtx/DownBot/scripts/startscript.sh')


bot = discord.ext.commands.Bot(command_prefix='#!')
loop = asyncio.AbstractEventLoop()
BOT = Bot(command_prefix='#!')


class StartBot():
    """Keeps track of certain variables"""
    cancelled = False
    handle = None
    in_alarm = False


async def start_up():
    """Starts the backup process"""
    await asyncio.sleep(CONFIG['time_to_wait'])
    if not StartBot.cancelled:
        StartBot.handle = subprocess.Popen(START_COMMAND, shell=True, cwd=CONFIG['directory'])
    if StartBot.cancelled:
        StartBot.cancelled = False


@BOT.event
async def on_member_update(before, after):
    """If the bot goes offline, trigger everything that should happen"""
    if before.id == CONFIG['id_to_watch']:
        if after.status == discord.Status('offline'):
            for i in CONFIG['notify_id']:
                person = before.guild.get_member(i)
                await person.send("NOTICE: {} has gone offline. Starting backup process in {} seconds. "
                                  "Resolve outage or send #!cancel to cancel.".format(before.display_name,
                                                                                      CONFIG['time_to_wait']))
            StartBot.cancelled = False
            await start_up()
        elif after.status == discord.Status('online') and before.status == discord.Status('offline'):
            StartBot.cancelled = True
        elif before.status == discord.Status.dnd and after.status == discord.Status.online:
            print("Primary back online registered")
            StartBot.cancelled = True
        else:
            print("after.status is {} type {} and before.status is {}".format(after.status, type(after.status),
                                                                              before.status))


@BOT.command()
async def cancel(ctx):
    """Manually cancel a startup"""
    if StartBot.in_alarm:
        StartBot.cancelled = True
        StartBot.in_alarm = False
        await ctx.send("start up cancelled")
    else:
        await ctx.send("No start up to cancel!")


@BOT.command()
async def shutdown(ctx):
    """Manually shut down the process"""
    StartBot.in_alarm = False
    StartBot.cancelled = False
    StartBot.handle.kill()
    await ctx.send("Shutdown successful")


@BOT.command()
async def gethandle(ctx):
    """Sends the handle of the process (debug only)"""
    await ctx.send(StartBot.handle)


@BOT.event
async def on_ready():
    """Announce that the bot is ready once it is"""
    print("Ready")

BOT.run(CONFIG['discord_token'])
