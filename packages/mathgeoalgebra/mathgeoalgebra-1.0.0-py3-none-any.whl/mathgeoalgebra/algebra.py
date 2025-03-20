import numpy as np

def solve_linear(coefficient,constant):
    """Solve a system of linear equation Ax= B"""
    coefficient = np.array(coefficient)
    constant = np.array(constant)
    solution = np.linalg.solve(coefficient,constant)
    return solution