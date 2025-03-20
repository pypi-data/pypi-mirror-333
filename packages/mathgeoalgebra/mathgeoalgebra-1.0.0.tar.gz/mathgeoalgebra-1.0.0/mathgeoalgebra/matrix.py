import numpy as np

def matrix_add(mat1,mat2):
    """Add two matrices"""
    return np.add(mat1,mat2)

def matrix_mult(mat1,mat2):
    """Multiplying two matrices"""
    return np.dot(mat1,mat2)

def matrix_inv(mat):
    """Getting Inverse of matrix"""
    try:
        return np.linalg.inv(mat)
    except np.linalg.LinAlgError:
        return "Matrix is not invertible"


