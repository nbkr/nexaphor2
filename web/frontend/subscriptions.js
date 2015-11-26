

socket.on('tfout1/port0', function (data) {
    console.log('Got state change for tfout1/port0, new state: ' + data);

    if (data == 'up') {
        document.getElementById('licht1').textContent = 'an';
    }

    if (data == 'down') {
        document.getElementById('licht1').textContent = 'aus';
    }
});
