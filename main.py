import mqtt
from uuid import getnode as get_mac

class Blaster():

    def __init__(self):
        self.config = None # TODO set to config object
        self.game_state = False # Set to true after receiving 'Start' from hub
        self.id = get_mac()

        # this will later all be retreived from config -> pass object to mqtt class
        self.blaster_topic = 'blaster/'+str(self.id)
        self.list_of_publish_topics = ['blaster/config', 'hub/hits']
        # create dictory of subscribe topics
        self.list_of_subscribe_topics = { "config_topic": "blaster/config", "gameplay_topic": "hub/gameplay", "blaster_topic": self.blaster_topic }
        self.server_ip = 'mqtt-dashboard.com' 
        self.mqtt_thingy = mqtt.MQTT(self.id, self.server_ip, self.list_of_subscribe_topics, self.register_ack_callback, self.request_config_callback)
        self.mqtt_thingy.start()

        self.ack_received = False


    def initialize_blaster(self):
        self.mqtt_thingy.register_id()

    def register_ack_callback(self):
        self.mqtt_thingy.request_config()
    
    def request_config_callback(self, config):
        pass


blaster_gun_thingy = Blaster()
blaster_gun_thingy.initialize_blaster()

while True:
    pass # blocking