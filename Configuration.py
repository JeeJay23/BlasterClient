import json

class Configuration(object):
    def __init__(self, filepath) -> None:
        with open(filepath, mode='r') as file:
            self.configJson = json.loads(file.read())
            print(self.configJson.get('ID'))
    
    def get(self, key):
        return self.configJson[key]

    def set(self, key, value):
        self.configJson[key] = value;

    def write(self, filepath):
        with open(filepath, mode='w') as file:
            file.write(json.dumps(self.configJson, indent='\t'))