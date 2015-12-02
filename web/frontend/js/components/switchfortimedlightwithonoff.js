// This is the switch for our TimedLightWithOnOff Helpr of the logic
// module. It basically sends out 'on', 'off', 'timed' and set's
// it's value accordingly

SwitchForTimedLightWithOnOff = function (config) {
    this.config = config;
    this.id = makeid();
    this.state = 'off';

    // subscribing outside of the construtor, because the object
    // has to exist
    this.subscribe();
};

SwitchForTimedLightWithOnOff.prototype.subscribe = function() {

    // Subscribing to the intopic to get status messages.
    subscribe(this.config['intopic']);

    // to get the current mode of the timed light
    // we send out a message to set the ligh to 
    // the 'current' value. This way we will receive
    // the actual value back.
    publish(this.config['outtopic'], 'current');
};


SwitchForTimedLightWithOnOff.prototype.message = function (topic, msg) {
    if (msg == 'on') {
        $('#timedlight_' + this.id).removeClass('btn-default');
        $('#timedlight_' + this.id).removeClass('btn-warning');
        $('#timedlight_' + this.id).addClass('btn-success');
        this.state = 'on';
    } else if (msg == 'timed') {
        $('#timedlight_' + this.id).removeClass('btn-success');
        $('#timedlight_' + this.id).removeClass('btn-default');
        $('#timedlight_' + this.id).addClass('btn-warning');
        this.state = 'timed';
    } else {
        $('#timedlight_' + this.id).removeClass('btn-success');
        $('#timedlight_' + this.id).removeClass('btn-warning');
        $('#timedlight_' + this.id).addClass('btn-default');
        this.state = 'off';
    }
};

SwitchForTimedLightWithOnOff.prototype.renderHtml = function (div) {
    var myself = this;
    $(div).append('<button type="button" class="btn btn-block btn-default" id="timedlight_' + this.id + '"><span class="glyphicon glyphicon-time"></span> ' + this.config['label'] + '</button><br>');
    $('#timedlight_' + this.id).click(function () {
            myself.toggle();
        });
};

SwitchForTimedLightWithOnOff.prototype.toggle = function () {
    if (this.state == 'on') {
        this.off();
    } else if (this.state == 'timed') {
        this.on();
    } else if (this.state == 'off') {
        this.timed();
    }
}

SwitchForTimedLightWithOnOff.prototype.on = function () {
    publish(this.config['outtopic'], 'on');
};

SwitchForTimedLightWithOnOff.prototype.off = function () {
    publish(this.config['outtopic'], 'off');
};

SwitchForTimedLightWithOnOff.prototype.timed = function () {
    publish(this.config['outtopic'], 'timed');
};
