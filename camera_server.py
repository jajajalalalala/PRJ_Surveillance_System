# inspired by https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking
from base_camera import BaseCamera
import time
import cv2
from lib_vibe.py_vibe import ViBe
from notifier import RPI_Notifier
import time, threading
from PIL import Image
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter
from object_detection import Human_Detector
import os

isAvailable = [True, True, True]


# Camera is the child of BaseCamera
class Camera(BaseCamera):

    def __init__(self, device, port_list):
        super(Camera, self).__init__(device, port_list)

    @staticmethod
    def server_frames(image_hub):
        num_frames = 0

        # Let a availability thread sleep for 5 minutes before sending the next frame
        def changeAvailability(i):
            time.sleep(30)
            isAvailable[i] = True

        # Set the cooling time for a camera
        def cooler(index):
            global isAvailable
            if not isAvailable[index]:
                t = threading.Thread(target=changeAvailability, args=(index,))
                t.start()

        # Function to send the notification
        def send_notification(id, frame):
            notifier = RPI_Notifier()
            cam_index = int(id[-1]) - 1
            if isAvailable[cam_index]:
                # if the parameter isAvailable is true, send notification.
                isAvailable[cam_index] = False
                cooler(cam_index)
                Image.fromarray(frame).save("input/frame.jpg")
                notifier.send_message("motion detected on camera {}".format(id), "input/frame.jpg")

        # cam_id, old_frame = image_hub.recv_image()
        # image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern
        #
        # cam_id, new_frame = image_hub.recv_image()
        # image_hub.send_reply(b'OK')

        # Initialize the Vibe Algorithm and collect the first image
        vibe = ViBe()
        cam_id, frame = image_hub.recv_image()
        image_hub.send_reply(b'OK')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        unique_frame = gray, num_frames
        if num_frames == 0:
            vibe.AllocInit(gray)

        old_segmentation_map = vibe.Segmentation(gray)
        num_frames += 1

        # Create a human detector class
        human_detector = Human_Detector()

        # Define the number of rectangle for human detection
        object_count = 0

        notifier = RPI_Notifier()

        # Define the check point
        check_point = time.time()
        while True:  # main loop
            cam_id, frame = image_hub.recv_image()
            image_hub.send_reply(b'OK')

            # Algorithm for motion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            new_segmentation_map = vibe.Segmentation(gray)
            difference = cv2.absdiff(old_segmentation_map, new_segmentation_map)
            old_segmentation_map = new_segmentation_map
            vibe.Update(gray, old_segmentation_map)
            blur = cv2.GaussianBlur(difference, (21, 21), 0)
            _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(threshold, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
            pick = []

            # Calculate the area of contours, if smaller than threshold, continue
            for i in contours:
                if cv2.contourArea(i) < 1000:
                    continue
                else:

                    # If the contour area is greater than threashold, do the classification
                    frame, count = human_detector.detect(frame)
                    object_count += count
                    if object_count > 2:
                        object_count = 0
                        if time.time() - check_point < 1:
                            send_notification(cam_id, frame)
                        check_point = time.time()
            num_frames += 1

            yield cam_id, frame

            # (x, y, z, v) = cv2.boundingRect(i)
            # #Draw the contours on each
            # cv2.rectangle(frame, (x, y), (x + z, y + v), (0, 255, 0), 2)

            # Human detection
            # (rects, weights) = hog.detectMultiScale(
            #     frame, winStride=(4, 4), padding=(8, 8), scale=1.05
            # )
            # pick = non_max_suppression(rects, probs=1, overlapThresh=0.15)

            #
            # for (xA, yA, xB, yB) in pick:
            #     cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            # if len(pick) >0:
            #     send_notification(cam_id, frame)

            # input = Image.fromarray(frame, "RGB").save("input/frame.jpg")
            #
            # #     Draw  classified image
            # detections = detector.detectObjectsFromImage(input_image=frame, output_image_path=output_path)
            #
            # output_image = Image.open("output/newimage.jpg")
            #
            # image_sequence = output_image.getdata()
            # frame = np.array(image_sequence)

            # Adding motion detection

            # Uncomment to disable background different motion detection
            #
            # difference = cv2.absdiff(old_frame, new_frame)
            # gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
            # blur = cv2.GaussianBlur(gray,(21,21), 0)
            # _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            #
            # dilated = cv2.dilate(threshold, None, iterations=3)
            # contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # # cv2.putText(old_frame, cam_id, (int(20), int(20 * 5e-3 * old_frame.shape[1])), 0,
            # #             1.5e-3 * old_frame.shape[0],
            # #             (255, 255, 255), 1)
            # # print(dilated)
            # for i in contours:
            #     (x, y, z, v) = cv2.boundingRect(i)
            #
            #     if cv2.contourArea(i) < 900:
            #         continue
            #     (x, y, z, v) = cv2.boundingRect(i)
            #     cv2.rectangle(old_frame, (x, y), (x + z, y + v), (0, 255, 0), 2)
            #     # cv2.putText(old_frame, "Status: {}".format("Movement"),(int(20), int(10 * 5e-3 * old_frame.shape[0])), 0,
            #     #         1.5e-3 * old_frame.shape[0],
            #     #         (255, 255, 255), 1)
            #
            # # cv2.putText(old_frame, "Room Status: {}".format(is_motion), (10, 20),
            # #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # # cv2.putText(old_frame, "Motion detected: {}".format(is_motion),
            # #             (int(20), int(10 * 5e-3 * old_frame.shape[0])), 0,
            # #             1.5e-3 * old_frame.shape[0],
            # #             (255, 255, 255), 1)
            #
            # old_frame = new_frame
            # cam_id, new_frame = image_hub.recv_image()
            # image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern
            # num_frames += 1

            # Uncomment to start without motion detection
            # cam_id, result= image_hub.recv_image()
            # image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern
            #
            # num_frames += 1
            #
            # time_now = time.time()
            # total_time += time_now - time_start
            # fps = num_frames / total_time

            # If the sum of contour meet the threshold, send the notification
            # if sum([cv2.contourArea(i) for i in contours]) > 3000:
            #     send_notification(cam_id, frame)
            # num_frames += 1
