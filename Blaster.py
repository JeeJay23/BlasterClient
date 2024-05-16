from enum import Enum
from Configuration import Configuration
from mqtt import MQTT

GameState = Enum("GameState", ["Initialization", "Playing", "Stopped"])

class Blaster():

    def __init__(self, config : Configuration, client : MQTT):
        self.config = config 
        self.game_state = GameState.Initialization # Set to true after receiving 'Start' from hub

        self.client = client
        self.client.register_ack_cb = self.register_ack_callback
        self.client.request_config_cb = self.request_config_callback
        self.client.register_id()
        print('Blaster: initialized')

    def register_ack_callback(self):
        self.client.request_config()
    
    def request_config_callback(self, config):
        pass

    def hit(self):
        self.client.sendHit()

