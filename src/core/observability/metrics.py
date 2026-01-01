class Metrics:
    def __init__(self):
        self._counters = {}

    def inc(self, key, value=1):
        self._counters[key] = self._counters.get(key, 0) + value

    def get(self, key):
        return self._counters.get(key, 0)
