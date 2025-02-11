//'use strict';

// Depends on:  https://www.npmjs.com/package/sprintf-js
const { sprintf } = require('sprintf-js');

/**
 * Why does the JavaScript engine do this?
 *
 *    017 == '017' := false
 *    018 == '108' := true
 *
 * A professional JS coder asked this seriously on X! This exactly is the reason,
 * why we security researchers have so much work to do. Missing knwoledge!
 *
 * Just a small excursion into number systems:
 *    dec   oct   hex   bin         | dec   oct   hex   bin
 *      0   000     0   0000.0000   |  11   013     b   0000.1011
 *      1   001     1   0000.0001   |  12   014     c   0000.1100
 *      2   002     2   0000.0010   |  13   015     d   0000.1101
 *      3   003     3   0000.0011   |  14   016     e   0000.1110
 *      4   004     4   0000.0100   |  15   017     f   0001.1111
 *      5   005     5   0000.0101   |  16   020    10   0001.0000
 *      6   006     6   0000.0111   |  17   021    11   0001.0001
 *      7   007     7   0000.1000   |  18   022    12   0001.0010
 *      8   010     8   0000.1001   |  19   023    13   0001.0011
 *     10   012     a   0000.1010   |  20   024    14   0001.0100
 */

let div = '', x = 0;
while (x++ < 80) div += '#';

console.log(div);
console.log('Why does the JavaScript engine do ths?');
console.log(div);
console.log(`017 == '017': ${017 == '017'}`);
console.log(`018 == '018': ${018 == '018'}`); // Throws an error when running in
console.log(`019 == '019': ${019 == '019'}`); // strict mode ;-)
console.log(`020 == '020': ${020 == '020'}`);
console.log(div);

let i = 17;
const max = 21;
while (i < max) {
   // Source:
   // https://w3resource.com/javascript-exercises/javascript-math-exercise-3.php
   oct = parseInt(i, 10).toString(8);
   num = sprintf('%03d', i++);
   console.log(`${sprintf("%03d", oct)} == '${num}': ${oct === "$num"}`);
}
console.log(div);

/**
 * Results:
 *    018 is not a valid octal number, so JS does an internal type cast
 *    to string! Hence '018' == '018' := TRUE
 */
// EOF
