const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./CONFIG.json');
const pm2 = require('pm2');

var in_alarm = false;
var running;

function start() {
    if (in_alarm) {
        pm2.start({
            name: "downbot-backup-process",
            script: config.start_command,
            cwd: config.directory
        });
        running = true;
    }
}

async function alertAlertedPeople(whoToSend, whatToSend) {
    var memberToSend = await client.fetchUser(whoToSend);
    await memberToSend.send(whatToSend).catch(console.error)
}


client.on('ready', () => {
    console.log("Ready!");
});

client.on('message', msg => {
    if(msg.content == "#!cancel") {
        if (in_alarm) {
            if (!running) {
                msg.reply("cancelled");
                in_alarm = false;
            }
        }
        else {
            msg.reply("no startup to cancel!")
        }
    }
    if(msg.content == "#!shutdown") {
        if (running) {
            pm2.stop("downbot-backup-process");
            in_alarm = false;
            running = false;
            msg.reply("sucessfully shut down");
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
                in_alarm = true;
                console.log("Alarm detected");
                var memb;
                for (memb in config.notify_id) {
                    var membid = config.notify_id[memb];
                    var prometo = alertAlertedPeople(membid, "The bot this bot is responsible for monitoring has gone down. Starting automatically if #!cancel is not sent.")
                }
                setTimeout(start, config.time_to_wait * 1000);
            }
        }
        if (oldMember.presence.status == "dnd") {
            if (newMember.presence.status == "online") {
                console.log('stop detected');
                pm2.stop("downbot-backup-process");
                running = false;
                in_alarm = false;
            }
        }
    }
});

client.login(config.discord_token);