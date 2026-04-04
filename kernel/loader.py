import os

class ModuleLoader:
    def scan(self, path):
        return [f for f in os.listdir(path) if f.endswith(".py")]
