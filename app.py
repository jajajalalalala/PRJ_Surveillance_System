######## A home Surveillance system - App.py Module.#########
#
# Author: Bonian Hu
# Date: 2021/04/08
# Description:
# This class defines the flask constructor and the method to retrive the latest frame
# from the thread.
# This code is based on the python Flask tutorial and the following example.
# https://flask.palletsprojects.com/en/1.1.x/tutorial/
# https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking
# I simplified the code and specificly client port list for this project.


from flask import Flask, render_template, Response
import cv2
from client_init import Client
from camera_server import  Camera
import sys

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
    Improved from: https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking
    """
    while True:
        cam_id, frame = camera_stream.get_frame(device)
        if frame is None:
            break
        # write camera name
        cv2.putText(frame, cam_id, (int(20), int(20 * 5e-3 * frame.shape[1])), 0, 1.5e-3 * frame.shape[0],
                    (0, 255, 255), 1)
        # Get the frame
        frame = cv2.imencode('.jpg', frame)[1].tobytes()


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video/<device>')
def video(device):
    """
    Video streaming route. Put this in the src attribute of an img tag.
    Improved from: https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking
    """

    # Create port list for each raspberry pi
    port_list = (5554, 5555, 5556)

    # Create the camera threads
    camera_threads = Camera(device, port_list)
    # Create the frame generator
    frame_generator = gen(camera_threads, device)
    return Response(frame_generator,
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        print("Exit with the key")

        sys.exit(0)
