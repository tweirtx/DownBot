const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./CONFIG.json');
const pm2 = require('pm2');

var in_alarm = false;
var running;

function start() {
    if (in_alarm) {
        var process = pm2.start({
            script: config.start_command,
            pm_cwd: config.directory
        })
    }
}


client.on('ready', () => {
    console.log("Ready!");
});

client.on('message', msg => {
    if(msg.content == "#!cancel") {
        if (in_alarm) {
            msg.reply("cancelled");
            in_alarm = false;
        }
        else {
            msg.reply("no startup to cancel!")
        }
    }
    if(msg.content == "#!shutdown") {
        if (running) {
            msg.reply("sucessfully shut down");
            running = false;
        }
        else {
            msg.reply("cannot shut down something that is not running!!")
        }
    }
});

client.on('presenceUpdate', () => {
    if (oldMember.id == config.id_to_watch) {
        if(oldMember.stuff) {
            console.log("Alarm detected");
            for (memb in config.notify_id) {
                var memberToSend = client.fetchUser(memb);
                memberToSend.send("The bot this bot is responsible for monitoring has gone down. Starting automatically if #!cancel is not sent.")
            }
            setTimeout(start, config.time_to_wait);
        }
    }
});

client.login(config.discord_token);