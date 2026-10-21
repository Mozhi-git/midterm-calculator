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