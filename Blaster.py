from enum import Enum
from Configuration import Configuration
from mqtt import MQTT
from display_pls_work import Display
from vision import Vision
from trigger import Trigger
from gpiozero import LED
from speakerPewPew import Speaker
from time import time

class Blaster():
    def __init__(self, 
                 config : Configuration, 
                 client : MQTT = None, 
                 display : Display = None,
                 vision : Vision = None,
                 trig : Trigger = None,
                 led : LED = None,
                 speaker: Speaker = None
                 ):

        self.is_running = True

        self.game_state_enum = Enum("GameState", ["Initialization", "Playing", "Stopped"])
        self.config = config 

        self.display = display
        if (self.display != None):
            self.display.name = config.name
            self.display.update_display()

        self.client = client
        if (self.client != None):
            self.client.callback_on_message_received = self.on_message_received
            self.client.start()
            self.client.register_id()

        self.trig = trig
        if (self.trig != None):
            trig.trigger_callback_pressed = self.on_button_press
            trig.trigger_callback_released = self.on_button_release
        
        self.speaker = speaker

        self.led = led
        self.vision = vision

        self.hitAcksToReceive = 0
        
        self.score = 0
        self.button_press_timestamp = time()
        self.delay_between_shots = config.firing_cooldown

        self.game_state = self.game_state_enum.Initialization # Set to Playing after receiving 'Start' from hub
        # self.game_state = self.game_state_enum.Playing # debug mode

        print('Blaster: initialized')
    
    def do_quit(self):
        print("Blaster: quitting...")
        self.is_running = False
        self.client.disconnect()
        exit()

    def on_message_received(self, topic, message):
        # receive poll from server and send response

        if (topic == self.client.topics['poll']):
            self.client.im_alive()
            return

        # receive player name from server and update display
        elif (topic == self.client.topics['config']):
            if (message['cmd'] == 'setName' and 'id' in message):
                if (int(message['id']) == self.client.id):
                    self.config.set('name', message['name'])
                    self.display.update_name(self.config.name)
            elif(message['cmd'] == 'setConfig'):
                self.config = Configuration(message['config'])
                self.do_quit()
            elif(message['cmd' == 'reset']):
                self.do_quit()
            elif(message['cmd'] == 'setInterval'):
                self.trig.cooldown_time = float(message['interval'])

        # receive start and stop game from server and start/stop game
        elif(topic == self.client.topics['gameplay']):
            if(message['cmd'] == 'gameStart'):
                self.game_state = self.game_state_enum.Playing
            elif(message['cmd'] == 'gameStop'):
                self.game_state = self.game_state_enum.Stopped

        # receive current score and update display
        elif(topic == self.client.topics['score'] and 'id' in message):
            if (message['cmd'] == 'hit' and message['id'] == self.client.id):
                self.score = message['score']
                self.display.update_score(self.score)
                self.hitAcksToReceive = self.hitAcksToReceive - 1
            
    def on_button_press(self):
        if (self.game_state == self.game_state_enum.Playing):
            # check if shot is allowed by checking time since last shot
            if((time() - self.button_press_timestamp) > self.delay_between_shots):
                self.button_press_timestamp = time()
                self.led.on()
                self.speaker.play_pewpew_async(volume=1, duration=0.3)
                
                ## TODO implement this nicely. this is just for demo
                hit, d = self.vision.checkForHuman()
                if (hit):
                    print(f'BlasterClient: hit {d}')
                    self.hitAcksToReceive = self.hitAcksToReceive + 1
                    for hit in range(self.hitAcksToReceive):
                        self.client.sendHit()
                    self.display.hit = True
                    self.display.needs_update = True   
                else:
                    self.display.missed = True
                    self.display.needs_update = True  

    def on_button_release(self):
        if (self.game_state == self.game_state_enum.Playing):
            self.led.off()

            ## TODO implement this nicely. this is just for demo
            self.display.hit = False
            self.display.missed = False

