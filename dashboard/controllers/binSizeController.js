const express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const GarbageBin = mongoose.model('Bin');

router.get('/', (req, res) => {
    GarbageBin.find((err, docs) => {
        if (!err) {
            res.render("bin/list", {
                list: docs
            });
        }
        else {
            console.log('Error in retrieving bin list :' + err);
        }
    });
});

router.get('/delete/:id', (req, res) => {
    GarbageBin.findByIdAndRemove(req.params.id, (err, doc) => {
        if (!err) {
            res.redirect('/bin/list');
        }
        else { console.log('Error in delete :' + err); }
    });
});

module.exports = router;