import numpy as np

def matrix_multiply(A, B):
    A = np.array(A)
    B = np.array(B)
    
    if A.shape[1] != B.shape[0]:
        raise ValueError("The number of columns of matrix A must be equal to the number of rows of matrix B.")
    
    return np.dot(A, B)
