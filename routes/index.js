var express = require('express');
var router = express.Router();
var multer = require("multer");
var upload = multer({dest: "uploads/"});

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {title: 'Super Meme Generator'});
});

/* GET features page. */
router.get('/features', function (req, res, next) {

    res.render('features');
});

/* Get Pricing page*/
router.get('/pricing', function (req, res, next) {
    res.render('pricing');
})
module.exports = router;

/* About page */
router.get('/about', function (req, res, next) {
    res.render('about');
});

/* Docs page */
router.get('/docs', function (req, res, next) {
    res.render('docs');
});

/* Questions page */
router.get('/questions', function (req, res, next) {
    res.render('questions');
});

/* Meme Maker endpoint */
router.post('/meme-maker', upload.single("memeFile"), function (req, res, next) {

    if (req.body && req.file) {

        let options = {};
        options.topText = req.body.topText;
        options.bottomText = req.body.bottomText;
        options.image = req.file.path;
        options.outfile = 'uploads/testing';

        var canvas = document.getElementById('canvas');
        options.canvas = canvas;

        memeGen(options, function (err) {
            if (err) {
                console.log(err);
                throw new Error(err);
            }
            console.log('Image saved: ' + options.outfile)
        });

        res.send('Image saved: ' + options.outfile)

    } else {
        console.log('no body found');
        res.status(500);
    }
});

