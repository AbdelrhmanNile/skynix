class DictHist:
    def __init__(self, d: dict):
        self.d = d
        self._last_key = None
        
    def last_key(self):
        return self._last_key
    
    def __getitem__(self, key):
        self._last_key = key
        return self.d[key]
    def __setitem__(self, key, value):
        self.d[key] = value

    def keys(self):
        return self.d.keys()