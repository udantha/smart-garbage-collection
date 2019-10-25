const express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const GarbageBin = mongoose.model('Bin');

router.get('/list', (req, res) => {
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

router.get('/json', (req, res) => {
    GarbageBin.find((err, docs) => {
        if (!err) {
            res.json(docs)
        }
        else {
            res.json({error: 'List not available'})
            console.log('Error in retrieving bin list :' + err);
        }
    });
});

router.get('/', (req, res) => {
    res.render("bin/addOrEdit", {
        viewTitle: "Create Bin"
    });
});

router.post('/', (req, res) => {
    if (req.body._id == '')
        insertRecord(req, res);
    else
        updateRecord(req, res);
});

router.get('/:id', (req, res) => {
    GarbageBin.findById(req.params.id, (err, doc) => {
        if (!err) {
            res.render("bin/addOrEdit", {
                viewTitle: "Update bin",
                bin: doc
            });
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

function insertRecord(req, res) {
    var bin = new GarbageBin();
    bin.binId = req.body.binId;
    bin.binHeight = req.body.binHeight;
    bin.binLocation = {
        type: 'Point',
        // Place longitude first, then latitude
        coordinates: req.body.lonlat.explode(',').map(d => d.trim())
    };
    bin.binCreatedOn = new Date();
    bin.lastCollectedOn = req.body.lastCollectedOn;

    bin.save((err, doc) => {
        if (!err)
            res.redirect('bin/list');
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("bin/addOrEdit", {
                    viewTitle: "Insert bin",
                    bin: req.body
                });
            }
            else
                console.log('Error during record insertion : ' + err);
        }
    });
}

function updateRecord(req, res) {
    var bin = {};
    bin.binId = req.body.binId;
    bin.binHeight = req.body.binHeight;
    bin.binLocation = {
        type: 'Point',
        coordinates: req.body.lonlat.split(',').map(d => d.trim())
    };
    bin.lastCollectedOn = req.body.lastCollectedOn;

    GarbageBin.findOneAndUpdate({ _id: req.body._id }, bin, { new: true }, (err, doc) => {
        if (!err) { res.redirect('bin/list'); }
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("bin/addOrEdit", {
                    viewTitle: 'Update bin',
                    bin: req.body
                });
            }
            else
                console.log('Error during record update : ' + err);
        }
    });
}

function handleValidationError(err, body) {
    for (field in err.errors) {
        switch (err.errors[field].path) {
            case 'binId':
                body['idError'] = err.errors[field].message;
                break;
            case 'binHeight':
                body['heightError'] = err.errors[field].message;
                break;
            default:
                break;
        }
    }
}

module.exports = router;