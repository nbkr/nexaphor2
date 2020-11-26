#! /usr/bin/env python3

# For whatever reasons, the flask-mqtt client will only connect to the mosquitto server if the latter has
# been restarted after flask-mqtt has been started. 
#
# I found something about this here:
#   https://stackoverflow.com/questions/61794148/mqtt-client-only-connecting-after-restarting-broker
#   https://stackoverflow.com/questions/62213258/flask-mqtt-disconnects-after-socket-error-on-client-unknown-while-running-on
#
# yet I couldn't solve it. So now I will use this, I will start the server.py, wait 30 seconds and restart mosquitto.
# That seems to do the trick.
#
# It's not stupid if it works!
#
# Ok, it is stupid.
#
# But it works.

import subprocess
import time

p1 = subprocess.Popen('/usr/bin/sudo -u pi /usr/bin/python3 server.py', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

time.sleep(30)

subprocess.Popen('/bin/systemctl restart mosquitto', shell=True)

# I now can communication with the server again. This way it supervisorctl can stop it, hopefully.
p1.communicate()
