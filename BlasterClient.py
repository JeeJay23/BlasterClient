import sys
from Configuration import Configuration

if __name__ == "__main__":
    settings_filepath = sys.argv[1]
    config = Configuration(settings_filepath)
    a = config.get('ID')
    a = a+1
    config.set('ID', a)
    config.write(settings_filepath)