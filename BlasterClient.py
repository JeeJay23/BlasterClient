import sys
from uuid import getnode as get_mac
from Configuration import Configuration
from Blaster import Blaster
from mqtt import MQTT

if __name__ == "__main__":
    settings_filepath = sys.argv[1]

    config = Configuration.createTestConfig();
    config.set("ID", get_mac())

    client = MQTT(config)

    blaster = Blaster(config, client)

    while True:
        pass
