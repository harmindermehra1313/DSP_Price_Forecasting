import time

class Cache:
    def __init__(self):
        self.store = {}

    def set(self, key, value, ttl=3600):
        expiry = time.time() + ttl
        self.store[key] = (value, expiry)

    def get(self, key):
        if key in self.store:
            value, expiry = self.store[key]
            if time.time() < expiry:
                return value
            else:
                del self.store[key]
        return None