def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def substract(a, b):
    """Returns the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def divide(a, b):
    """Returns the quotient after the division of two numbers."""
    if b != 0:
        return a / b
    else:
        return "Cannot divide by zero"
    