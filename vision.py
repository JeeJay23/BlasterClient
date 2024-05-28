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
from Configuration import Configuration

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vision():
    def __init__(self, config : Configuration):

        self.scaling = config.camera_scaling
        self.camera_width = config.camera_width * self.scaling
        self.camera_height = config.camera_height * self.scaling
        self.hitbox_size = config.camera_hitbox_size

        # TODO inject this camera through an abstraction
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size = (self.camera_width, self.camera_height)
        self.cam.preview_configuration.main.format = config.camera_color_format
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()
        self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        print('Vision: initialized camera')

        # Vision settings
        self.model_path = config.vision_model_path
        self.label_path = config.vision_label_path
        self.confidence_treshold = config.vision_confidence_treshold

        self.interpreter = Vision.load_model(self.model_path)
        self.labels = Vision.load_labels(self.label_path)
        self.allowed_labels = config.vision_allowed_labels
        print('Vision: initialized interpreter')

        input_details = self.interpreter.get_input_details()
        input_shape = input_details[0]['shape']

        self.model_height = input_shape[1]
        self.model_width = input_shape[2]
        self.input_index = input_details[0]['index']

    def load_labels(label_path : str):
        r"""Returns a list of labels"""
        with open(label_path) as f:
            labels = {}
            for line in f.readlines():
                m = re.match(r"(\d+)\s+(\w+)", line.strip())
                labels[int(m.group(1))] = m.group(2)
            return labels

    def load_model(model_path : str):
        r"""Load TFLite model, returns a Interpreter instance."""
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        print(f"Vision: initialized interpreter with model {model_path}")
        return interpreter

    def process_image(self, image):
        r"""Process an image, Return a list of detected class ids and positions"""
        input_data = np.expand_dims(image, axis=0)  # expand to 4-dim

        # Process
        self.interpreter.set_tensor(self.input_index, input_data)
        self.interpreter.invoke()

        # Get outputs
        output_details = self.interpreter.get_output_details()
        positions = np.squeeze(self.interpreter.get_tensor(output_details[0]['index']))
        classes = np.squeeze(self.interpreter.get_tensor(output_details[1]['index']))
        scores = np.squeeze(self.interpreter.get_tensor(output_details[2]['index']))

        results = []

        for idx, score in enumerate(scores):
            if score > self.confidence_treshold:
                results.append({'pos': positions[idx], 'id': classes[idx]})
        return results

    def isInCenterBox(self, image, p1 : Point, p2 : Point) -> bool:

        midPoint = Point(
            image.shape[0]/2,
            image.shape[1]/2
        )

        a1 = Point(
            midPoint.x - self.hitbox_size,
            midPoint.y - self.hitbox_size
        )

        a2 = Point(
            midPoint.x + self.hitbox_size,
            midPoint.y + self.hitbox_size
        )

        return (p1.x < a2.x and p2.x > a1.x) and (p1.y < a2.y and p2.y > a1.y)

    # TODO run this on a seperate thread (with callback)
    def checkForHuman(self) -> tuple[bool, str]:
        im = self.cam.capture_array()
        image=Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        image=image.resize((self.camera_width, self.camera_height))

        results = self.process_image(image)
        for obj in results:
            pos = obj['pos']
            y1 = int(pos[0] * self.camera_height)
            x1 = int(pos[1] * self.camera_width)
            y2 = int(pos[2] * self.camera_height)
            x2 = int(pos[3] * self.camera_width)

            hit = self.isInCenterBox(im, Point(x1, y1), Point(x2, y2))
            d=self.labels[obj['id']]
            if hit and (d in self.allowed_labels):
                return (True, d)
            else:
                return (False, " ")
        return (False, " ")

