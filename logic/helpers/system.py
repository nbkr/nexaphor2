import logging
from helpers import Helper
import subprocess


class CommandRunner(Helper):

    def message(self, topic, message):
        if message == 'up':
            subprocess.Popen(self._config['command'], shell=True)
