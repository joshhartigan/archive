var http = require('http');
var fs = require('fs');

var get = function(url, dest) {
  var file = fs.createWriteStream(dest);
  var req = http.get(url, function(response) {
    response.pipe(file);
    file.on('finish', function() {
      file.close();
    });
  }).on('error', function(error) {
    fs.unlink(dest);
  })
}

module.exports.get = get;

