from datetime import datetime


class Calculation:
    def __init__(self, operation, a, b, result):
        self.operation = operation
        self.a = a
        self.b = b
        self.result = result
        self.timestamp = datetime.now()