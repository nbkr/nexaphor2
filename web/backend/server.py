import eventlet
import logging
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'fjdaskfjdaksl4732q47329jfklajldfsk74038928403jfkajflsda48230482309'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
forwardings = []
subscriptions = []


@socketio.on('clientmessage')
def handle_clientmessage(data):
    if data['topic'] in forwardings:
        logging.debug("Publishing: {} with data {}".format(data['topic'], data['message']))
        mqtt.publish(data['topic'], data['message'])


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    logging.debug("Emitting: {} with value {}".format(message.topic, message.payload.decode()))
    socketio.emit(message.topic, message.payload.decode())


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    logging.info('MQTT connected!')
    for line in subscriptions:
        print('Subscribing to: {}'.format(line.strip()))
        mqtt.subscribe(line.strip())

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s', level=logging.DEBUG)

    with open('forwardings.txt') as k:
        for line in k:
            forwardings.append(line.strip())

    with open('subscriptions.txt') as k:
        for line in k:
            subscriptions.append(line.strip())

    socketio.run(app, host='127.0.0.1', port=8080, use_reloader=False, debug=False)
    #eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 8080)), app)
