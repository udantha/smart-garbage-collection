const mongoose = require('mongoose');

var binSchema = new mongoose.Schema({
    binId: {
        type: String,
        required: 'This field is required.'
    },
    binHeight: {
        type: String
    }
});

mongoose.model('Bin', binSchema);