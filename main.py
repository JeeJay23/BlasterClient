import mqtt

def message_handler(topic, message):
    print(f"Received message from {topic}: {message}")
    # TODO handle messages from server

id = 1

server_ip = 'mqtt-dashboard.com' # to be set to the server IP

blaster_topic = 'blaster/'+str(id)

list_of_publish_topics = ['blaster/config', 'hub/hits']

list_of_subscribe_topics = ['blaster/config', 'hub/gameplay', blaster_topic]

mqtt_thingy = mqtt.MQTT(server_ip, list_of_subscribe_topics, message_handler)

mqtt_thingy.start()

mqtt_thingy.publish("blaster/config", f'{{"cmd": "register", "id": {id}}}')


while True:
    # send something from server 'test/config' topic to receive it here
    
    
    pass