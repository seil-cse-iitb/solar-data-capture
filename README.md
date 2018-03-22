# Introduction
Solar data collection app creates wifi hotspot to which nodemcus connect and then we can download data from the nodes.

# Installation
* Install RaspAP by following https://howtoraspberrypi.com/create-a-wi-fi-hotspot-in-less-than-10-minutes-with-pi-raspberry/
* Install the node modules by running `npm install` inside the templates directory.

# Configuration
Change the `templates/js/config.js` with the IP of the hotspot. Ideally should not change

# Deploy
* Run `FLASK_APP=server.py flask run --host=0.0.0.0` from project root