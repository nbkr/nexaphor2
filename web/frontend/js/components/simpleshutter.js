/*
 * A Shutter contains to buttons, one for up, one for down.
 */
var SimpleShutter = function (config) {
    this.config = config;
    this.id = makeid();
}

SimpleShutter.prototype.renderHtml = function (identifier) {
    var myself = this;

    $(identifier).append( '<div style="width:100%" class="well well-sm">'
                        + '<button type="button" class="btn btn-default" style="width:15%" id="SimpleShutter_up_' + this.id + '"><span class="glyphicon glyphicon-chevron-up"></span></button>'
                        + ''
                        + '<div style="display: inline-block; width:70%; text-align:center;">'
                        + this.config['label']
                        + '</div>'
                        + ''
                        + '<button type="button" class="btn btn-default" style="width:15%" id="SimpleShutter_down_' + this.id + '"><span class="glyphicon glyphicon-chevron-down"></span></button>'
                        + '</div>');

    $('#SimpleShutter_up_' + this.id).click( function () {
            myself.up();
        });
                                        

    $('#SimpleShutter_down_' + this.id).click( function () {
            myself.down();
        });
                                          
}

SimpleShutter.prototype.up = function () {
    publish(this.config['outtopic'], 'up');
}

SimpleShutter.prototype.down = function () {
    publish(this.config['outtopic'], 'up');
}
