def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    return a ** b

def root(a, b):
    if b == 0:
        raise ValueError("Root degree cannot be zero")
    if a < 0 and b % 2 == 0:
        raise ValueError("Cannot calculate an even root of a negative number")
    if a < 0:
        return -((-a) ** (1 / b))
    return a ** (1 / b)

def modulus(a, b):
    if b == 0:
        raise ValueError("Cannot calculate modulus by zero")
    return a % b

def integer_division(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a // b

def percentage(a, b):
    if b == 0:
        raise ValueError("Cannot calculate percentage with zero")
    return (a / b) * 100

def absolute_difference(a, b):
    return abs(a - b)

class Addition:
    def execute(self, a, b):
        return add(a, b)

class Subtraction:
    def execute(self, a, b):
        return subtract(a, b)

class Multiplication:
    def execute(self, a, b):
        return multiply(a, b)

class Division:
    def execute(self, a, b):
        return divide(a, b)

class Power:
    def execute(self, a, b):
        return power(a, b)

class Root:
    def execute(self, a, b):
        return root(a, b)

class Modulus:
    def execute(self, a, b):
        return modulus(a, b)

class IntegerDivision:
    def execute(self, a, b):
        return integer_division(a, b)

class Percentage:
    def execute(self, a, b):
        return percentage(a, b)

class AbsoluteDifference:
    def execute(self, a, b):
        return absolute_difference(a, b)

class OperationFactory:
    operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "integer_division": IntegerDivision,
        "percentage": Percentage,
        "absolute_difference": AbsoluteDifference
    }

    @staticmethod
    def create(name):
        if name not in OperationFactory.operations:
            raise ValueError("Unknown operation")
        return OperationFactory.operations[name]()