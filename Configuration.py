import json

class Configuration(object):
    def __init__(self, filepath=None) -> None:
        if (filepath == None):
            self.cfDict = {}
        else:
            with open(filepath, mode='r') as file:
                self.cfDict = json.loads(file.read())

        
    def createTestConfig():
        config = Configuration()
        config.set("ID", -1)
        config.set("name", "testname")
        config.set("server-ip", "mqtt-dashboard.com")

        return config

    def getId(self):
        return self.cfDict["ID"]

    def get(self, key):
        return self.cfDict[key]

    def set(self, key, value):
        self.cfDict[key] = value;

    def write(self, filepath):
        with open(filepath, mode='w') as file:
            file.write(json.dumps(self.cfDict, indent='\t'))