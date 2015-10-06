
var spawn = require('child_process').spawn;

var standardOut = "";

var _ = require("underscore");
var express = require("express");
var app = express();
var server = app.listen(4000);
var io = require('socket.io').listen(server);

app.get("/", function (req, res) {
    res.sendFile(__dirname + "/public/index.html");
});

var process = spawn('python', ['partyled.py', 'node']);
process.stdout.on('data', function (data) {


    var packet = data.toString().split(";").map(function(i) {
        return i.split(",").map(function(i) {
            return parseFloat(i);
        });
    });

    io.emit('tick', packet);
});