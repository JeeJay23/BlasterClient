import paho.mqtt.client as mqtt
import json

class MQTT():

    def __init__(self, id, broker_ip, topic_list, register_ack_callback, request_config_callback):
        self.id = id
        self.BROKER_ADDR = broker_ip
        self.TOPICS = topic_list
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.register_ack_callback = register_ack_callback
        self.request_config_callback = request_config_callback
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        # Subscribe to all topics in the list
        for topic in self.TOPICS.values():
            client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
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
                self.request_config_callback(json_object)
                
            



    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.connect(self.BROKER_ADDR, 1883, 60)
        self.mqttc.loop_start()


    def register_id(self):
        self.mqttc.publish("blaster/config", f'{{"cmd": "regID", "id": {self.id}}}')
    
    def request_config(self):
        self.mqttc.publish("blaster/config", f'{{"cmd": "reqSettings", "id": {self.id}}}')