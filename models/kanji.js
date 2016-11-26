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
        required: true,
        unique: true
    },
    svg: {
        type: [String],
        required: true
    }
});

var Kanji = mongoose.model('Kanji', kanjiSchema);

module.exports = Kanji;
