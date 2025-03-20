import numpy as np

def add_matrix(a, b):
    """Returns the sum of two matrices.
    It takes two numpy arrays as arguments.
    """
    return np.add(a, b)

def multiply_matrix(a, b):
    """Returns the product of two matrices.
    It takes two numpy arrays as arguments.
    """
    return np.dot(a, b)

def inverse_matrix(a):
    """Returns the inverse of a matrix.
    It takes a numpy array as argument.
    """
    return np.linalg.inv(a)
