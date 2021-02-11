#!/bin/sh
# if virtualenvwrapper.sh is in your PATH (i.e. installed with pip)
#source /path/to/virtualenvwrapper.sh # if it's not in your PATH
source /home/pi/.local/bin/virtualenvwrapper.sh
workon prj_client
python /home/pi/PRJ/Client/camera_client_3.py
deactivate