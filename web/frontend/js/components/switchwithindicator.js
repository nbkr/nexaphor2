// A comibation of a switch and a status indicator
// it will switch the 'id' you assign and
// display the status of the 'statusport'

SwitchWithIndicator = function (config) {
    this.config = config;
    this.id = makeid();
    this.onclass = 'well-success';
};

SwitchWithIndicator.prototype.subscribe = function() {

    // Subscribing to the intopic to get status messages.
    subscribe(this.config['intopic'], this);

    // to get the current mode of the timed light
    // we send out a message to set the ligh to 
    // the 'current' value. This way we will receive
    // the actual value back.
    publish(this.config['outtopic'], 'current');
};

SwitchWithIndicator.prototype.renderHtml = function (identifier) {
    var myself = this;
    $(identifier).append( '<div style="width:100%" class="well well-sm" id="switchwithindicator_' + this.id + '">'
                        + '<button type="button" class="btn btn-default" style="width:15%" id="switchwithindicator_on_' + this.id + '">' + this.config['label_on'] + '</button>'
                        + ''
                        + '<div style="display: inline-block; width:70%; text-align:center;" id="#switchwithindicator_' + this.id + '">'
                        + this.config['label']
                        + '</div>'
                        + ''
                        + '<button type="button" class="btn btn-default" style="width:15%" id="switchwithindicator_off_' + this.id + '">' + this.config['label_off'] + '</button>'
                        + '</div><br>');

    $('#switchwithindicator_off_' + this.id).click(function () {
            myself.off();
        });

    $('#switchwithindicator_on_' + this.id).click(function () {
            myself.on();
        });
};

SwitchWithIndicator.prototype.on = function () {
    publish(this.config['outtopic'], 'up');
};

SwitchWithIndicator.prototype.off = function () {
    publish(this.config['outtopic'], 'down');
};

SwitchWithIndicator.prototype.message = function (msg) {
    if (msg == 'up') {
        $('#switchwithindicator_' + this.id).addClass(this.onclass);
    } 
    
    if (msg == 'down') {
        $('#switchwithindicator_' + this.id).removeClass(this.onclass);
    }
}
