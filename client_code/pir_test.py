######## A home Surveillance system - PIR sensor test module #########
#
# Author: Bonian Hu
# Date: 2021/04/08
# Description:
# This is the script running Raspberry Pi side to test PIR sensor.
# It will running the PIR sensor detection for 60 seconds, count the true and false.
# Finally returns the error rate.


import RPi.GPIO as GPIO
import time


# Initialize the GPIO pins
GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

# Initialize
count = 60
true_count = 0
false_count = 0

try:
    print ("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)
    print ("Ready")
    while count > 0:
        if GPIO.input(PIR_PIN):
            print ("Motion Detected!")
            true_count += 1
        else:
            print("motion not detected")
            false_count += 1
        time.sleep(1)
        count -= 1

    print("The count of high is {}".format(true_count))
    print("The count of low is {}".format(false_count))

    print("The error rate is {}".format(float(true_count)/float(true_count + false_count)))


except KeyboardInterrupt:
    print ("quit")
    GPIO.cleanup()
