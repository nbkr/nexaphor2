#! /usr/bin/env python

import logging
from controller import Controller
import yaml


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s', level=logging.DEBUG)
    logging.info('Reading configuration')

    with open('logicdata.yml') as data_file:    
        objects = yaml.load(data_file)

    controller = Controller();

    for o in objects:
        controller.registerLogic(o[:], objects[o])

    try:
        controller.start()
    except KeyboardInterrupt:
        logging.info("Stopping")
        controller.shutdown()
    except Exception, msg:
        logging.debug(msg)
