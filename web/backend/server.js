var io = require('socket.io')(8080);
var mqtt    = require('mqtt');
var client  = mqtt.connect({ port: 1883, host: 'localhost'});
var fs = require('fs');

 
client.on('connect', function () {
  // Reading the topics we should subscribe to.
  fs.readFile('subscriptions.txt', 'utf8', function (err,data) {
    if (err) {
      return console.log(err);
    }

    var lines = data.trim().split("\n")
    for (var i = 0; i < lines.length; i++) {
        console.log(i);
        if (lines[i].trim() != '') {
            console.log('Subscribing to ' + lines[i].trim());
            client.subscribe(lines[i].trim());
        }
    }
  });
});
 
client.on('message', function (topic, message) {
  io.sockets.emit(topic, message.toString());
});

io.on('connection', function(socket) {
    console.log('New Connection');

    // Reading the allowd forwardings. I'm not sure 
    // if this is a good idea to do this here. 
    //
    // On the one hand
    // a change in 'forwardings.txt' doesn't require a restart,
    // just a reload from the browser.
    //
    // On the other hand now the file is read everytime a bowser 
    // connects.
    fs.readFile('forwardings.txt', 'utf8', function (err,data) {
        if (err) {
            return console.log(err);
        }

        lines = data.trim().split("\n")
        for (var i = 0; i < lines.length; i++) {
            var topic = lines[i].trim()
            console.log('Adding socket.io forwarding: ' + topic);
            socket.on(topic, function(data) {
                var ptopic = topic;
                console.log('publishing ' + ptopic + '/' + data); 
                client.publish(ptopic, data);
            });
        }
    });
    
});


