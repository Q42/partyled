var fs = require("fs");
var spawn = require('child_process').spawn;
var _ = require("underscore");
var express = require("express");
var app = express();
var server = app.listen(4000);
var io = require('socket.io').listen(server);

app.get("/", function (req, res) {
    res.sendFile(__dirname + "/public/index.html");
});

var sendTick = function(packet) {
    io.emit('tick', packet);
};

var tick = _.throttle(sendTick, 10);

var process;
var ledProcess = function() {
    process = spawn('python', ['partyled.py', 'node']);
    process.stdout.on('data', function (data) {


        var packet = data.toString().split(";").map(function (i) {
            return i.split(",").map(function (i) {
                return parseFloat(i);
            });
        });

        tick(packet);
    });

};

ledProcess();

fs.watch(".", function (event, filename) {
    if (filename !== "partyled.py") return;
    console.log(event, filename);
    process.kill();
    ledProcess();
});