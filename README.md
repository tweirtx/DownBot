# DownBot

This is a Discord bot that will monitor your bot to check if it goes offline. If the bot does go offline, any people you have in the list
will be notified via a direct message, and if the bot does not come back online within a configurable time allotment or you do not
manually cancel, this bot will run a system command to start your bot process. I haven't figured out the mechanism for how the primary
host will notify that it is back online, however once the main host comes back online the backup host will shut its copy down.

# Integration Guide

If you would like to integrate this with your bot, here's the best guide I can write. If you run into trouble or have questions, please contact the email listed on my GitHub profile.

In order to take chance of the fully automatic features, there is a tiny change to make to your code. I would recommend using a configuration file for this.

This is the best way I can figure out, let me know if you have a better one!

1. Add a key to your configuration file to dictate whether that installed instance is a backup instance or the primary. I recommend using a boolean.

2. Add code to your bot to set the presence to dnd (do not disturb) if it is the backup host. This will not only signal to developers that something is wrong, but it is a status change that is overriden automatically when the primary instance comes back online. That change signals DownBot to terminate its backup process.

# DownBot setup (Linux)

This is a step-by-step guide to setting up DownBot on a Linux backup host. This guide may also work for macOS, but macOS is not officially tested or supported.

1. **Download the files** Do this by navigating to your chosen directory and running ``git clone https://github.com/tweirtx/DownBot``
2. **Install Python 3.6** If your bot is a Python bot, chances are you're already good to go. If your bot is not Python, you might need to install 3.6. Run ``python3 -V`` within the DownBot folder. If your installed version is higher than 3.6.0, you are all set. Otherwise, refer to the **Installing Python3.6** section down below. Once you've gotten it installed, make sure discord.py is installed by running the following command: ``pip3 install -e git+https://github.com/Rapptz/discord.py.git@rewrite``
3. **Run the bot process** You will need to run the bot process to generate the config file to modify in the next step. Use ``python3 downbot.py as the command to do so.``
4. **Set your config variables**. Open config.json in your favorite editor (I prefer nano, but use whatever you prefer!) and set the keys accordingly. For the discord_token variable, create a bot user and paste the user token into the discord_token JSON key. This ***must*** be separate from the bot you are setting up redundancy on. For id_to_watch, paste in the user ID of the bot you want to monitor. notify_id should be a list of the user IDs you want DownBot to DM on a bot outage event. time_to_wait is a configurable integer that specifies the time (in seconds) DownBot should give you to resolve the outage or cancel the auto-start. The default is 2 minutes, but feel free to change this.
5. **Set your start commands** Almost done! All that's left to do is tell DownBot how it should start your bot when it's necessary. Open start.sh with your favorite text editor. Inside you should see a template that you just have to fill in with your appropriate commands. Change bot_directory to the directory your backup bot process is in. Change the second line to whatever the correct start command for your bot is, Python or otherwise.
6. **Make the start script usable** In order to make your start script usable, you will need to mark it as executable. Simply run ``sudo chmod +x startscript.sh``to make it usable.
7. **All done!** You should be ready to go from here. Go ahead and run ``python3 downbot.py`` and see if it works. If you see "Ready" then that means everything is installed correctly. Test your config by setting your bot to offline while DownBot is running.

# DownBot setup (Windows)

This is a step-by-step guide to setting up DownBot on a Windows host.

1. **Download the files** The easiest method is to download a ZIP file of this repository and extract it on your system.
2. **Install Python 3.6** If your bot is a Python bot, chances are you're already good to go. If your bot is not Python, you might need to install 3.6. Run ``py -V`` within the DownBot folder. If your installed version is higher than 3.6.0, you are all set. Otherwise, download and install the latest version from https://python.org. Once you've gotten it installed, make sure discord.py is installed by running the following command: ``pip3 install -e git+https://github.com/Rapptz/discord.py.git@rewrite``
3. **Run the bot process** You will need to run the bot process to generate the config file to modify in the next step. Do this with ``py DownBot.py``
4. **Set your config variables**. Open config.json in your favorite editor and set the keys accordingly. For the discord_token variable, create a bot user and paste the user token into the discord_token JSON key. This ***must*** be separate from the bot you are setting up redundancy on. For id_to_watch, paste in the user ID of the bot you want to monitor. notify_id should be a list of the user IDs you want DownBot to DM on a bot outage event. time_to_wait is a configurable integer that specifies the time (in seconds) DownBot should give you to resolve the outage or cancel the auto-start. The default is 2 minutes, but feel free to change this.
5. **Set your start commands** Almost done! All that's left to do is tell DownBot how it should start your bot when it's necessary. Open start.bat with your favorite text editor. Inside you should see a template that you just have to fill in with your appropriate commands. Change bot_directory to the directory your backup bot process is in. Change the second line to whatever the correct start command for your bot is, Python or otherwise.
6. **All done!** You should be ready to go from here. Go ahead and run ``py downbot.py`` and see if it works. If you see "Ready" then that means everything is installed correctly. Test your config by setting your bot to offline while DownBot is running.

# Installing Python3.6

1. Install any system packages required by running the correct command for your OS version from the list here: https://github.com/pyenv/pyenv/wiki
2. Run the following command: curl -L https://gist.githubusercontent.com/tweirtx/e891ad89d600559d1b014fa8b625fc97/raw/02c97575e616a58b29094c3cc3fd6f4d469a8943/py3.6-linux | bash
3. Restart your interpreter by logging out and back in or rebooting. If you are in a graphical environment, closing and reopening Terminal will work as well.
4. cd to your DownBot directory and run the following commands:
pyenv install 3.6.4
pyenv local 3.6.4
5. Run python3 -V and you should see Python 3.6.4 as the installed Python version in that folder.
