var socket = null;
var topics2components = {};


function makeid() {
    var text = ""; 
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function publish(topic, message) {
    console.log('emitting: ' + topic + '/' + message);
    socket.emit(topic, message);
}


function message(topic, message) {
    // Find the objects that are subscribed to this topic, and pass them topic and message.
    if (! (topic in topics2components)) {
        return;
    }

    var c = null;
    console.log(topic2components);
    console.log(topic);
    for (var i = 0; topics2components[topic].length; i++) {
        c = topics2components[topic][i];
        c['message'](topic, message);
    }
}

function subscribe(topic, object) {
    if (! (topic in topics2components)) {
        topics2components[topic] = [];
    }

    topics2components[topic].push(object);

    var ptopic = topic;
    socket.on(topic, function(data) {
        message(ptopic, data);
    });

}


function setup(config) {
    socket = io.connect('//' + config['meta']['socketio']['host'] + ':' + config['meta']['socketio']['port']);

    // Deside on which page we are.
    var page = config['meta']['mainpage'];
    var hash = window.location.hash.substring(1);
    if (hash != '') {
        if (hash in config['pages']) {
            page = hash;
        }
    }

    // Setting the name
    $('#brandname').text(config['meta']['label']);
    $('title').text(config['meta']['label']);

    // Ading the menu
    for (p in config['pages']) {
        if (p == page) {
            $('#navmenu').append('<li class="active"><a href="#' + p + '">' + config['pages'][p]['label'] + '</a></li>');
        } else {
            $('#navmenu').append('<li><a href="#' + p + '">' + config['pages'][p]['label'] + '</a></li>');
        }
    }

    // Add Items according to the page configration
    for (var i = 0; i < config['pages'][page]['items'].length; i++) {
        var o = config['pages'][page]['items'][i];

        // Creating an object of this new type.
        var component = new window[o['type']](o);

        component.renderHtml('#nbkrcontent');
    }
}


$( document ).ready(function() {
    // Load the configuration
    $.getJSON('frontendconfig.json', function(data) {
        setup(data);
    });
});

