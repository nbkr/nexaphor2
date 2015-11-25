from dateutil import tz
from helpers import Helper
import ephem
import datetime
import logging

class AtDay(Helper):
    def __init__(self, controller, name, config):
        super(AtDay, self).__init__(controller, name, config)
        self._logger = logging.getLogger('atday')
        self._longitude = config['longitude']
        self._latitude = config['latitude']
        self._elevation = int(config['elevation'])

    def message(self, topic, message):
        # Calculating if the sun is up.
        obs = ephem.Observer()
        obs.lat = self._latitude
        obs.long = self._longitude
        obs.elevation = self._elevation

        rutc = obs.previous_rising(ephem.Sun()).datetime()                              
        rutc = rutc.replace(tzinfo=tz.tzutc())                                          
        rlocal = rutc.astimezone(tz.tzlocal())                                          
                                                                                        
        sutc = obs.previous_setting(ephem.Sun()).datetime()                             
        sutc = sutc.replace(tzinfo=tz.tzutc())                                          
        slocal = sutc.astimezone(tz.tzlocal())

        if rlocal >= slocal:
            self._logger.debug(
                'The sun is UP, so I ({}) will forward "{}"'.format(
                    self._name,
                    message))
            self._c.publish(self._config['outtopic'], message)

        else:
            self._logger.debug(
                'The sun is DOWN, so I ({}) will NOT forward "{}"'.format(
                    self._name,
                    message))


class AtNight(Helper):
    def __init__(self, controller, name, config):
        super(AtNight, self).__init__(controller, name, config)
        self._logger = logging.getLogger('atnight')
        self._longitude = config['longitude']
        self._latitude = config['latitude']
        self._elevation = int(config['elevation'])

    def message(self, topic, message):
        # Calculating if the sun is up.
        obs = ephem.Observer()
        obs.lat = self._latitude
        obs.long = self._longitude
        obs.elevation = self._elevation

        rutc = obs.previous_rising(ephem.Sun()).datetime()                              
        rutc = rutc.replace(tzinfo=tz.tzutc())                                          
        rlocal = rutc.astimezone(tz.tzlocal())                                          
                                                                                        
        sutc = obs.previous_setting(ephem.Sun()).datetime()                             
        sutc = sutc.replace(tzinfo=tz.tzutc())                                          
        slocal = sutc.astimezone(tz.tzlocal())

        if rlocal < slocal:
        
            self._logger.debug(
                'The sun is DOWN, so I ({}) will forward "{}"'.format(
                    self._name,
                    message))
            self._c.publish(self._config['outtopic'], message)

        else:
            self._logger.debug(
                'The sun is UP, so I ({}) will NOT forward "{}"'.format(
                    self._name,
                    message))
