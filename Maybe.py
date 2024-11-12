class Maybe:
    def __init__(self, value):
        self.value = value

    def is_nothing(self):
        return self.value is None

    def __str__(self):
        return f"{self.value}"

    def bind(self, func):
        if self.is_nothing():
            return self
        return func(self.value)

    @staticmethod
    def just(value):
        return Maybe(value)

    @staticmethod
    def nothing():
        return Maybe(None)