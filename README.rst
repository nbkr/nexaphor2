.. vim: set tw=80 :

#########
Nexaphor2
#########

My Home Automation System based on Tinkerforge, MQTT, a bit of Javascript, a bit
more of Python and a Raspberry Pi.

Setup
=====

Install nginx, tinkerforge, nodejs, npm, pip, mosquitto on your raspberry.

Run::
    apt-get install nginx supervisor python-pip
    pip install tinkerforge
    pip install ephem

    # Install nodejs from it's binary distribution, don't use the version
    # that comes with raspbian it seems to old.

    npm install socket.io
    npm install mqtt
     
    wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
    apt-key add mosquitto-repo.gpg.key
    cd /etc/apt/sources.list.d/
    wget http://repo.mosquitto.org/debian/mosquitto-wheezy.list
    apt-get update
    apt-get install mosquitto

    mkdir -p /etc/nexaphor2/{tinkerforge,web,logic}
    mkdir -p /etc/nexaphor2/web/{frontend,backend}

Copy the repository to /opt/nexaphor2

Create the configuration symlinks::

    cd /opt/nexaphor2/tinkerforge
    ln -s /etc/nexaphor2/tinkerforge/tfdata.json

    cd /opt/nexaphor2/logic
    ln -s /etc/nexaphor2/logic/logicdata.json
    
    cd /opt/nexaphor2/web/backend
    ln -s /etc/nexaphor2/web/backend/forwardings.txt
    ln -s /etc/nexaphor2/web/backend/subscribtions.txt

    cd /opt/nexaphor2/web/frontend
    ln -s /etc/nexaphor2/web/frontend/frontendconfig.json


Create the Supervisor Configuration

Start the services
