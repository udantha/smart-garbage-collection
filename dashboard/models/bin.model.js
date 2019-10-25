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
    currentMetalBinHeight: {
        type: Number
    },
    binMetalHeightUpatedOn: {
        type: Date
    },
    currentAllBinHeight: {
        type: Number
    },
    binAllHeightUpatedOn: {
        type: Date
    },
    binLocation: {
        type: { type: String, enum: ['Point'], default: 'Point' },
        coordinates: { type: [Number], default: [0, 0], index: '2dsphere' }
    },
    binCreatedOn: {
        type: Date
    },
    lastCollectedOn: {
        type: Date
    },
});

mongoose.model('Bin', binSchema);