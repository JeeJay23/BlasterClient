import prototype

mqtt_thingy = prototype.MQTT('mqtt-dashboard.com', 'test/hits')

mqtt_thingy.start()
mqtt_thingy.publish("test/hits", "Hello World!")

while True:
    pass