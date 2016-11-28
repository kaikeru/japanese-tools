module.exports = {
    getKanjiSVG: getKanjiSVG,
    getEmptyDiagramBox: getEmptyDiagramBox
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

function getEmptyDiagramBox(count){
    var boxSVG = '<svg height="109" version="1.1" width="109" xmlns="http://www.w3.org/2000/svg"><desc>Created with Snap</desc><defs></defs><line x1="54.5" x2="54.5" y1="0" y2="109" style="stroke-width: 1; stroke-dasharray: 5,3;" stroke="#cccccc"></line><line x1="0" x2="109" y1="54.5" y2="54.5" style="stroke-width: 1; stroke-dasharray: 5,3;" stroke="#cccccc"></line><line x1="0" x2="109" y1="0" y2="0" style="stroke-width: 2;" stroke="#000000"></line><line x1="109" x2="109" y1="0" y2="109" style="stroke-width: 2;" stroke="#000000"></line><line x1="109" x2="0" y1="109" y2="109" style="stroke-width: 2;" stroke="#000000"></line><line x1="0" x2="0" y1="109" y2="0" style="stroke-width: 2;" stroke="#000000"></line></svg>';
    var boxes = [];
    for(var i = 0; i < count; i++){
        boxes.push(boxSVG);
    }

    return boxes;
}
