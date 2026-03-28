import yaml
from config.paths import CONFIG_PATH

class ConfigLoader:
    def __init__(self, path=CONFIG_PATH):
        with open(path, "r") as f:
            self.config = yaml.safe_load(f)

    def get(self, key):
        return self.config.get(key, {})