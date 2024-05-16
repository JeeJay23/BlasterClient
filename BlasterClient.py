import sys
from uuid import getnode as get_mac
from Configuration import Configuration
from Blaster import Blaster
from mqtt import MQTT
from trigger import Trigger
from gpiozero import LED
from display_pls_work import Display
from vision import Vision
from time import sleep

def trigger_callback_pressed():
    led.on()
    
    ## TODO implement this nicely. this is just for demo
    disp.hit = True
    disp.update_score()
    
    print('This button pressed calledback is called in main')

def trigger_callback_released():
    led.off()

    ## TODO implement this nicely. this is just for demo
    disp.hit = False
    disp.update_display()

    print('This button released calledback is called in main')

if __name__ == "__main__":
    settings_filepath = sys.argv[1]

    print(f'BlasterClient started with config {settings_filepath}')

    config = Configuration(settings_filepath)
    config.set("ID", get_mac())

    client = MQTT(config)
    blaster = Blaster(config, client)
    
    # initialize led and turn off by default
    led = LED(13)
    led.off()

    # initialize trigger
    trig = Trigger(button_pin=6, 
                    trigger_callback_pressed=trigger_callback_pressed, 
                    trigger_callback_released=trigger_callback_released)

    # initialize display (default name is Sjaakie, can be updated with disp.update_name('name'))'
    disp = Display()
    vision = Vision(config)

    while True:
        hit, d = vision.checkForHuman()
        if (hit):
            print(f'BlasterClient: hit {d}')
            blaster.hit()
        sleep(1)
