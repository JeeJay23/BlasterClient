# import sys
# from uuid import getnode as get_mac
# from Configuration import Configuration
# from Blaster import Blaster
# from mqtt import MQTT
from trigger import Trigger

def trigger_callback_pressed():
    print('This button pressed calledback is called in main')

def trigger_callback_released():
    print('This button released calledback is called in main')

if __name__ == "__main__":
    # settings_filepath = sys.argv[1]

    # config = Configuration.createTestConfig()
    # config.set("ID", get_mac())

    # client = MQTT(config)

    # blaster = Blaster(config, client)

    trig = Trigger(button_pin=26, 
                    led_pin=13,
                    trigger_callback_pressed=trigger_callback_pressed, 
                    trigger_callback_released=trigger_callback_released)

    while True:
        pass