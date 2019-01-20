#! /usr/bin/env python

import logging
import paho.mqtt.client as mqtt
from functools import partial
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
from tinkerforge.bricklet_industrial_digital_out_4 \
            import IndustrialDigitalOut4
from tinkerforge.bricklet_io4 import BrickletIO4
from tinkerforge.bricklet_io16 import BrickletIO16
from tinkerforge.bricklet_nfc_rfid import NFCRFID
import yaml

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

def on_io16in(client, name, bank, mask, flank):
    for i in range(0, 7):
        if (mask & (1 << i)):
            # Pin "i" fired and it went
            if (flank & (1 << i)):
                state = 'up'
            else:
                state = 'down'

            logging.debug('sending: {}/port{}{}/{}'.format(name, bank, i, state))
            client.publish('{}/port{}{}'.format(name, bank, i), state)

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


def on_ipcon_enmumerate(ipcon_name, objects):
    # Starting all objects that are connected to the ipconnection that
    # is going to be enumerated.
    # Python doesn't copy a string, this makes trouble with the callbacks
    # as their 'name' changes. So I have to do this ugly workaround here.
    for o in objects:
        c = objects[o]

        if objects[c['ipcon']] != ipcon_name:
            # Make sure only those objects get configured for which
            # IPCon the call back has been called.
            continue

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
            for i in range(0, len(c['inout'])):
                if c['inout'][i] == 'o':
                    io4.set_configuration(1 << i, 'o', False)

                if c['inout'][i] == 'i':
                    io4.set_configuration(1 << i, 'i', True)
                    io4.set_interrupt(io4.get_interrupt() | (1 << i)) 

            c['object'] = io4

        if c['type'] == 'io16':

            # Create object
            io16 = BrickletIO16(c['uid'], objects[c['ipcon']]['ipcon'])

            # Callback
            io16.register_callback(
                io16.CALLBACK_INTERRUPT,
                partial(on_io16in, client, o))

            # Setting the configuration
            for port in ['a', 'b']:
                for i in range(0, len(c['inout_' + port])):
                    if c['inout_' + port][i] == 'o':
                        io16.set_configuration(port, 1 << i, 'o', False)

                    if c['inout'][i] == 'i':
                        io16.set_configuration(port, 1 << i, 'i', True)
                        io16.set_port_interrupt(
                            port,
                            io16.get_port_interrupt(port) | (1 << i)) 

            c['object'] = io16

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


def on_ipcon_connected(ipcon):
    """ Everytime we connect, we just call the enumration, which will configure all connected bricks """
    ipcon.enumerate()

    

def on_connect(client, userdata, flags, rc):
    """ Callback for connection to mqtt """
    for o in objects:
        # the digout subscribe to topics
        if objects[o]['type'] == 'idout':
            client.subscribe('{}/+/set'.format(o))

        # The outputs of the io4 subscribe to topics.
        if objects[o]['type'] == 'io4':
            client.subscribe('{}/+/set'.format(o))

        # The outputs of the io16 subscribe to topics.
        if objects[o]['type'] == 'io16':
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

    if objects[recp]['type'] in ['io16']:
        tfobject = objects[recp]['object']
        bank = msg.topic[msg.topic.find('port') + 4:msg.topic.find('port') + 5]
        port = msg.topic[msg.topic.find('port') + 5:msg.topic.find('port') + 6]
        port = int(port)
        message = str(msg.payload)
        state = message

        logging.debug("received: {}/port{}{}/set/{}".format(recp, bank, port, message))

        if message not in ['up', 'down', 'current']:
            return

        if message == 'up':
            tfobject.set_port(bank, tfobject.get_port(bank) | (1 << port))

        if message == 'down':
            tfobject.set_port(bank, tfobject.get_port(bank) & ~(1 << port))

        # We need to be able to ask the current state of the port
        # So basically we tell the port to set it to it's current
        # value. This way it isn't confusing to /set the port to
        # something like 'getvalue'.
        if message == 'current':
            if (tfobject.get_value() & (1 << port)):
                state = 'up'
            else:
                state = 'down'

        logging.debug('sending: {}/port{}{}/{}'.format(recp, bank, port, state))
        client.publish('{}/port{}{}'.format(recp, bank, port), state)

    if objects[recp]['type'] in ['idout', 'io4']:
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
    with open('tfdata.yml') as data_file:    
        objects = yaml.load(data_file)


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
            c['ipcon'].register_callback(c['ipcon'].CALLBACK_ENUMERATE, 
                                          partial(on_ipcon_enumerate, o, objects))

            c['ipcon'].register_callback(c['ipcon'].CALLBACK_CONNECTED, 
                                          partial(on_ipcon_connected, c['ipcon']))
            c['ipcon'].connect(c['host'], c['port'])
            c['ipcon'].enumerate()



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
