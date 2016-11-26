module.exports = {
    getKanjiSVG: getKanjiSVG
}

var Promise = require('bluebird');

var Kanji = require('../models/kanji');

function getKanjiSVG(kanjiArray){
    return new Promise((resolve, reject) => {
        if (kanjiArray.constructor != Array) {
            reject("Not an array");
        }
        Kanji.find({'character': { $in: kanjiArray }}).then((k) => {
            resolve(k);
        }).catch((e) => {
            reject(e);
        });
    });
}
