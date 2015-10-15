var fs = require("fs");
var spawn = require('child_process').spawn;
var _ = require("underscore");
var express = require("express");
var app = express();
var server = app.listen(4000);
var io = require('socket.io').listen(server);

app.get("/", function (req, res) {
    res.sendFile(__dirname + "/templates/index.html");
});

app.get("/settings", function(req, res) {
    res.send({"connection": "socketio"});
});


var switches = {};
var master = 1;

var sendSwitch = function() {
    var command = "v;";
    Object.keys(switches).forEach(function(key) {
        command += key + "$" + (switches[key] ? 1 : 0) + "%"
    });
    console.log("sending command: " + command);
    if (process) process.stdin.write(command+"\n");
};

io.on('connection', function (socket) {
    socket.emit("switches", switches);
    socket.emit("master", master);
    socket.on("switch", function(pattern) {
        if (switches[pattern] === undefined) {
            switches[pattern] = true
        } else {
            switches[pattern] = !switches[pattern]
        }

        sendSwitch();
        io.emit("switches", switches);
    });
    socket.on("set", function(pattern) {
        switches[pattern["name"]] = pattern["value"];

        sendSwitch();
        io.emit("switches", switches);
    });
    socket.on("master", function(value) {
        process.stdin.write("m;"+value+"\n")
    })
});

var sendTick = function(packet) {
    io.emit('tick', packet);
};

var tick = _.throttle(sendTick, 10);

var process;
var ledProcess = function() {
    process = spawn('python', ['partyled.py', 'node']);
    process.stdin.setEncoding('utf-8');
    process.stdout.on('data', function (data) {
        var packet = data.toString().replace(/\n/g, "").split(";").map(function (i) {
            var separated = i.split(",");
            if (parseInt(separated[0]) === 0) {
                return separated.map(function (i) {
                    return parseFloat(i);
                });
            }

            if (separated[0] === '1' && separated.length > 1 && separated[1].indexOf("FPS") > -1) {
                console.log(separated);
            }

            return i
        });
        tick(packet);
    });

    process.stderr.on('data', function (data) {
        console.error(data.toString());
    });

    sendSwitch();
};

ledProcess();

fs.watch(".", function (event, filename) {
    console.log("restart", event, filename);
    if (!(filename === "partyled.py" || filename === "generators.py")) return;
    process.kill();
    ledProcess();
});
