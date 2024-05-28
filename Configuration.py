import json
import time

class Configuration(object):
    def __init__(self, filepath : str = None) -> None:
        if (filepath == None):
            print('Configuration: Created empty config')
            self.configDict = {}
        else:
            with open(filepath, mode='r') as file:
                self.configDict = json.loads(file.read())
                print(f'Configuration: Loaded existing config')

    def createFromString(json : str):
        config = Configuration()
        config.configDict = json.loads(json)
        return config
        
    def createTestConfig():
        config = Configuration()
        config.set("ID", -1)
        config.set("name", "testname")
        config.set("server-ip", "mqtt-dashboard.com")

        return config
    
    def __getattr__(self, attr):
        return self.configDict[attr]

    def set(self, key, value):
        self.configDict[key] = value

    def write_error_log(self, error):
        with open(self.error_log_filepath, mode='a') as file:
            file.write(f"\n[{time.asctime()}]:\t{error}")

    def write(self, filepath):
        with open(filepath, mode='w') as file:
            file.write(json.dumps(self.configDict, indent='\t'))