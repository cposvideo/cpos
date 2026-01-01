class ModelRegistry:
    def __init__(self):
        self._models = {}

    def register(self, name, version):
        self._models[name] = version

    def get_version(self, name):
        return self._models.get(name)
