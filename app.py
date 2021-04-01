# Obtained and improved from the following project
# https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking

from importlib import import_module
from flask import Flask, render_template, Response, jsonify
import cv2
import time
from client_init import Client
from datetime import datetime

import sys
import random

app = Flask(__name__)
# Initialize the 3 camera clients, the clients will start one after another.


client_list = [Client("192.168.0.172"), Client("192.168.0.145"), Client("192.168.0.144")]
for client in client_list:
    client.stop()
    client.start()


@app.route('/')
def index():
    """The dashboard of the video stream"""
    return render_template('index.html')


# Generate the video stream, device is the camera number video stream is used to get the frames
def gen(camera_stream, device):
    """
    Video streaming generator function.

    :param camera_stream: the stream of the camera
    :param device： camera id
    """
    total_time = 0
    while True:
        time_start = time.time()

        cam_id, frame = camera_stream.get_frame(device)
        if frame is None:
            break

        time_now = time.time()
        total_time += time_now - time_start

        # # write camera name
        cv2.putText(frame, cam_id, (int(20), int(20 * 5e-3 * frame.shape[1])), 0, 1.5e-3 * frame.shape[0],
                    (255, 255, 255), 1)

        frame = cv2.imencode('.jpg', frame)[1].tobytes()  # Remove this line for test camera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video/<device>')
def video(device):
    """Video streaming route. Put this in the src attribute of an img tag."""
    port_list = (5554, 5555, 5556)
    camera_stream = import_module('camera_server').Camera
    return Response(gen(camera_stream=camera_stream(device, port_list), device=device),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/get_start_time/<device>')
def get_start_time(device):
    """This is to get the start time of the device"""
    client = client_list[device]
    start_time = datetime.now() - client.start_time
    return start_time







if __name__ == '__main__':
    try:

        app.run(host='0.0.0.0', threaded=True)
    except KeyboardInterrupt:
        print("interrupt exit with key")

        sys.exit(0)
