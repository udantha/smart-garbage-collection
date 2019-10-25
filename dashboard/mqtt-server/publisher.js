var mqtt = require('mqtt');
var client = mqtt.connect('mqtt://127.0.0.1');
client.on('connect', function () {
    setInterval(function () {
        var rand = (new Date()).getSeconds();
        client.publish('channel_garbage_amount', '1:' + rand +':BIN_NON_METAL');
        console.log('MQTT Message Sent - ' + rand);
    }, 1000);
});