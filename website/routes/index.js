var express = require('express');
var router = express.Router();
var kh = require('../lib/kanjiHandler');
var Promise = require('bluebird');
var http = require('https');

/**
* GET: Render the index page
*/
router.get('/', function(req, res, next) {
    res.render('index', {
        title: 'Kanji Stroke Order'
    });
});

/*
 * GET /kanji
 * Returns the kanji as a json object
 */
router.get('/kanji', function(req, res, next){
    if(req.accepts('html')){
        next();
    }
    if(req.accepts('json')) {
        if (req.query.k) {
            var kanjiArray = req.query.k.split("");
            kh.getKanjiSVG(kanjiArray).then((k) => {
                res.json(k);
            });
        } else {
            next();
        }
    }
});

/*
 * GET /kanji/:kanji
 */
router.get('/kanji/:kanji', function(req, res, next){
    var kanji = req.params.kanji;
    var retKanji = null;
    kh.getKanjiSVG([kanji]).then((k) => {
        retKanji = k[0];
    }).finally(() => {
        if (retKanji == null) {
            next();
        } else {
            res.render('kanji', {
                'title': retKanji.character,
                'svg': retKanji.svg
            });
        }
    });
});

router.get('/worksheet/:kanji', function(req, res, next){
    var kanji = req.params.kanji;
    var retKanji = null;
    kh.getKanjiSVG([kanji]).then((k) => {
        retKanji = k[0];
    }).finally(() => {
        if (retKanji == null) {
            next();
        } else {
            //Get the kanji filler size
            var totalBoxes = 80;
            var boxes = retKanji.svg.concat(kh.getEmptyDiagramBox(totalBoxes - retKanji.svg.length));
            var onyomi = null;
            if (retKanji.readings.onyomi){
                onyomi = retKanji.readings.onyomi.join(', ');
            }
            var kunyomi = null;
            if (retKanji.readings.kunyomi){
                kunyomi = retKanji.readings.kunyomi.join(', ');
            }
            var meanings = null;
            if (retKanji.meanings){
                meanings = retKanji.meanings.join(', ');
            }
            res.render('kanji-worksheet', {
                'title': retKanji.character + " Writing Worksheet",
                'character': retKanji.character,
                'onyomi': onyomi,
                'kunyomi': kunyomi,
                'meanings': meanings,
                'svg': boxes
            });
        }
    });
});

router.get('/wanikani', function(req, res, next){
    var apiKey = req.query.key;

    if(!apiKey){
        res.json({error: "Need key"});
    }
    var url = 'https://www.wanikani.com/api/user/' + apiKey + '/kanji/';
    http.get(url, (response) => {
        var body = '';
        response.on('data', (d) => {
            body += d;
        });
        response.on('end', () => {
            var wk = JSON.parse(body)['requested_information'];

            var kanjiList = [];
            for(var i = 0; i < wk.length; i++){
                kanjiList.push(wk[i].character);
            }
            kh.getKanjiSVG(kanjiList).then((k) => {
                res.json(k);
            });
        });
    }).on('error', (err) => {
        res.json({
            success: false,
            error: "Problem connecting to WaniKani API",
            key: apiKey
        });
    });
});

module.exports = router;
