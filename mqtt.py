import paho.mqtt.client as mqtt
import json
from Configuration import Configuration

class MQTT():

    def __init__(self, config):
        self.config = config

        self.id = config.Id
        self.name = config.name

        # public broker for testing now
        self.hubIp = config.network_hub_ip
        self.hubPort = config.network_hub_port

        self.topics = {
            "config": "blaster/config", 
            "gameplay": "hub/gameplay", 
            "score": "gameplay/score", 
            "blaster": MQTT.makeBlasterTopic(config.Id), 
            "poll": "blaster/poll" 
            }
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.callback_on_message_received = None
        print('MQTT: started mqtt client')

    def makeBlasterTopic(id):
        return f"blaster/{id}"

    def disconnect(self):
        print('MQTT: disconnecting...')
        self.mqttc.publish(self.topics['blaster'], json.dumps({
            'id': self.id,
            'cmd':'imOut'
        }))
        self.mqttc.disconnect()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"MQTT: Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        # Subscribe to all topics in the list
        for topic in self.topics.values():
            client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message_received(self, client, userdata, msg):
        message = msg.payload.decode()
        topic = msg.topic

        print(f"MQTT: Received message from {topic}: {message}")
        
        # convert message_string to json object
        json_object = json.loads(message)

        if ('ack' in json_object):
            # TODO implement
            print(f"MQTT: {json_object['cmd']} acknowledged")
        else:
            if (self.callback_on_message_received == None):
                pass
            else:
                try:
                    self.callback_on_message_received(topic, json_object)
                except Exception as e:
                    self.config.write_error_log(e)
                    exit()
                
    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message_received
        self.mqttc.connect(self.hubIp, self.hubPort, 60)
        self.mqttc.loop_start()

    def sendHit(self):
        self.mqttc.publish(self.topics['blaster'], json.dumps({
            'id': self.id,
            'cmd':'hit'
        }))

    def register_id(self):
        self.mqttc.publish(self.topics['config'], json.dumps({
            'id':self.id,
            'cmd':'regID'
        }))
    
    def request_config(self):
        self.mqttc.publish(self.topics['blaster'], json.dumps({
            'id': self.id,
            'cmd':'reqSettings'
        }))

    def im_alive(self):
        self.mqttc.publish(self.topics['blaster'], json.dumps({
            'id': self.id,
            'cmd':'pollClients',
            'ack': True
        }))
