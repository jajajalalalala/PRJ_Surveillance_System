######## A home Surveillance system - Client-site script#########
#
# Author: Bonian Hu
# Date: 2021/04/08
# Description:
# The client 2 code that send the frame to server using imagezmq library.
# The PIR sensor code is also showed up, but they are commented as the sensor does not working properly.

# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import socket
import time
import imutils
# import RPi.GPIO as GPIO


# GPIO.setmode(GPIO.BCM)
# PIR_PIN = 4
# GPIO.setup(PIR_PIN, GPIO.IN)

sender = imagezmq.ImageSender(connect_to='tcp://192.168.0.143:5555')

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

while True:
    # GPIO.setup(4, GPIO.OUT)
    # if GPIO.input(PIR_PIN):
    #     print("Motion detected")
        # read the frame from the camera and send it to the server
    frame = vs.read()