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
    "light1": {
        "type": "lights.TimedLight", 
        "interval": 30
        "intopic": "tfin1/port2", 
        "outtopic": "tfout1/port0/set"
    }
