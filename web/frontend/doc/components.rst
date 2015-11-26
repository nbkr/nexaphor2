.. vim: set tw=80 :

##########
Components
##########

Each page has a list of components that will get rendered on it. There are
serveral components that differ in behaviour.

Buttons
=======

Upbutton
--------
An Upbutton will simply send an *up* to it's *outtopic* everytime you click it.

Configexample
`````````````
{ 
    'type': 'upbutton',
    'outtopic': 'door1',
    'label': 'Haustür'
}
