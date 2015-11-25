#! /usr/bin/env python

import logging
import paho.mqtt.client as mqtt
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
from tinkerforge.bricklet_industrial_digital_out_4 \
            import IndustrialDigitalOut4
import json


def on_idin(client, name, mask, flank):
    # publish message
    for i in range(0, 4):
        if (mask & (1 << i)):
            # Pin "i" fired and it went
            if (flank & (1 << i)):
                state = 'up'
            else:
                state = 'down'

            logging.debug('sending: {}/port{}/{}'.format(name, i, state))
            client.publish('{}/port{}'.format(name, i), state)

def on_connect(client, userdata, flags, rc):
    # the digout subscribe to topics
    for o in objects:
        if objects[o]['type'] == 'idout':
            client.subscribe('{}/+/set'.format(o))

def on_message(client, userdata, msg):
    # Checking for which object (currently only idouts) the message
    # was and setting the port appropriatly.
    if msg.topic.find('/') < 0:
        return

    # Check if we have recpient for it
    recp = msg.topic[0:msg.topic.index('/')]
    if not recp in objects:
        return


    if objects[recp]['type'] == 'idout':
        tfobject = objects[recp]['object']
        port = msg.topic[msg.topic.find('port') + 4:msg.topic.find('port') + 5]
        port = int(port)
        message = str(msg.payload)
        state = message

        logging.debug("received: {}/port{}/set/{}".format(recp, port, message))

        if message not in ['up', 'down', 'current']:
            return

        if message == 'up':
            tfobject.set_value(tfobject.get_value() | (1 << port))

        if message == 'down':
            tfobject.set_value(tfobject.get_value() & ~(1 << port))

        # We need to be able to ask the current state of the port
        # So basically we tell the port to set it to it's current
        # value. This way it isn't confusing to /set the port to
        # something like 'getvalue'.
        if message == 'current':
            if (tfobject.get_value() & (1 << port)):
                state = 'up'
            else:
                state = 'down'

        logging.debug('sending: {}/port{}/{}'.format(recp, port, state))
        client.publish('{}/port{}'.format(recp, port), state)




if __name__ == '__main__': 

    logging.basicConfig(level=logging.DEBUG)

    logging.info('Reading configuration')
    with open('tfdata.json') as data_file:    
        objects = json.load(data_file)


    # Connecting to mqtt
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    # Tinkerforge part
    # Connecting the IPs
    for o in objects:
        c = objects[o]

        if c['type'] == 'ipcon':
            logging.info('Connecting to brickd')
            c['ipcon'] = IPConnection()
            c['ipcon'].connect(c['host'], c['port'])

    # Starting the other objects
    for o in objects:
        c = objects[o]

        if c['type'] == 'idin':
            name = o[:]
            # Create object
            idin4 = IndustrialDigitalIn4(c['uid'], objects[c['ipcon']]['ipcon'])
            idin4.register_callback(
                idin4.CALLBACK_INTERRUPT,
                lambda mask, flank: on_idin(client, name, mask, flank))

            # Enable interrupt on all 4 pins
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 0)) 
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 1)) 
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 2)) 
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 3))

        if c['type'] == 'idout':
            c['object'] = IndustrialDigitalOut4(c['uid'],
                                                objects[c['ipcon']]['ipcon'])


    # Looping over mqtt messages
    try:
        logging.info('Starting loop')
        client.loop_forever()
    except Exception, msg:
        logging.info('Stopping')
        logging.debug(msg)

    # Disconnecting
    for o in objects:
        if objects[o]['type'] == 'ipcon':
            objects[o]['ipcon'].disconnect()