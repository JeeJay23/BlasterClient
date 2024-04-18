import mqtt

mqtt_thingy = mqtt.MQTT('mqtt-dashboard.com', ['test/hits', 'test/config'])

mqtt_thingy.start()
mqtt_thingy.publish("test/hits", "Somebody has been hit!")

while True:
    # send something from server 'test/config' topic to receive it here
    pass