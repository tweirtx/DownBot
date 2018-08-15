# DownBot

This is a Discord bot that will monitor your bot to check if it goes offline. If the bot does go offline, any people you have in the list
will be notified via a direct message, and if the bot does not come back online within a configurable time allotment or you do not
manually cancel, this bot will run a system command to start your bot process.

# Integration Guide

If you would like to integrate this with your bot, here's the best guide I can write. If you run into trouble or have questions, please contact the email listed on my GitHub profile.

In order to take chance of the fully automatic features, there is a tiny change to make to your code. I would recommend using a configuration file for this.

This is the best way I can figure out, let me know if you have a better one!

1. Add a key to your configuration file to dictate whether that installed instance is a backup instance or the primary. I recommend using a boolean.

2. Add code to your bot to set the presence to dnd (do not disturb) if it is the backup host. This will not only signal to developers that something is wrong, but it is a status change that is overriden automatically when the primary instance comes back online. That change signals DownBot to terminate its backup process.

# DownBot setup

This is a step-by-step guide to setting up DownBot on a backup host. This process works on Linux, but at this time macOS and Windows are not natively supported. See below if you are using macOS or Windows

**1. Download the files.** To get started, run ```git clone https://github.com/tweirtx/DownBot``` to download the files. Alternatively, download a ZIP file from this page.

**2. Install node.js.** Refer to https://nodejs.org for instructions to install node.js for your OS.

**3. Install dependencies.** Run ```npm install``` in the directory where the DownBot files are.

**4. Configure the bot.** Open the sample_config.json file in your favorite text editor (mine's nano) and fill out each space. Once you're done filling it out, rename the file to CONFIG.json.

**5. Run the bot.** Congratulations, it should be done! Go ahead and run ```node downbot.js``` in the DownBot folder. If you see the word ready appear, then you have successfully started the bot!

**Troubleshooting** If the bot is misbehaving, contact tweirtx#9400 for assistance.

Credits:

tweirtx - Writing the bot, testing on Linux

endreman0 - Windows testing

elevenchars - macOS testing
