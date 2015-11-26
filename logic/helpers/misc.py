import logging
from helpers import Helper
from thread import start_new_thread
import time


class Impulsegiver(Helper):
    def __init__(self, controller, name, config):
        super(Impulsegiver, self).__init__(controller, name, config)
        self._interval = config['interval']
        self._active = False

    def _offswitcher(self):
        time.sleep(int(self._config['interval']) / 1000.0)
        self._logger.error('Ending Impulse ("{}")'.format(self._name))
        self._c.publish(self._config['outtopic'], 'down')
        self._active = False

    def message(self, topic, message):
        if message == 'up' and not self._active:
            self._active = True
            self._logger.error('Starting Impulse ("{}")'.format(self._name))
            self._c.publish(self._config['outtopic'], 'up')

            # Somehow a  'time_sleep' doesn't really work here so I had
            # to do it with a thread.
            start_new_thread(self._offswitcher, ())
