import sys
from uuid import getnode as get_mac
from Configuration import Configuration
from Blaster import Blaster
# from mqtt import MQTT
from trigger import Trigger
from gpiozero import LED

def trigger_callback_pressed():
    led.on()
    print('This button pressed calledback is called in main')

def trigger_callback_released():
    led.off()
    print('This button released calledback is called in main')

if __name__ == "__main__":
    settings_filepath = sys.argv[1]

    config = Configuration.createTestConfig()
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

    while True:
        pass