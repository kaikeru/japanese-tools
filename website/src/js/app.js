$ = jQuery = require('jquery');
var bootstrap = require('../../node_modules/bootstrap-sass/assets/javascripts/bootstrap');

function createKanjiStrokeItem(kanjiObj){

    // List item
    var listItem = $("<div class='item row'></div>");
    listItem.attr({id: "kanji-" + kanjiObj.character});

    // Meta
    var meta = $("<div class='meta col-md-3'></div>");
    listItem.append(meta);

    // Title
    var title = $("<h3 class='character'>" + kanjiObj.character + "</h3>");
    meta.append(title);

    // Readings
    var readings = $("<table class='table table-striped readings'><tbody></tbody></table>");
    meta.append(readings);

    if(kanjiObj.meanings.length > 0) {
        var meanings = $("<tr class='meanings'><td class='title'>meaning</td></tr>");
        meanings.append($("<td class='reading'></td>").append(kanjiObj.meanings.join(', ')));
        readings.append(meanings);
    }

    if (kanjiObj.readings.onyomi.length > 0){
        var onyomi = $("<tr class='onyomi'><td class='title'>onyomi</td></tr>");
        onyomi.append($("<td class='reading'></td>").append(kanjiObj.readings.onyomi.join(', ')));
        readings.append(onyomi);
    }
    if (kanjiObj.readings.kunyomi.length > 0){
        var kunyomi = $("<tr class='kunyomi'><td class='title'>kunyomi</td></tr>");
        kunyomi.append($("<td class='reading'></td>").append(kanjiObj.readings.kunyomi.join(', ')));
        readings.append(kunyomi);
    }
    if (kanjiObj.readings.nanori.length > 0){
        console.log(kanjiObj.readings.nanori);
        var nanori = $("<tr class='nanori'><td class='title'>nanori</td></tr>");
        nanori.append($("<td class='reading'></td>").append(kanjiObj.readings.nanori.join(', ')));
        readings.append(nanori);
    }

    // Print button
    var printButton = $("<a target='_blank' class='printButton btn btn-success' href='/worksheet/" + kanjiObj.character + "' role='button'><span class='glyphicon glyphicon-print' aria-hidden='true'></span>&nbsp;&nbsp;Worksheet</a>")
    meta.append(printButton);

    // Right
    var rightCol = $("<div class='col-md-9'></div>");
    listItem.append(rightCol);

    //SVG
    var svg = $("<div class='stroke col-md-9'></div>");
    rightCol.append(svg);
    for (var j = 0; j < kanjiObj.svg.length; j++){
        svg.append(kanjiObj.svg[j]);
    }

    return listItem;
}

function createKanjiList(kanjis){
    var container = $("<div></div>");
    for(var i=0; i<kanjis.length; i++){
        var link = $("<a class='item' href='#kanji-" + kanjis[i].character + "'>" + kanjis[i].character + "</a>");
        container.append(link);
    }
    return container;
}

// Unique array.
function uniq_fast(a) {
    var seen = {};
    var out = [];
    var len = a.length;
    var j = 0;
    for(var i = 0; i < len; i++) {
        var item = a[i];
        if(seen[item] !== 1) {
            seen[item] = 1;
            out[j++] = item;
        }
    }
    return out;
}

// Sort the kanji back to their order.
function sortKanji(inputKanji, responseKanji){
    var retKanji = [];
    var tmpDict = {};

    for(var i=0; i < responseKanji.length; i++){
        tmpDict[responseKanji[i].character] = responseKanji[i];
    }

    for(var i=0; i<inputKanji.length; i++){
        retKanji.push(tmpDict[inputKanji[i]]);
    }

    return retKanji;
}

$(function(){
    $('#form-list').on('submit', function () {
        var kanjis = uniq_fast($("#form-list :input[name=kanji]").val());
        $.ajax({
            url: "kanji?k=" + kanjis.join(""),
            headers: {
                Accept : "application/json"
            },
            data: {},
            success : function(response) {
                var list = $("#kanjiList-available");
                list.empty();
                var strokes = $("#kanjiStrokes-listing");
                strokes.empty();

                // Make them sorted
                var sortedKanji = sortKanji(kanjis, response);

                // List them
                list.append(createKanjiList(sortedKanji));

                // Get the stroke orders
                $.each(sortedKanji, function(i, c){
                    var strokesItem = createKanjiStrokeItem(c);
                    strokes.append(strokesItem);
                });
            }
        });
        return false;
    });

    $('#form-wanikani').on('submit', function() {
        var apikey = $("#form-wanikani :input[name=wanikani-api-key]").val();
        $.ajax({
            url: "wanikani?key=" + apikey,
            headers: {
                Accept: "application/json"
            },
            data: {},
            success: function(res) {
                var list = $("#kanjiList-available");
                list.empty();
                var strokes = $("#kanjiStrokes-listing");
                strokes.empty();

                // List them
                list.append(createKanjiList(res));

                // Get the stroke orders
                $.each(res, function(i, c){
                    var strokesItem = createKanjiStrokeItem(c);
                    strokes.append(strokesItem);
                });
            }
        });
        return false;
    });
})
