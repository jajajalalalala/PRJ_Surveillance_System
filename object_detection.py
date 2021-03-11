import numpy as np
from tensorflow.lite.python.interpreter import Interpreter
import os
import cv2


# This is to detect the human
class Human_Detector:

    def __init__(self):
        self.MODEL = 'models/tensorflow_models'
        self.LABEL = 'models/tensorflow_models/labelmap.txt'

        self.min_conf_threshold = 0.6

        self.imW, self.imH = 300, 300
        # Get path to current working directory
        self.CWD_PATH = os.getcwd()

        # Path to .tflite file, which contains the model that is used for object detection
        self.PATH_TO_CKPT = os.path.join(self.CWD_PATH, self.MODEL, 'detect.tflite')

        # Path to label map file
        PATH_TO_LABELS = os.path.join(self.CWD_PATH, self.MODEL, self.LABEL)

        # Load the label map
        with open(self.LABEL, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        # Load the Tensorflow Lite model.
        self.interpreter = Interpreter(model_path=self.PATH_TO_CKPT)
        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

        floating_model = (self.input_details[0]['dtype'] == np.float32)

    def detect(self, frame):
        # Tensorflow model
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
        input_data = np.expand_dims(frame_resized, axis=0)
        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        # Retrieve detection results
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[
            0]  # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # Class index of detected objects
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]  # Confidence of detected objects

        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        human_count = 0
        # Tensorflow motion detection
        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if (scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0):
                object_name = self.labels[
                    int(classes[i])]  # Look up object name from "labels" array using class index

                label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                if object_name == 'person':
                    human_count += 1
                    # Get bounding box coordinates and draw box Interpreter can return coordinates that are outside
                    # of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1, (boxes[i][0] * self.imH)))
                    xmin = int(max(1, (boxes[i][1] * self.imW)))
                    ymax = int(min(self.imH, (boxes[i][2] * self.imH)))
                    xmax = int(min(self.imW, (boxes[i][3] * self.imW)))

                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 1)

                    # Draw label

                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(ymin,
                                     labelSize[1] + 10)  # Make sure not to draw label too close to top of window

                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0),
                                1)  # Draw label text

        return frame, human_count
