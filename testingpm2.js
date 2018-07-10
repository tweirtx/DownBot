const pm2 = require('pm2');

function stop() {
    pm2.stop("downbot-backup-process");
    console.log("Stopped");
}

pm2.start(jsonConfigFile = 'pm2config.json');
setTimeout(stop, 10000);
