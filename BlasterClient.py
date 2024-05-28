import sys
from uuid import getnode as get_mac
from Configuration import Configuration
from Blaster import Blaster
from mqtt import MQTT
from trigger import Trigger
from gpiozero import LED
from display_pls_work import Display
from vision import Vision
from speakerPewPew import Speaker
from time import sleep

if __name__ == "__main__":
    settings_filepath = sys.argv[1]
    print(f'BlasterClient started with config {settings_filepath}')

    config = Configuration(settings_filepath)
    config.set("Id", get_mac())
    client = MQTT(config)
    
    led = LED(13)
    led.off()

    trig = Trigger(button_pin=6)
    disp = Display()
    vision = Vision(config)
    speaker = Speaker(12)

    blaster = Blaster(
        config=config, 
        client=client, 
        display=None, 
        vision=vision, 
        trig=trig, 
        led=led,
        speaker=None)

    #blaster = Blaster(config=config, client=client)

    while True:
        sleep(1)
