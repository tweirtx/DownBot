# DownBot

This is a Discord bot that will monitor your bot to check if it goes offline. If the bot does go offline, any people you have in the list
will be notified via a direct message, and if the bot does not come back online within a configurable time allotment or you do not
manually cancel, this bot will run a system command to start your bot process. I haven't figured out the mechanism for how the primary
host will notify that it is back online, however once the main host comes back online the backup host will shut its copy down.
