const mongoose = require('mongoose');

var binSchema = new mongoose.Schema({
    binId: {
        type: String,
        required: 'This field is required.',
        index: true,
        unique: true
    },
    binHeight: {
        type: Number,
        required: 'This field is required.'
    },
    currentBinHeight: {
        type: Number
    },
    binHeightUpatedOn: {
        type: Date
    },
    binLocation: {
        type: { type: String, default: 'Point' },
        coordinates: { type: [Number], default: [0, 0], index: '2dsphere' }
    },
    binCreatedOn: {
        type: Date
    },
});

mongoose.model('Bin', binSchema);