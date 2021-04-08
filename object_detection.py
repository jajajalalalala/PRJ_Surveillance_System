######## A home Surveillance system - Human Classification module #########
#
# Author: Bonian Hu
# Date: 2021/04/08
# Description:
# This class use the Tensorflow object detection model to classify the image in a frame.
# It accepts a frame from the image hub if the frame satisfies the requirement and send the
# frame with drawed boxes back to the server
#
# This code is based off and improved from the TensorFlow Lite image classification example at:
# https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/TFLite_detection_stream.py
#
# I added my own script logic to let the system only detect human object. It will return a classified object to the server.


import numpy as np
from tensorflow.lite.python.interpreter import Interpreter
import os
import cv2





# This is the class to detect the human
class Human_Detector:

    def __init__(self):

        #  Define the threshold of the classifier
        self.min_threshold = 0.65
        # Configure image width and height
        self.imW, self.imH = 300, 300

        # Load the label map from the directory
        label_file = 'models/tensorflow_models/labelmap.txt'
        self.label_list = []
        with open(label_file, 'r') as label_map:
            for i in label_map.read().split("\n"):
                self.label_list.append(i)


        # Load the tensorflow models
        self.interpreter = Interpreter(model_path='models/tensorflow_models/detect.tflite')
        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]



    # Human detection method
    def detect(self, frame):
        # Tensorflow model
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
        input_data = np.expand_dims(frame_resized, axis=0)
        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        # get the detection results

        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # get the index of detect object
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]  # the score of this classification

        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        human_count = 0
        # Tensorflow motion detection
        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if (scores[i] > self.min_threshold) and (scores[i] <= 1.0):
                object_name = self.label_list[
                    int(classes[i])]  # Look up object name from "labels" array using class index
                # Define the model name
                label = '%s: %d%%' % (object_name, int(scores[i] * 100))
                # If the objectt equals human, the count + 1
                if object_name == 'person':
                    human_count += 1
                    rectangle = self.interpreter.get_tensor(self.output_details[0]['index'])[
                        0]  # get the box around this obejct
                    # Define the position of the box
                    ymin = int(max(1, (rectangle[i][0] * self.imH)))
                    xmin = int(max(1, (rectangle[i][1] * self.imW)))
                    ymax = int(min(self.imH, (rectangle[i][2] * self.imH)))
                    xmax = int(min(self.imW, (rectangle[i][3] * self.imW)))

                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 1)
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                    # Draw label on the frame
                    cv2.putText(frame, label, (xmin, label_ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0),
                                1)  # Draw label text

        return frame, human_count
