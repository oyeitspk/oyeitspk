import json

global config
with open('config.json', 'r') as config_file:
    config = config_file.read()
    config = json.loads(config)