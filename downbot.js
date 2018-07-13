const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./CONFIG.json');
const pm2 = require('pm2');

var in_alarm = false;
var running;

function start() {
    if (in_alarm) {
        pm2.start({
            script: config.start_command,
            pm_cwd: config.directory
        })
    }
}

async function alertAlertedPeople(whoToSend, whatToSend) {
    console.log(whoToSend);
    var memberToSend = await client.fetchUser(whoToSend);
    console.log(memberToSend);
    if (!whoToSend.dmChannel) {
        await whoToSend.createDM;
        console.log("DM created");
    }
    await whoToSend.dmChannel.send(whatToSend).catch(console.error)
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
            msg.reply("cannot shut down something that is not running!!");
        }
    }
    if(msg.content == "#!ping") {
        msg.reply("Pong!");
    }
});

client.on('presenceUpdate', (oldMember, newMember) => {
    if (oldMember.id == config.id_to_watch) {
        if(oldMember.presence.status == "online") {
            if (newMember.presence.status == "offline") {
                console.log("Alarm detected");
                var memb;
                for (memb in config.notify_id) {
                    var membid = config.notify_id[memb];
                    var prometo = alertAlertedPeople(membid, "The bot this bot is responsible for monitoring has gone down. Starting automatically if #!cancel is not sent.")
                }
                setTimeout(start, config.time_to_wait * 1000);
            }
        }
    }
    else {
        console.log("Not it");
    }
});

client.login(config.discord_token);