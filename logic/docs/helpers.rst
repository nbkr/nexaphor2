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

TimedLightWithOnOff
-------------------
A TimedLightWithOnOff behaves mostly like a TimedLight. I.E. it will send 'up'
on it's *outtopic* if it receives an 'up' on it's *intopic*. After *interval*
number of seconds it will send out 'down'.

In difference to the TimedLight the TimedLightWithOnOff has a second intopic,
call *intopic-mode*.

There it accepts *on*, *off* and *timed*. If you send off to that topic the
light will turn off and stay off.

If you send 'on' it will turn on and stay on.

If you send 'timed' it will switch back to the normal behaviour of a TimedLight.

On *outtopic-mode* the helper will send out the current state of it is in
everytime it switched the state. If you send *current* to the intopic-mode the
helper won't change anything but will send out the current mode it is in (on,
off, timed)

Configexampe
````````````
..
    "timedlightonoff1": {
        "type": "lights.TimedLightWithOnOff", 
        "interval": 30
        "intopic": "tfin1/port2", 
        "intopic-mode": "modeswitchtimedlight1",
        "outtopic": "tfout1/port0/set",
        "outtopic-mode": "timedlight1mode"
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


Shutters
========

SimpleShutter
-------------
A SimpleShutter is meant for controlling shuttermotors. A shuttermotor has two
inputs for turning left/right or respectivly up and down. 

The SimpleShutter accepts *up*, *down* and *stop* via it's *intopic*. stop means
it sends 'down' to both of it's outtopics. 

up results in sending a 'down' to outtopic-down and up to outtopic-up. 

down is the same, but with reversed outtopics.

SimpleShutter will send 'down' to both outtopics if it currently moved the motor
'up' after 'interval-up'.

It will send 'down' to both outtopics if it currentlich moved the motor 'down'
after 'interval-down'.

Configexampe
````````````
..
    "shutter1": {
        "type": "shutters.SimpleShutter", 
        "intopic": "shutter1",
        "outtopic-up": "tfout1/port0",
        "outtopic-down": "tfout1/port1",
        "interval-up": 30,
        "interval-down": 30
    }


Misc
====

Impulsegiver
------------

An Impulsegiver waits for an *up* on it's intopic and then sends out an *up*
followed by a *down* after *interval* number of milliseconds

If the Impulsegiver get's another *up* while the interval is running, it will be
ignored.

Configexampe
````````````
..
    "dooropener1": {
        "type": "misc.Impulsegiver", 
        "intopic": "door1",
        "outtopic": "tfout2/port3/set",
        "interval": "500",
    }

Translators
===========

SimpleTranslator
----------------
A simple signal translator will every signal that it get's via its *intopic*
forward to it's *outtopic*. If the incoming signal matched any of the left sides
of *translations* it will be translated to the approprate right side of
*translataions*.

Configexampe
````````````
..
    "translator1": {
        "type": "translators.SimpleTranslator", 
        "intopic": "tfnfc1",
        "outtopic": "door1",
        "translations": {
            "1234": "up"
            "xyza": "down"
            "abc": "timed"
        }
    }

System
======

CommandRunner
----------------
A CommandRunner runs it's *command* everytime it get's an *up* on it's intopic.

Configexampe
````````````
..
    "doorbell": {
        "type": "system.CommandRunner", 
        "intopic": "doorbell",
        "command": "/usr/bin/mpg321 /etc/nexaphor2/logic/klingel.mp3"
    }
