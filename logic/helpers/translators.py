from helpers import Helper
import logging

class SimpleTranslator(Helper):

    def message(self, topic, message):
        outgoing = message

        if message in self._config['translations']:
            outgoing = self._config['translations'][message]

        self._c.publish(self._config['outtopic'], outgoing)
