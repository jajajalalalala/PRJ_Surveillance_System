#!/bin/sh
# Call the bash script on the raspberry Pi site
source /usr/local/bin/virtualenvwrapper.sh
workon prj_client
python3 /home/pi/PRJ/Client/camera_client_2.py
deactivate
