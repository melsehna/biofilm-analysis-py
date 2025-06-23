import json

def load_config(path='experiment_config.json'):
    with open(path) as f:
        return json.load(f)

