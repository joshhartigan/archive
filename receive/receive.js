#!/usr/local/bin/node

var request = require('request');
var program = require('commander');
var colors = require('colors');

var download = require('./download');

var rcvLog = function(msg) {
  console.log(' > rcv: '.magenta + msg);
};

program.version('0.1.0')
  .usage('<options> <url>')
  .option('-l, --local', 'Install Thing locally')
  .option('-g, --global', 'Install Thing globally')
  .option('-i, --info', 'Get info on Thing without installing')
  .parse(process.argv);

var thingsRepo = {};

request.get('http://joshhartigan.github.io/receive/things.json',
  function(err, response, body) {
    if (!err && response.statusCode == 200) {
      thingsRepo = JSON.parse(body);

      receiveThing(thingsRepo);
    }
  }
);

var receiveThing = function(json) {
  var thingArg = process.argv[process.argv.length - 1];

  if ( json[thingArg] ) {

    request.get( json[thingArg],
    function(err, response, body) {
      if (!err && response.statusCode == 200) {
        var thingJson = JSON.parse(body);

        rcvLog('located thing ' + thingJson['name'].bold.red + ':');

        if ( thingJson['description'] ) {
          rcvLog( '"' + thingJson['description'] + '"' );
        }

        if ( !( thingJson['get'] && thingJson['file'] ) ) {
          rcvLog(
            'error: '.bold + 'insufficient properties for ' + thingJson['name'].bold.red
          )
        } else {
          download.get( thingJson['get'], thingJson['file'] )
          rcvLog( 'got ' + thingJson['get'].green + ' as ' + thingJson['file'].green );
        }

      }
    });

  } else {
    rcvLog('thing ' + thingArg.bold.red + ' not found.');
  }
};
