var io = require('socket.io')(8080);
var mqtt    = require('mqtt');
var client  = mqtt.connect({ port: 1883, host: 'localhost'});

 
client.on('connect', function () {
  client.subscribe('tfin1/port0');
  client.subscribe('tfout1/port0');
});
 
client.on('message', function (topic, message) {
  // message is Buffer 
  console.log(topic);
  io.sockets.emit(topic, message.toString());
});

io.on('connection', function(socket) {
    console.log('New Connection');
    socket.on('publish', function(data) {
        topic = data['topic'];
        message = data['message'];
        client.publish(topic, message);
    });
});
