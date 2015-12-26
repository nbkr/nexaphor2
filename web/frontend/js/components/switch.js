// A simple switch, that you can set to 'on' or 'off' and it
// will submit up and down respectifly. Interesstingly enought
// we have a slight problem with this. Because an 'on', 'off'
// switch we planned to use has a status. Therefore I don't use
// the bootstrap switch, but a simple two button switch.

Switch = function (config) {
    this.config = config;
    this.id = makeid();
};

Switch.prototype.renderHtml = function (identifier) {
    var myself = this;
    $(identifier).append( '<div style="width:100%" class="well well-sm">'
                        + '<button type="button" class="btn btn-default" style="width:15%" id="switch_on_' + this.id + '">' + this.config['label_on'] + '</button>'
                        + ''
                        + '<div style="display: inline-block; width:70%; text-align:center;">'
                        + this.config['label']
                        + '</div>'
                        + ''
                        + '<button type="button" class="btn btn-default" style="width:15%" id="switch_off_' + this.id + '">' + this.config['label_off'] + '</button>'
                        + '</div><br>');

    $('#switch_off_' + this.id).click(function () {
            myself.off();
        });

    $('#switch_on_' + this.id).click(function () {
            myself.on();
        });
};

Switch.prototype.on = function () {
    publish(this.config['outtopic'], 'up');
};

Switch.prototype.off = function () {
    publish(this.config['outtopic'], 'down');
};

