import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
from libcamera import controls
from mqtt import MQTT
from gpiozero import Button

BUTTONPIN = 4
CHECK_FLAG = False
BROKER_ADDR = "172.20.10.6"
TOPIC = "test/hits"

class Vision():
    def __init__(self, config):
        # TODO move these settings to config object
        self.scaling = 1
        self.camera_width = 320 * self.scaling
        self.camera_height = 320 * self.scaling
        self.hitbox_size = 50

        # Camera settings
        # TODO inject this camera through an abstraction
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size = (self.camera_width, self.camera_height)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()
        self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})

        # Vision settings
        self.model_path = 'efficientdet_lite0.tflite'
        self.label_path = 'labels.txt'

        self.interpreter = Vision.load_model(self.model_path)
        self.labels = Vision.load_labels(self.label_path)

        input_details = self.interpreter.get_input_details()
        input_shape = input_details[0]['shape']

        self.model_height = input_shape[1]
        self.model_width = input_shape[2]
        self.input_index = input_details[0]['index']


    def load_labels(label_path):
        r"""Returns a list of labels"""
        with open(label_path) as f:
            labels = {}
            for line in f.readlines():
                m = re.match(r"(\d+)\s+(\w+)", line.strip())
                labels[int(m.group(1))] = m.group(2)
            return labels

    def load_model(model_path):
        r"""Load TFLite model, returns a Interpreter instance."""
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    def checkForHuman(self):
        pass
