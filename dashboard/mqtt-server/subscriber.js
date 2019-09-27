var mqtt = require('mqtt')
const mongoose = require('mongoose');
require('./models/db');

const GarbageBin = mongoose.model('Bin');

var IP_ADDRESS = '192.168.1.1';
var CHANNEL = 'channel_garbage_amount';

var client = mqtt.connect('mqtt://' + IP_ADDRESS)
client.on('connect', function () {
    client.subscribe(CHANNEL)
})

client.on('message', function (topic, message) {
    if (topic == CHANNEL){
        var data = message.toString();
        var payload = data.split(':')
        var binId = payload[0];
        var height = payload[1];

        //save data
        updateRecord(binId, {
            binId: binId,
            binHeight: height
        })
    }
})


function updateRecord(id, data) {
    GarbageBin.findOneAndUpdate({ _id: req.body._id }, req.body, { new: true }, (err, doc) => {
        if (!err) { console.log('saved data'); }
        else {
            console.log('Error during record update : ' + err);
        }
    });
}