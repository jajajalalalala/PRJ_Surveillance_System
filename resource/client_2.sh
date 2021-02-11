#!/bin/sh
# if virtualenvwrapper.sh is in your PATH (i.e. installed with pip)
#source /path/to/virtualenvwrapper.sh # if it's not in your PATH
source /usr/local/bin/virtualenvwrapper.sh
workon prj_client
python /home/pi/PRJ/Client/camera_client_2.py
deactivate
