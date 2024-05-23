from enum import Enum
from Configuration import Configuration
from mqtt import MQTT
from display_pls_work import Display
from vision import Vision
from trigger import Trigger
from gpiozero import LED



class Blaster():
    def __init__(self, 
                 config : Configuration, 
                 client : MQTT = None, 
                 display : Display = None,
                 vision : Vision = None,
                 trig : Trigger = None,
                 led : LED = None
                 ):

        self.GameState = Enum("GameState", ["Initialization", "Playing", "Stopped"])
        
        self.config = config 

        self.client = client
        if (self.client == None):
            pass
        else:
            self.client.callback_on_message_received = self.on_message_received
            self.client.register_id()

        self.display = display
        if (self.display == None):
            pass
        else:
            self.display.name = config.name
            self.display.update_display()

        self.trig = trig
        if (self.trig == None):
            pass
        else:
            trig.trigger_callback_pressed = self.on_button_press
            trig.trigger_callback_released = self.on_button_release

        self.led = led

        self.vision = vision

        self.score = 0

        self.game_state = self.GameState.Initialization # Set to Playing after receiving 'Start' from hub
        print('Blaster: initialized')

    def callback_register_ack(self):
        # TODO move to on_message_receive
        self.client.request_config()
    
    def callback_request_config(self, config):
        # TODO move to on_message_receive
        pass

    def on_message_received(self, topic, message):
        # receive poll from server and send response
        if (topic == self.client.topics['poll']):
            self.client.im_alive()

        # receive player name from server and update display
        elif (topic == self.client.topics['config']):
            if (message['cmd'] == 'setName'):
                self.config.set('name', message['name'])
                self.display.update_name(self.config.name)

        # receive start and stop game from server and start/stop game
        elif(topic == self.client.topics['gameplay']):
            if(message['cmd'] == 'gameStart'):
                self.game_state = self.GameState.Playing
            elif(message['cmd'] == 'gameStop'):
                self.game_state = self.GameState.Stopped

        # receive current score and update display
        elif(topic == self.client.topics['blaster']):
            if (message['cmd'] == 'hit'):
                self.score = message['score']
                self.display.update_score(self.score)
            
    def on_button_press(self):
        if (self.game_state == self.GameState.Playing):
            self.led.on()
            
            ## TODO implement this nicely. this is just for demo
            hit, d = self.vision.checkForHuman()
            if (hit):
                print(f'BlasterClient: hit {d}')
                self.client.sendHit()
                self.display.hit = True    
            else:
                self.display.missed = True
            self.display.update_display()

    def on_button_release(self):
        if (self.game_state == self.GameState.Playing):
            self.led.off()

            ## TODO implement this nicely. this is just for demo
            self.display.hit = False
            self.display.missed = False
            self.display.update_display()

