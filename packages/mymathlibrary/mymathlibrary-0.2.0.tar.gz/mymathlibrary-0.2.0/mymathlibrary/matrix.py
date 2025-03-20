import numpy as np

def add_matrix(a, b):
    return np.add(a, b)

def multiply_matrix(a, b):
    return np.dot(a, b)

def inverse_matrix(a):
    return np.linalg.inv(a)
