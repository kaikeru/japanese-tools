var Promise = require('bluebird');
var fs = Promise.promisifyAll(require('fs'));

function main(){
    var dirName = __dirname + '/kanji';
    var files = fs.readdirSync(dirName);
    files.forEach((file) => {
        if (file.split('.').pop() != "svg") {
            return;
        }
        var data = fs.readFileSync(dirName + '/' + file);
        var lines = data.toString().split('\n');
        var i = 0;
        for(; i < lines.length; i++){
            var line = lines[i];
            if(line.indexOf('<svg xmlns') > -1) {
                break;
            }
        }
        lines = lines.slice(i).join('\n');
        var wrote = fs.writeFileSync(__dirname + '/kanji_fixed/' + file, lines);
    });
}

main();
