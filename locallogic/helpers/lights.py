import logging
from helpers import Helper
from thread import start_new_thread
import time

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


class TimedLight(Helper):
    """ see ../docs/helpers.rst """

    def __init__(self, controller, name, config):
        super(TimedLight, self).__init__(controller, name, config)
        self._interval = config['interval']
        self._timeleft = self._interval
        self._shutdown = False

        start_new_thread(self.runner, ())

    def runner(self):
        while not self._shutdown:
            if self._timeleft == 0:
                self._c.publish(self._config['outtopic'], 'down')

            if self._timeleft >= 0:
                self._timeleft = self._timeleft - 1 

            time.sleep(1)


    def shutdown(self):
        self._shutdown = True


    def message(self, topic, message):
        if message == 'up':
            self._logger.debug('Resetting Countdown at "{}"'.format(self._name))
            self._timeleft = self._interval

            self._logger.debug('Switching light "{}" on'.format(self._name))
            self._c.publish(self._config['outtopic'], 'up')

