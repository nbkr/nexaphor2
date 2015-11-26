/*
 * An upbutton simply sends and 'up' to its 'outtopic'.
 */
var upbutton = function (config) {
    this.config = config;
    this.id = makeid();
}

upbutton.prototype.renderHtml = function (identifier) {
    var myself = this;

    $(identifier).append('<button type="button" class="btn btn-block btn-default" id="upbutton_' + this.id + '">' + this.config['label'] + '</button><br>');

    // Adding the click to the button
    $('#upbutton_' + this.id).click(function () {
            myself.onClick();
    }); 
}

upbutton.prototype.onClick = function () {
    publish(this.config['outtopic'], 'up');
}
