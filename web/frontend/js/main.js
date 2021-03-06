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

    data = {};
    data['topic'] = topic;
    data['message'] = message;

    socket.emit('clientmessage', data);
    console.log('emitting: ' + topic + '/' + message);
}


function message(topic, message) {
    // Find the objects that are subscribed to this topic, and pass them topic and message.
    console.log('received: ' + topic + '/' + message)

    if (! (topic in topics2components)) {
        return;
    }

    console.log('forwarded: ' + topic + '/' + message)

    var c = null;
    for (var i = 0; i < topics2components[topic].length; i++) {
        c = topics2components[topic][i];
            c.message(topic, message);
    }
}

function subscribe(topic, obj) {
    if (! (topic in topics2components)) {
        topics2components[topic] = [];
    }

    topics2components[topic].push(obj);
 
    console.log('Subscribing to: ' + topic);

    var ptopic = topic;
    socket.on(topic, function(data) {
        message(ptopic, data);
    });

}

function getCurrentPage(config) {
    var page = config['meta']['mainpage'];
    var hash = window.location.hash.substring(1);
    if (hash != '') {
        if (hash in config['pages']) {
            page = hash;
        }
    }

    return page
}

function renderContent(config) {
    // Clearing the old content
    var myNode = document.getElementById("nbkrcontent");
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }

    // Add Items according to the page configration
    page = getCurrentPage(config)
    for (var i = 0; i < config['pages'][page]['items'].length; i++) {
        var o = config['pages'][page]['items'][i];

        // Creating an object of this new type.
        var component = new window[o['type']](o);

        component.renderHtml('#nbkrcontent');
    }
    
    // Ading the menu - quick and dirty for now, we could just move the active class
    var myNode = document.getElementById("navmenu");
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }
    for (p in config['pages']) {
        if (p == page) {
            $('#navmenu').append('<li class="active"><a href="#' + p + '">' + config['pages'][p]['label'] + '</a></li>');
        } else {
            $('#navmenu').append('<li><a href="#' + p + '">' + config['pages'][p]['label'] + '</a></li>');
        }
    }
}


function setup(config) {
    socket = io();

    page = getCurrentPage(config)

    // Setting the name
    $('#brandname').text(config['meta']['label']);
    $('title').text(config['meta']['label']);


    var navMain = $("#navbar");
    navMain.on("click", "a", null, function () {
        navMain.collapse('hide');
    });

    window.addEventListener('hashchange', function() { renderContent(config) });
    window.addEventListener('focus', function() { renderContent(config) });


    var lconfig = config;
    socket.on('connect', function (){
       console.info('Connected');
       // We render the page after he socket has connected as the components will subscribe
       // themself after rendering. So we should be connected before hand.
       renderContent(lconfig)
	});




}


$( document ).ready(function() {
    // Load the configuration
    $.getJSON('frontendconfig.json', function(data) {
        setup(data);
    });
});

