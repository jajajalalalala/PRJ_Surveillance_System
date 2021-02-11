#inspired by https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking
from base_camera import BaseCamera
import time
import cv2
from lib_vibe.py_vibe import ViBe

#Camera is the child of BaseCamera
class Camera(BaseCamera):

    def __init__(self, device, port_list):
        super(Camera, self).__init__(device, port_list)



    @staticmethod
    def server_frames(image_hub):
        num_frames = 0
        total_time = 0
        vibe = ViBe()

        # cam_id, old_frame = image_hub.recv_image()
        # image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern
        #
        # cam_id, new_frame = image_hub.recv_image()
        # image_hub.send_reply(b'OK')

        #Initialize the Vibe background
        cam_id, frame = image_hub.recv_image()
        image_hub.send_reply(b'OK')
        time_start = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        unique_frame = gray, num_frames
        if num_frames == 0:
            vibe.AllocInit(gray)

        old_segmentation_map = vibe.Segmentation(gray)
        num_frames += 1


        while True:  # main loop

            #Uncomment to disable Vibe motion detection

            cam_id, frame = image_hub.recv_image()
            image_hub.send_reply(b'OK')
            time_start = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if num_frames == 0:
                vibe.AllocInit(gray)

            new_segmentation_map = vibe.Segmentation(gray)
            difference = cv2.absdiff(old_segmentation_map, new_segmentation_map)
            old_segmentation_map = new_segmentation_map
            vibe.Update(gray, old_segmentation_map)
            blur = cv2.GaussianBlur(difference, (21, 21), 0)


            _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(threshold, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            for i in contours:
                if cv2.contourArea(i) < 1000:
                        continue

                (x, y, z, v) = cv2.boundingRect(i)
                cv2.rectangle(frame, (x, y), (x + z, y + v), (0, 255, 0), 2)
            num_frames += 1



            #Adding motion detection

            #Uncomment to disable background different motion detection
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

            yield cam_id,  frame