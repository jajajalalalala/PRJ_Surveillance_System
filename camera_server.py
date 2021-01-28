#inspired by https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking
from base_camera import BaseCamera
import time
import cv2


#Camera is the child of BaseCamera
class Camera(BaseCamera):

    def __init__(self, feed_type, device, port_list):
        super(Camera, self).__init__(feed_type, device, port_list)

    @staticmethod
    def server_frames(image_hub):
        num_frames = 0
        total_time = 0


        cam_id, old_frame = image_hub.recv_image()
        image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern

        cam_id, new_frame = image_hub.recv_image()
        image_hub.send_reply(b'OK')



        while True:  # main loop
            time_start = time.time()


            #Adding motion detection

            #Uncomment to disable motion detection

            difference = cv2.absdiff(old_frame, new_frame)
            gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5), 0)



            _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)



            dilated = cv2.dilate(threshold, None, iterations=3)

            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            cv2.drawContours(old_frame, contours, -1, (0,255,0), 2)

            result = old_frame
            old_frame = new_frame
            cam_id, new_frame = image_hub.recv_image()
            image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern
            num_frames += 1


            # Uncomment to start without motion detection
            # cam_id, result= image_hub.recv_image()
            # image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern
            #
            # num_frames += 1
            #
            # time_now = time.time()
            # total_time += time_now - time_start
            # fps = num_frames / total_time

            yield cam_id, result