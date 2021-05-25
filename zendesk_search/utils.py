class Bunch:
    """A simple class allowing dynamic attributes."""

    def __init__(self):
        self.__dict__["_data"] = {}

    def __getattr__(self, key):
        return self._data[key]

    def __setattr__(self, key, value) -> None:
        self._data[key] = value
