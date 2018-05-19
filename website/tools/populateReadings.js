var Promise = require('bluebird');
var fs = Promise.promisifyAll(require('fs'));
var Kanji = require('../models/kanji');

var savedKanji = 0;
fs.readFileAsync(process.argv[2]).then((data) =>{
    var wkData = JSON.parse(data);
    var kanjis = wkData['requested_information'];
    Promise.map(kanjis, (kanji) => {
        return Kanji.findOne({character: kanji.character}).then((k) => {
            if(kanji.onyomi){
                k.readings.onyomi = kanji.onyomi.split(',');
            }
            if(kanji.kunyomi){
                k.readings.kunyomi = kanji.kunyomi.split(',');
            }
            if(kanji.nanori){
                k.readings.nanori = kanji.nanori.split(',');
            }
            if(kanji.meaning){
                k.meanings = kanji.meaning.split(',');
            }
            if(kanji.level){
                k.wanikani.level = kanji.level;
            }
            if(kanji.important_reading){
                k.wanikani.important_reading = kanji.important_reading;
            }
            console.log(++savedKanji, "Saving data for", k.character);

            return k.save();
        });
    });
}).error((err) => {
    console.log(err);
});
