.. vim: set tw=80 :

#########
Nexaphor2
#########

My Home Automation System based on Tinkerforge, MQTT, a bit of Javascript, a bit
more of Python and a Raspberry Pi (2 works, 3 and up is better)

I've upgraded the project to Python3, fixed some code, and changed the part on how to create the 'custom' logic to the installation. This version of the software is therefore outdated and the repository therefore archived.


Setup
=====

Install nginx, tinkerforge, nodejs, npm, pip, mosquitto on your raspberry.

Run::
    apt-get install nginx git mosquitto python-dateutil python-ephem python-paho-mqtt python-pip python-yaml python3-paho-mqtt python3-pip supervisor
    pip install tinkerforge
    pip3 install eventlet flask-socketio flask-mqtt flask-bootstrap

    mkdir -p /etc/nexaphor2/{tinkerforge,web,logic}
    mkdir -p /etc/nexaphor2/web/{frontend,backend}

Copy the repository to /opt/nexaphor2

Create the configuration symlinks::

    cd /opt/nexaphor2/tinkerforge
    ln -s /etc/nexaphor2/tinkerforge/tfdata.yaml

    cd /opt/nexaphor2/logic
    ln -s /etc/nexaphor2/logic/logicdata.json
    
    cd /opt/nexaphor2/web/backend
    ln -s /etc/nexaphor2/web/backend/forwardings.txt
    ln -s /etc/nexaphor2/web/backend/subscribtions.txt

    cd /opt/nexaphor2/web/frontend
    ln -s /etc/nexaphor2/web/frontend/frontendconfig.json


Create the Supervisor Configuration::

    [program:nexaphor-tf]
    user=pi
    command=/usr/bin/python tfcontroller.py
    autostart=true
    directory=/opt/nexaphor2/tinkerforge

    [program:nexaphor-web]
    user=root
    command=/usr/bin/python3 bugfixer.py
    autostart=true
    directory=/opt/nexaphor2/web/backend

    [program:nexaphor-logic]
    user=pi
    command=/usr/bin/python logiccontroller.py
    autostart=true
    directory=/opt/nexaphor2/logic

Configure Nginx::

	root /opt/nexaphor2/web/frontend;

    [...]

	location /socket.io {
	    proxy_set_header Host $host;
	    proxy_set_header X-Real-IP $remote_addr;
	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

	    proxy_http_version 1.1;
	    proxy_buffering off;
	    proxy_set_header Upgrade $http_upgrade;
	    proxy_set_header Connection "Upgrade";
	    proxy_pass http://localhost:8080/socket.io;
	}

Create the configuration at /etc/nexaphor2 (see .dist files)

Start the services.
