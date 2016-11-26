var Promise = require('bluebird');
const jsdom = require('jsdom');
const xmlserializer = require('xmlserializer');

var Promise = require('bluebird');
var fs = Promise.promisifyAll(require('fs'));

var client = require('./redis');

module.exports = {
    generateStrokeDiagram: generateStrokeDiagram,
    getStrokeOrderSVG: getStrokeOrderSVG
}

function getStrokeOrderSVG(kanji){
    var hex = kanji.charCodeAt(0).toString(16);
    while (hex.length < 5) {
        hex = "0" + hex;
    }
    var key = 'kanji_'+hex;
    return client.getAsync(key).then((kanjiSVG) => {
        if(kanjiSVG){
            console.log("Found cached SVG for", kanji);
            return new Promise((resolve, reject) => {
                resolve(JSON.parse(kanjiSVG));
            });
        } else {
            return fs.readFileAsync( __dirname + '/../kanji_fixed/'+ hex + '.svg').then((data) => {
                return generateStrokeDiagram(kanji, data.toString());
            }).then((strokes) => {
                console.log("Caching SVG for", kanji);
                client.set(key, JSON.stringify(kanjiStroke));
                return new Promise((resolve, reject) => {
                    resolve(strokes);
                });
            });
        }
    });
}

function generateStrokeDiagram(kanjiCharacter, svgString){
    return new Promise(function(resolve, reject){
        jsdom.env('', ['node_modules/snapsvg/dist/snap.svg.js'], (error, window) => {
            if (error) reject(error);

            // Create the boxes
            function createKanjiBox(){
                var size = 109;
                var kb = window.Snap(size, size);

                var outerAttr = {
                    stroke: "#000",
                    strokeWidth: 2
                };

                var innerAttr = {
                    stroke: "#ccc",
                    strokeWidth: 1,
                    "stroke-dasharray":'5,3'
                };

                // dash
                kb.line(size/2, 0, size/2, size).attr(innerAttr);
                kb.line(0, size/2, size, size/2).attr(innerAttr);

                //box
                kb.line(0, 0, size, 0).attr(outerAttr);
                kb.line(size, 0, size, size).attr(outerAttr);
                kb.line(size, size, 0, size).attr(outerAttr);
                kb.line(0, size, 0, 0).attr(outerAttr);

                return kb;
            }

            // How the kanji looks
            var kanjiAttr = {
                'fill':'none',
                'stroke':'#000000',
                'stroke-width':3,
                'stroke-linecap':'round',
                'stroke-linejoin':'round'
            };

            // Load and create the kanji
            var kanji = window.Snap.parse(svgString);
            var paths = kanji.selectAll('path').attr(kanjiAttr);
            var boxes = [];

            // Add the inital kanji
            boxes.push(xmlserializer.serializeToString(createKanjiBox().append(paths).node));

            // Add the stroke orders
            for (var i = 0; i < paths.length; i++){
                var box = createKanjiBox();
                for (var j = 0; j <= i; j++){
                    var cp = paths[j].clone();
                    box.append(cp);
                    if (j == i){
                        var startPt = window.Snap.path.getPointAtLength(cp, 0);
                        box.circle(startPt.x, startPt.y, 5).attr({
                            'fill': '#f00'
                        });
                    } else {
                        cp.attr({
                            'stroke': '#aaa'
                        });
                    }
                }
                box.text(5,15,i+1).attr({
                    'font-size': '10px'
                });
                boxes.push(xmlserializer.serializeToString(box.node));
            }
            // Send the SVG
            window.close();
            resolve({'character': kanjiCharacter, 'svg': boxes});
        });
    });
}
