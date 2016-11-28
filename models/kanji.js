var mongoose = require('../lib/db');
var Schema = mongoose.Schema;

var kanjiSchema = new Schema({
    character: {
        type: String,
        required: true,
        unique: true
    },
    readings: {
        onyomi: {
            type: [String]
        },
        kunyomi: {
            type: [String]
        },
        nanori: {
            type: [String]
        }
    },
    meanings: {
        type: [String]
    },
    wanikani: {
        level: Number,
        important_reading: String
    },
    unicode: {
        type: String,
        unique: true
    },
    svg: {
        type: [String]
    },
    radicalNumber: {
        type: Number
    },
    jouyouGrade: {
        type: Number
    },
    strokeCount: {
        type: [Number]
    },
    frequencyOfUse: {
        type: Number
    },
    oldJlptLevel: {
        type: Number
    },
    nelsonId: {
        type: Number
    }
});

var Kanji = mongoose.model('Kanji', kanjiSchema);

module.exports = Kanji;
