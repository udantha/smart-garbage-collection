const express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const GarbageBin = mongoose.model('Bin');

router.get('/', (req, res) => {
    res.render("dashboard/map");
});

module.exports = router;