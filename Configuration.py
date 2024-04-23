import json

class Configuration(object):
    def __init__(self, filepath) -> None:
        with open(filepath) as file:
            print(file)