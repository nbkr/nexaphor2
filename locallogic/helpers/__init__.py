import logging

class Helper(object):

    def __init__(self, controller, name, config):
        self._c = controller
        self._config = config
        self._name = name
        self._logger = logging.getLogger('helper')

        self._subscribe()

        self._logger.debug('Created helpler "{}" of type "{}"'.format(
            name,
            config['type']))



    def _subscribe(self):
        """ Overwrite this """
        self._logger.debug('Subscribing to topic "{}" by helpler "{}"'.format(
            self._config['intopic'],
            self._name))
        self._c.subscribe(self, self._name, self._config['intopic'])


    def message(self, topic, message):
        """ Overwrite this """
        pass
