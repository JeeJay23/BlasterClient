from enum import Enum
from Configuration import Configuration
from mqtt import MQTT
from display_pls_work import Display
from vision import Vision
from trigger import Trigger
from gpiozero import LED

GameState = Enum("GameState", ["Initialization", "Playing", "Stopped"])

class Blaster():

    def __init__(self, config : Configuration, 
                 client : MQTT, 
                 display : Display,
                 trig : Trigger,
                 led : LED
                 ):

        self.config = config 

        self.client = client
        self.client.callback_on_message_received = self.on_message_received
        self.client.register_id()

        self.display = display
        self.display.name = config.name
        self.display.update_display()

        self.trig = trig
        trig.trigger_callback_pressed = self.on_button_press
        trig.trigger_callback_released = self.on_button_release

        self.led = led

        self.game_state = GameState.Initialization # Set to true after receiving 'Start' from hub
        print('Blaster: initialized')

    def callback_register_ack(self):
        self.client.request_config()
    
    def callback_request_config(self, config):
        pass

    def on_message_received(self, topic, message):
        # # Handle ack messages
        # if topic == self.TOPICS['blaster_topic']:
        #     # Handle ack message for registration
        #     if json_object['cmd'] == 'ack' and json_object['cmdAck'] == 'True':
        #         self.register_ack_callback()

        #     if json_object['cmd'] == 'setSettings':
        #         self.request_config_callback(json_object['someSettings'])

        #     #if json_object['cmd'] == 'ack' and json_object[]

        # if topic == self.TOPICS['poll_topic']:
        if (topic == self.client.TOPICS['poll_topic']):
            self.client.im_alive()
        
        
    

    def on_button_press(self):
        self.led.on()
        
        ## TODO implement this nicely. this is just for demo
        hit, d = self.vision.checkForHuman()
        if (hit):
            print(f'BlasterClient: hit {d}')
            #blaster.hit()
            self.disp.hit = True    
            self.disp.update_score()
        else:
            self.disp.missed = True
        self.disp.update_display()

    def on_button_release(self):
        self.led.off()

        ## TODO implement this nicely. this is just for demo
        self.disp.hit = False
        self.disp.missed = False
        self.disp.update_display()

    def hit(self):
        self.client.sendHit()

