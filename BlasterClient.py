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

    try:
        client = MQTT(config)
        
        led = LED(config.led_pin)
        led.off()

        trig = Trigger(button_pin=config.button_pin)
        disp = Display()
        vision = Vision(config)
        speaker = Speaker(config.speaker_pin)

        blaster = Blaster(
            config=config, 
            client=client, 
            display=disp, 
            vision=vision, 
            trig=trig, 
            led=led,
            speaker=speaker)
    except Exception as e:
        config.write_error_log(e)
        print(f"BlasterClient: application crashed with exception {e}")
        exit()

    while (blaster.is_running):
        sleep(1)
    
    # save settings on succesfull exit
    config.write(settings_filepath)
    print("BlasterClient: exited successfully")
