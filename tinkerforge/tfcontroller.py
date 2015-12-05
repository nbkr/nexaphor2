#! /usr/bin/env python

import logging
import paho.mqtt.client as mqtt
from functools import partial
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
from tinkerforge.bricklet_industrial_digital_out_4 \
            import IndustrialDigitalOut4
from tinkerforge.bricklet_io4 import BrickletIO4
from tinkerforge.bricklet_nfc_rfid import NFCRFID
import json

# Somehow needed for the NFC Reader
tagtype = 0


def on_idin(client, name, mask, flank):
    for i in range(0, 4):
        if (mask & (1 << i)):
            # Pin "i" fired and it went
            if (flank & (1 << i)):
                state = 'up'
            else:
                state = 'down'

            logging.debug('sending: {}/port{}/{}'.format(name, i, state))
            client.publish('{}/port{}'.format(name, i), state)

def on_io4in(client, name, mask, flank):
    for i in range(0, 4):
        if (mask & (1 << i)):
            # Pin "i" fired and it went
            if (flank & (1 << i)):
                state = 'up'
            else:
                state = 'down'

            logging.debug('sending: {}/port{}/{}'.format(name, i, state))
            client.publish('{}/port{}'.format(name, i), state)

def on_nfc(client, name, obj, state, idle):
    if idle:
        global tagtype
        tagtype = (int(tagtype) + 1) % 3
        obj.request_tag_id(tagtype)

    if state == nfc.STATE_REQUEST_TAG_ID_READY:
        ret = obj.get_tag_id()
        tagid = ''.join(map(
            str, map(int, ret.tid[:ret.tid_length])))

        logging.debug('I ({}) found a new tag with id "{}".'.format(
            name, tagid))

             
        # Sending the tag to our topic
        logging.debug('sending: {}/{}'.format(name, tagid))
        client.publish('{}'.format(name), tagid)


def on_connect(client, userdata, flags, rc):
    for o in objects:
        # the digout subscribe to topics
        if objects[o]['type'] == 'idout':
            client.subscribe('{}/+/set'.format(o))

        # The outputs of the io4 subscribe to topics.
        if objects[o]['type'] == 'io4':
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


    if objects[recp]['type'] == 'idout' or objects[recp]['type'] == 'io4':
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
    # Python doesn't copy a string, this makes trouble with the callbacks
    # as their 'name' changes. So I have to do this ugly workaround here.
    for o in objects:
        c = objects[o]

        if c['type'] == 'idin':
            # Create object
            idin4 = IndustrialDigitalIn4(c['uid'], objects[c['ipcon']]['ipcon'])
            idin4.register_callback(
                idin4.CALLBACK_INTERRUPT,
                partial(on_idin, client, o))

            # Enable interrupt on all 4 pins
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 0)) 
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 1)) 
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 2)) 
            idin4.set_interrupt(idin4.get_interrupt() | (1 << 3))

        if c['type'] == 'io4':

            # Create object
            io4 = BrickletIO4(c['uid'], objects[c['ipcon']]['ipcon'])

            # Callback
            io4.register_callback(
                io4.CALLBACK_INTERRUPT,
                partial(on_io4in, client, o))

            # Setting the configuration
            for i in range(0, len(c['inout']):
                if c['inout'][i] == 'o':
                    id4.set_configuration(1 << i, 'o', False)

                if c['inout'][i] == 'i':
                    id4.set_configuration(1 << i, 'i', True)
                    id4.set_interrupt(1 << i)

            c['object'] = id4

        if c['type'] == 'idout':
            c['object'] = IndustrialDigitalOut4(c['uid'],
                                                objects[c['ipcon']]['ipcon'])

        if c['type'] == 'nfc':
            nfc = NFCRFID(c['uid'],
                           objects[c['ipcon']]['ipcon'])

            nfc.register_callback(
                nfc.CALLBACK_STATE_CHANGED,
                partial(on_nfc, client, o, nfc))

            # Starting the initial tag scan
            nfc.request_tag_id(nfc.TAG_TYPE_MIFARE_CLASSIC)


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
