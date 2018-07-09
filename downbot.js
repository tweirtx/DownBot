const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./CONFIG.json');

client.on('ready', () => {
  console.log("Ready!");
});

client.on('message', msg => {
    if (msg.content == 'hello world') {
        msg.reply("Hello world!");
    }
});

client.login(config.discord_token);