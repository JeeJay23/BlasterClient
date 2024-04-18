import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
from libcamera import controls
import paho.mqtt.client as mqtt
from gpiozero import Button

BUTTONPIN = 4
CHECK_FLAG = False
BROKER_ADDR = "172.20.10.6"
TOPIC = "test/hits"
SCALING = 1
HITBOX_SIZE = 50
CAMERA_WIDTH = 320 * SCALING
CAMERA_HEIGHT = 320 * SCALING

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (CAMERA_WIDTH,CAMERA_HEIGHT)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

def on_press():
    global CHECK_FLAG
    CHECK_FLAG = True

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


def process_image(interpreter, image, input_index):
    r"""Process an image, Return a list of detected class ids and positions"""
    input_data = np.expand_dims(image, axis=0)  # expand to 4-dim

    # Process
    interpreter.set_tensor(input_index, input_data)
    interpreter.invoke()

    # Get outputs
    output_details = interpreter.get_output_details()

    positions = np.squeeze(interpreter.get_tensor(output_details[0]['index']))
    classes = np.squeeze(interpreter.get_tensor(output_details[1]['index']))
    scores = np.squeeze(interpreter.get_tensor(output_details[2]['index']))

    result = []

    for idx, score in enumerate(scores):
        if score > 0.5:
            result.append({'pos': positions[idx], 'id': classes[idx]})
    return result

def display_result(result, frame, labels):
    global CHECK_FLAG
    
    for obj in result:
        pos = obj['pos']
        id = obj['id']
        y1 = int(pos[0] * CAMERA_HEIGHT)
        x1 = int(pos[1] * CAMERA_WIDTH)
        y2 = int(pos[2] * CAMERA_HEIGHT)
        x2 = int(pos[3] * CAMERA_WIDTH)
        d=labels[id]

        midX = int(frame.shape[0]/2)
        midY = int(frame.shape[1]/2)

        a1x = midX - HITBOX_SIZE
        a1y = midY - HITBOX_SIZE

        a2x = midX + HITBOX_SIZE
        a2y = midY + HITBOX_SIZE

        hit = (x1 < a2x and x2 > a1x) and (y1 < a2y and y2 > a1y)
        if (hit):
            mqttc.publish(TOPIC, f"Hit {d} at ({x1}, {y1}. {x2}, {y2})!")
        
        # draw center marker
        cv2.rectangle(frame, 
                      (a1x, a1y),
                      (a2x, a2y),
                      (0,0,255),
                      1)
        cvzone.putTextRect(frame, f'{hit}', (a1x, a1y),1,1)

        # draw obj marker
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0),1)
        cvzone.putTextRect(frame,f'{d}',(x1,y1),1,1)

    cv2.imshow('Object Detection', frame)

if __name__ == "__main__":

    btn = Button(BUTTONPIN)
    btn.when_pressed = on_press

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(BROKER_ADDR, 1883, 60)
    mqttc.loop_start()

    model_path = 'efficientdet_lite0.tflite'
    # model_path = '1.tflite'
    label_path = 'labels.txt'
    interpreter = load_model(model_path)
    labels = load_labels(label_path)

    input_details = interpreter.get_input_details()

    # Get Width and Height
    input_shape = input_details[0]['shape']
    height = input_shape[1]
    width = input_shape[2]

    # Get input index
    input_index = input_details[0]['index']

    # Process Stream
    while True:
        im= picam2.capture_array()
        image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        image = image.resize((width, height))

        if (CHECK_FLAG):
            top_result = process_image(interpreter, image, input_index)
            display_result(top_result, im, labels)
            CHECK_FLAG = False

        key = cv2.waitKey(1)
        if key == 27:  # esc
            break


    mqttc.loop_stop()
    cv2.destroyAllWindows()
