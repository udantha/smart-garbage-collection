var mqtt = require('mqtt')
const mongoose = require('mongoose');
require('../models/db');

const GarbageBin = mongoose.model('Bin');

var IP_ADDRESS = '127.0.0.1';
var CHANNEL = 'channel_garbage_amount';

var client = mqtt.connect('mqtt://' + IP_ADDRESS)
client.on('connect', function () {
    console.log('MQTT subscriber connected');
    client.subscribe(CHANNEL)
})

client.on('message', function (topic, message) {
    if (topic == CHANNEL){
        var data = message.toString();
        var payload = data.split(':')
        var binId = payload[0];
        var height = payload[1];
        var binType = payload[2];
        var record = {};

        if (binType =='BIN_METAL'){
            record = {
                currentMetalBinHeight: height,
                binMetalHeightUpatedOn: new Date()
            }
        }else{
            record = {
                currentAllBinHeight: height,
                binAllHeightUpatedOn: new Date()
            }
        }
        //save data
        updateRecord(binId, record)
    }
})


function updateRecord(id, data) {
    GarbageBin.findOneAndUpdate({ binId: id }, data, { new: true }, (err, doc) => {
        if (!err) { console.log('saved data'); }
        else {
            console.log('Error during record update : ' + err);
        }
    }).then(data => {
        console.log(data)
    });
}