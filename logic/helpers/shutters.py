import logging
from helpers import Helper
from thread import start_new_thread
import time


class SimpleShutter(Helper):

    def __init__(self, controller, name, config):
        super(SimpleShutter, self).__init__(controller, name, config)
        self._intervalup = config['interval-up']
        self._intervaldown = config['interval-down']
        self._timeleft = -1 
        self._mode = 'stop'
        self._shutdown = False

        start_new_thread(self.runner, ())

    def runner(self):
        while not self._shutdown:
            if self._timeleft == 0:
                self._c.publish(self._config['outtopic-up'], 'down')
                self._c.publish(self._config['outtopic-down'], 'down')
                self._c.publish(self._config['outtopic-status'], 'stop')
                self._mode = 'stop'

            if self._timeleft >= 0:
                self._timeleft = self._timeleft - 1 

            time.sleep(1)

    def shutdown(self):
        self._shutdown = True


    def message(self, topic, message):

        # If we are currently moving and we get a message that issen't 'status'
        # then we stop immediatelly.
        if self._mode != 'stop' and message != 'status':
            self._c.publish(self._config['outtopic-up'], 'down')
            self._c.publish(self._config['outtopic-down'], 'down')
            self._c.publish(self._config['outtopic-status'], 'stop')
            self._mode = 'stop'
            return

        if message == 'up':
            self._timeleft = self._intervalup
            self._c.publish(self._config['outtopic-down'], 'down')
            self._c.publish(self._config['outtopic-up'], 'up')
            self._c.publish(self._config['outtopic-status'], 'up')
            self._mode = 'up'
            return

        if message == 'down':
            self._timeleft = self._intervaldown
            self._c.publish(self._config['outtopic-up'], 'down')
            self._c.publish(self._config['outtopic-down'], 'up')
            self._c.publish(self._config['outtopic-status'], 'down')
            self._mode = 'down'
            return

        if message == 'stop':
            self._c.publish(self._config['outtopic-up'], 'down')
            self._c.publish(self._config['outtopic-down'], 'down')
            self._c.publish(self._config['outtopic-status'], 'stop')
            self._mode = 'stop'
            return

        if message == 'status':
            self._c.publish(self._config['outtopic-status'], self._mode)
            return
