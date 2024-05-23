from enum import Enum
from Configuration import Configuration
from mqtt import MQTT

GameState = Enum("GameState", ["Initialization", "Playing", "Stopped"])

class Blaster():

    def __init__(self, config : Configuration, client : MQTT):
        self.config = config 
        self.game_state = GameState.Initialization # Set to true after receiving 'Start' from hub

        self.client = client

        self.client.callback_on_message_received = self.on_message_received
        self.client.register_id()
        print('Blaster: initialized')

    def callback_register_ack(self):
        self.client.request_config()
    
    def callback_request_config(self, config):
        pass

    def on_message_received(self, message):
        # # Handle ack messages
        # if topic == self.TOPICS['blaster_topic']:
        #     # Handle ack message for registration
        #     if json_object['cmd'] == 'ack' and json_object['cmdAck'] == 'True':
        #         self.register_ack_callback()

        #     if json_object['cmd'] == 'setSettings':
        #         self.request_config_callback(json_object['someSettings'])

        #     #if json_object['cmd'] == 'ack' and json_object[]

        # if topic == self.TOPICS['poll_topic']:
        pass

    def hit(self):
        self.client.sendHit()

