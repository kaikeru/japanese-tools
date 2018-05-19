module.exports = {
    modIf: modIf,
    toLowerCase: toLowerCase
}

function modIf(index_count, mod, block) {

    if (parseInt(index_count) % (mod) === 0) {
        return block.fn(this);
    }
}

function toLowerCase(str) {
    return str.toLowerCase();
}