import logging
import paho.mqtt.client as mqtt

class Controller(object):

    def __init__(self):
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._topic2objects = {}
        self._started = False
        self._logger = logging.getLogger('controller')
        self._objects = []

    def _on_message(self, client, userdata, msg):
        self._logger.debug('received: {}/{}'.format(msg.topic, str(msg.payload)))
        if msg.topic not in self._topic2objects:
            return

        for c in self._topic2objects[msg.topic]:
            o = c['object']
            n = c['name']
            self._logger.debug('forwarding: {}/{} to object "{}"'.format(
                msg.topic,
                str(msg.payload),
                n))
            o.message(msg.topic, str(msg.payload))

    def _on_connect(self, client, userdata, flags, rc):
        for t in self._topic2objects:
            logging.debug('subscribing system to topic "{}"'.format(t))
            self._client.subscribe(str(t))

    def registerLogic(self, name, config):
        #Creating an object
        componentfname = 'helpers.{}'.format(config['type'])

        try:
            classname = componentfname.split('.')[-1]
            module = componentfname.replace('.' + classname, '') 
            mod = __import__(module, fromlist=[classname])
            classobject = getattr(mod, classname)
        except Exception, msg:
            print msg 
            raise

        # New we actually create the object, give it it's configuration
        # and a reference to the controller, it should subscribe itself
        logging.debug('creating helper "{}" of type "{}"'.format(
            name,
            config['type']))
        component = classobject(self, name, config) 
        self._objects.append(component)

    def subscribe(self, component, name, topic):
        if topic not in self._topic2objects:
            self._topic2objects[topic] = []

        self._topic2objects[topic].append({'object': component,
                                           'name': name})

    def publish(self, topic, message):
        if self._started:
            self._logger.debug('sending: {}/{}'.format(
                topic, message))
            self._client.publish(topic, message)

    def shutdown(self):
        for o in self._objects:
            o.shutdown()

    def start(self):
        self._client.connect("localhost", 1883, 60)

        self._started = True

        # Looping over mqtt messages
        try:
            self._logger.info('Starting loop')
            self._client.loop_forever()
        except Exception, msg:
            self._logger.info('Stopping')
            self._logger.debug(msg)
