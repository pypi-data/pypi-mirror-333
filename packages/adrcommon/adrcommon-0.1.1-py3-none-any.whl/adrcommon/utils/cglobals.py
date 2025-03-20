from . import maputil


class CGlobals(object):
    def __init__(self):
        self._values = {}

    def reset(self):
        self._values.clear()

    def get(self, key, default=None):
        return self._values.get(key, default)

    def keys(self):
        return self._values.keys()

    def __getitem__(self, key):
        return self._values.__getitem__(key)

    def __setitem__(self, key, value):
        maputil.compute_if_absent(self._values, key, lambda _: value)

    def __delitem__(self, key):
        if key in self.keys():
            self._values.__delitem__(key)


cglobals = CGlobals()
