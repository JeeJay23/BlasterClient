import paho.mqtt.client as mqtt

class MQTT():

    def __init__(self, broker_ip, topic_list, message_callback):
        self.BROKER_ADDR = broker_ip
        self.TOPICS = topic_list
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.message_callback = message_callback
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for t in self.TOPICS:
            client.subscribe(t)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        self.message_callback(msg.topic, msg.payload.decode())


    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.connect(self.BROKER_ADDR, 1883, 60)
        self.mqttc.loop_start()

    def publish(self, topic, message):
        self.mqttc.publish(topic, message)