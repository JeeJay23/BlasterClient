import paho.mqtt.client as mqtt
import json
from Configuration import Configuration

class MQTT():

    def __init__(self, config):
        self.config = config

        self.id = config.getId()
        self.name = "jebedemiah"

        self.BROKER_ADDR = config.get('server-ip')
        self.TOPICS = { "config_topic": "blaster/config", "gameplay_topic": "hub/gameplay", "blaster_topic": MQTT.makeBlasterTopic(config.get("ID")) }
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.start()

    def makeBlasterTopic(id):
        return f"blaster/{id}"

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        # Subscribe to all topics in the list
        for topic in self.TOPICS.values():
            client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message_received(self, client, userdata, msg):
        message = msg.payload.decode()
        topic = msg.topic

        print(f"Received message from {topic}: {message}")
        
        # example JSON messages
        # json_object cmdAck to receive
        #   {
        #       "cmd": "ack",
        #       "id": 0 // id of the hub
        #       "cmdAck": "regID" // command that was acknowledged
        #   }
        # -> { "cmd": "ack", "id": 0, "cmdAck": "regID" }
        
        # example JSON messages
        # json_object settings to receive
        #   {
        #       "cmd": "setSettings",
        #       "id": 0 // id of the hub
        #       "someSettings": 
        #           {
        #               "setting1": "value1",   
        #               "setting2": "value2"
        #           }
        #   }
        # -> { "cmd": "setSettings", "id": 0, "someSettings": { "setting1": "value1", "setting2": "value2" } }



        # convert message_string to json object
        json_object = json.loads(message)

        # Handle ack messages
        if topic == self.TOPICS['blaster_topic']:
            # Handle ack message for registration
            if json_object['cmd'] == 'ack' and json_object['cmdAck'] == 'regID':
                self.register_ack_callback()

            if json_object['cmd'] == 'setSettings':
                self.request_config_callback(json_object['someSettings'])
                
    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message_received
        self.mqttc.connect(self.BROKER_ADDR, 1883, 60)
        self.mqttc.loop_start()

    def sendHit(self):
        msg = {}
        msg['id'] = self.id
        msg['cmd'] = 'hit'
        self.mqttc.publish("gameplay/hits", json.dumps(msg))

    def register_id(self):
        # TODO make name not hardcoded
        msg = {}
        msg['id'] = self.id
        msg['cmd'] = 'pollAck'
        msg['name'] = self.name

        self.mqttc.publish("blaster/config", json.dumps(msg))
    
    def request_config(self):
        msg = { 
            'id' : self.id, 
            'cmd' : "reqSettings"
        }
        self.mqttc.publish("blaster/config", json.dumps(msg))