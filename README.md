# Introduction
Solar data collection app creates wifi hotspot to which nodemcus connect and then we can download data from the nodes.

# Installation
* Install RaspAP by following https://howtoraspberrypi.com/create-a-wi-fi-hotspot-in-less-than-10-minutes-with-pi-raspberry/
* Install the node modules by running `npm install` inside the templates directory.

# Configuration
Change the `templates/js/config.js` with the IP of the hotspot. Ideally should not change

# Deploy
* Run `python3 server.py` from project root
* Sample PM2 startup script also present. Copy it to parent folder of project and run using `pm2 start processes.yml`

# Management
* To stop server `pm2 stop server`
* To restart server `pm2 restart server`
* To start server `pm2 start server`
* To view logs `pm2 logs`. Ctrl+C to quit



