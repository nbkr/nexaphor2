from helpers import Helper
import logging


class Multi(Helper):

    def _subscribe(self):
        for it in self._config['intopic']:
            self._logger.debug(
                'Subscribing to topic "{}" by helper "{}"'.format(
                    it,
                    self._name))

            self._c.subscribe(self, self._name, it)

    def message(self, topic, message):
        self._logger.debug(
            'I ({}) recevied the message "{}" on "{}" and will forward it to my outtopic'.format(
                self._name,
                message,
                topic))
        self._c.publish(self._config['outtopic'], message)


class Demulti(Helper):

    def message(self, topic, message):
        self._logger.debug(
            'I ({}) recevied the message "{}" and will forward it to all my outtopics'.format(
                self._name,
                message))
        for ot in self._config['outtopic']:
            self._c.publish(ot, message)
