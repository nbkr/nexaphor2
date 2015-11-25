.. vim: set tw=80 :

#######
Helpers
#######

I'm probably going to rename 'helpers' once I figured a better name for them.
But for now I will describe what they do.

Lights
======

Light
-----
A light will listen to topics specified with *intopic*. It it receives the
message *up* or *down* via that topic it will forward it via the topic
*outtopic*.

A usage scenario would be to directly connect a Tinkerforge Input to an
Tinkerforge Output. Everytime the input goes 'up', the logic will turn the
output 'up'. And of course the same applies for 'down'.

Configexampe
````````````
..
    "light1": {
        "type": "lights.Light", 
        "intopic": "tfin1/port2", 
        "outtopic": "tfout1/port0/set"
    }


TimedLight
----------
A TimedLight switches an output on and after *interval* number of seconds it
will shut it down again. It does so by sending out *up* or *down* via it's
*outtopic*.

It will only react to *up* messages coming in via *intopic*. If it receives
another *up* while the light is still switched on, it will reset the number of
seconds after which the *down* message is send out back to *interval*.

Configexampe
````````````
..
    "timedlight1": {
        "type": "lights.TimedLight", 
        "interval": 30
        "intopic": "tfin1/port2", 
        "outtopic": "tfout1/port0/set"
    }


Forwarders
==========

AtDay
-----
A AtDay-Forwarder will forward any message it receives via it's *intopic* by
it's *outtopic* as long as the sun is up.

Based on the longitude and latitude given in the configuration it will calculate
wether or not the sun is currently up at that location.

Configexampe
````````````
..
    "daylightforwarder": {
        "type": "forwarders.AtDay", 
        "latitude": "50.0",
        "longitude": "9.3",
        "intopic": "tfin1/port2", 
        "outtopic": "daylight"
    }

AtNight
-------
A AtNight-Forwarder will forward any message it receives via it's *intopic* by
it's *outtopic* as long as the sun is down.

Based on the longitude and latitude given in the configuration it will calculate
wether or not the sun is currently up at that location.

Configexampe
````````````
..
    "nighttimeforwarder": {
        "type": "forwarders.AtNight", 
        "latitude": "50.0",
        "longitude": "9.3",
        "intopic": "tfin1/port2", 
        "outtopic": "nighttime"
    }


Plexers
=======

Multiplexer
-----------
A Multiplexer listens to multiple intopics and forwards all of the messages
to a single outtopic.

Configexampe
````````````
..
    "multiplexer1": {
        "type": "plexer.Multi", 
        "intopic": ["tfin1/port0", 
                    "tfin1/port1",
                    "tfin1/port2"]
        "outtopic": "multi1"
    }

Demultiplexer
-------------
A Demultiplexer listens to one intopic and forwards all messages to multiple
outtopics.

Configexampe
````````````
..
    "demultiplexer1": {
        "type": "plexer.Demulti", 
        "intopic": "tfin1/port0",
        "outtopic": ["tfout1/port0",
                     "tfout1/port1"]
    }
