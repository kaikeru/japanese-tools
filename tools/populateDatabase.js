var Kanji = require('../models/kanji');
var svgCreator = require('../lib/svgCreator');
var Promise = require('bluebird');
var fs = Promise.promisifyAll(require('fs'));

function main(){
    var dirName = __dirname + '/../kanji_fixed';
    console.log(dirName);
    var files = fs.readdirSync(dirName);
    var promises = [];
    var kanjiToUnicode = {}
    Promise.map(files, (file) => {
        if (file.indexOf('-') > -1) {
            //console.log("Skipping file:", file);
            return Promise.resolve(null);
        }
        var data = fs.readFileSync(dirName + '/' + file);
        var fileHex = file.slice(0, -4);
        var kanjiCharacter = String.fromCharCode(parseInt(fileHex, 16));
        kanjiToUnicode[kanjiCharacter] = fileHex;
        console.log('Processing SVG:', fileHex, kanjiCharacter);
        return svgCreator.generateStrokeDiagram(kanjiCharacter, data.toString());
    }, {'concurrency': 10}).then((strokeOrders) => {
        for(var i = 0; i < strokeOrders.length; i++) {
            var strokeOrder = strokeOrders[i];
            if (strokeOrder == null) {
                continue;
            }
            var character = strokeOrder['character'];
            console.log(character, kanjiToUnicode[character]);
            try {
                var k = new Kanji({
                    'character': character,
                    'unicode': kanjiToUnicode[character],
                    'svg': strokeOrder['svg']
                });
                k.save();
                console.log("Saved kanji:", k.character, k.unicode);
            } catch (e){
                console.err("Couldn't save:", k.character, k.unicode);
            }
        }

    });
}

// Run the main
main();
