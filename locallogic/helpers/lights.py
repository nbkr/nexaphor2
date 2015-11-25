import logging
from helpers import Helper

class Light(Helper):
    """ A light is a simple object that forwards accepts
        up/down as intopic and forwards it to it's outtopic """

    def message(self, topic, message):
        if message == 'up':
            self._logger.debug('Switching light "{}" on'.format(self._name))
            self._c.publish(self._config['outtopic'], 'up')

        if message == 'down':
            self._logger.debug('Switching light "{}" off'.format(self._name))
            self._c.publish(self._config['outtopic'], 'down')
