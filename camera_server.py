# Based on the project
# https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking

from base_camera import BaseCamera
import time
import cv2
from lib_vibe.py_vibe import ViBe  #Library import from https://github.com/232525/ViBe.Cython.git
from notifier import RPI_Notifier
import time, threading
from PIL import Image
from object_detection import Human_Detector
import os

from database import Database

isAvailable = [True, True, True]


# Camera is the child of BaseCamera
class Camera(BaseCamera):

    def __init__(self, device, port_list):
        super(Camera, self).__init__(device, port_list)

    @staticmethod
    def server_frames(image_hub):
        """
        This method process the frame in the image_hub, and doing the motion detection using either VIBE algorithm or frame difference algorithm, object classification.

        If it detects the person, under a certain criteria, it will send the notification and add the record to a database.

        :param image_hub: the frame pool
        """

        num_frames = 0
        # Initialize the databese to store the record
        db = Database()
        # Let a availability thread sleep for 5 minutes before sending the next frame
        def changeAvailability(index):
            """
            Set the availablility in the "isAvaibable" to True after 30 seconds
            :param index: the index in the list
            """
            time.sleep(300)
            isAvailable[index] = True

        # Set the cooling time for a notification of a raspberry Pi.
        def cooler(index):
            """
            Control the freezing time of the notifier
            :param index: the index in the "isAvailable" list
            """
            global isAvailable
            if not isAvailable[index]:
                t = threading.Thread(target=changeAvailability, args=(index, ))
                t.start()


        def send_notification(id, frame):
            """
            This function is used to send the notification to user
            :param id: the camera id
            :param fram: the current frame
            """
            notifier = RPI_Notifier()
            cam_index = int(id[-1]) - 1
            if isAvailable[cam_index]:
                # if the parameter isAvailable is true, send notification.
                isAvailable[cam_index] = False
                cooler(cam_index)
                Image.fromarray(frame).save("input/frame.jpg")
                notifier.send_message("motion detected on camera {}".format(id), "input/frame.jpg")
                db.save_data(cam_id, time.strftime('%Y%m%d%h %H:%M'))  # Save this record to the database




        # # Initialize the Vibe Algorithm and collect the first image
        vibe = ViBe()
        cam_id, frame = image_hub.recv_image() #Get the recent image from image_hub
        image_hub.send_reply(b'OK')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if num_frames == 0:
            vibe.AllocInit(gray)
        background_segmentation_map = vibe.Segmentation(gray)  #When the new Vibe algorithem initialize its background.


        # Image difference motion detection
        # cam_id, old_frame = image_hub.recv_image()
        # image_hub.send_reply(b'OK')
        # new_frame = old_frame


        num_frames += 1

        # Create a human detector class
        human_detector = Human_Detector()

        # Define the number of rectangle for human detection
        object_count = 0
        notifier = RPI_Notifier()

        # Define the time check point
        check_point = time.time()


        while True:  # main loop
            cam_id, frame = image_hub.recv_image()
            image_hub.send_reply(b'OK')

            #############################
            # Frame Difference Algorithm
            #############################
            # new_frame = frame
            #
            #
            # frame_difference = cv2.absdiff(old_frame, new_frame)
            #
            # frame_gray = cv2.cvtColor(frame_difference, cv2.COLOR_BGR2GRAY)
            #
            # frame_blur = cv2.GaussianBlur(frame_gray, (21, 21), 0)
            # _, threshold = cv2.threshold(frame_blur, 20, 255, cv2.THRESH_BINARY)
            # frame_dilated = cv2.dilate(threshold, None, iterations=3)
            # frame_contours, _ = cv2.findContours(frame_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # # Calculate the area of contours, if smaller than threshold, continue
            #
            # #Calculate the total contour area
            #
            # for i in frame_contours:
            #     if cv2.contourArea(i) < 2000:
            #         continue
            #     else:
            #
            #         # If the contour area is greater than threashold, do the classification
            #         frame, count = human_detector.detect(frame)
            #         object_count += count
            #         if object_count > 2:
            #             object_count = 0
            #             if time.time() - check_point < 1:

            #                 send_notification(cam_id, frame)
            #             check_point = time.time()
            #
            # print(frame_contours)
            #
            # frame = frame_dilated
            # num_frames += 1
            # old_frame = new_frame



            #############################
            # Normal Vibe algorithm
            #############################

            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # segmentation_map = vibe.Segmentation(gray)
            # vibe.Update(gray, segmentation_map)
            # #Define the threshold for pure vibe
            # vibe_sum = sum([sum(i) for i in segmentation_map]) / 10000
            #
            # cam_index = int(cam_id[-1]) - 1
            # # If the sum is too large, the position of the camera might changed, stop detecting
            # if vibe_sum > 800 and isAvailable[cam_index] == True:
            #
            #     notifier.send_text("The position of the camera {} might be altered, please check <a href='http://192.168.0.143:5000'>here</a>.".format(cam_id))
            #
            #     isAvailable[cam_index] = False
            #     cooler(cam_index) #Start the cooling after a notification is sent
            #
            #
            # # detect then motion is greater than the threshold 100
            # elif vibe_sum > 100:
            # # If the contour area is greater than threashold, do the classification
            #     frame, count = human_detector.detect(frame)
            #     object_count += count
            #     # If a object consistently appears in the stream, then send the notification
            #     if object_count > 1:
            #         object_count = 0
            #         if time.time() - check_point < 1:
            #             send_notification(cam_id, frame)    # Send the frame to telegram
            #         check_point = time.time()
            # frame = segmentation_map
            # num_frames += 1


            #############################
            # The New algorithm for the Vibe motion detection
            # Will remove the frame quicker
            #############################
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            segmentation_map = vibe.Segmentation(gray)

            vibe.Update(gray, background_segmentation_map)

            vibe_sum = sum([sum(i) for i in segmentation_map]) / 10000

            cam_index = int(cam_id[-1]) - 1
            # If the sum is too large, the position of the camera might changed, stop detecting
            if vibe_sum > 800 and isAvailable[cam_index] == True:

                notifier.send_text(
                    "The position of the camera {} might be altered, please check <a href='http://192.168.0.143:5000'>here</a>.".format(
                        cam_id))

                isAvailable[cam_index] = False
                cooler(cam_index)  # Start the cooling after a notification is sent


            # detect then motion is greater than the threshold 100
            elif vibe_sum > 15:
                # If the contour area is greater than threashold, do the classification
                frame, count = human_detector.detect(frame)
                object_count += count
                # If a object consistently appears in the stream, then send the notification
                if object_count > 0:
                    object_count = 0
                    if time.time() - check_point < 1:
                        send_notification(cam_id, frame)  # Send the frame to telegram
                    check_point = time.time()
            print(vibe_sum)
            frame = segmentation_map
            num_frames += 1
            yield cam_id, frame


