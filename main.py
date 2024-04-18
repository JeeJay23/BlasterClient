import prototype

mqtt_thingy = prototype.MQTT('mqtt-dashboard.com', ['test/hits', 'test/config'])

mqtt_thingy.start()
mqtt_thingy.publish("test/hits", "Somebody has been hit!")

while True:
    # send something from server 'test/config' topic to receive it here
    pass