function point(x) {
    for (var g = [], A = "0123456789abcdef", I = 0; I < 36; I++)
        g[I] = A.substr(Math.floor(16 * Math.random()), 1);
    g[14] = "4",
        g[19] = A.substr(3 & g[19] | 8, 1),
        g[8] = g[13] = g[18] = g[23] = "-";
    var C = "point-" + g.join("")
    return C
}

console.log(point(1))