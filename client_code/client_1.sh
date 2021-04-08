#!/bin/sh
# Call the bash script on the raspberry Pi site,
# where /home/pi/PRJ/Client/camera_client_1.py is the directory
# of python script.

source /home/pi/.local/bin/virtualenvwrapper.sh
workon prj_client
python3 /home/pi/PRJ/Client/camera_client_1.py &
deactivate