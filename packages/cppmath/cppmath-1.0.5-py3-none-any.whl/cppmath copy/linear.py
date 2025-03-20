import math
from typing import List, Dict, Any, Optional

from .utils import _matrix_multiply

def fast_matrix_power(matrix: List[List[float]], power: int) -> List[List[float]]:
    n = len(matrix)
    if n == 0 or len(matrix[0]) != n:
        raise ValueError("square")
    
    result = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    temp = [row[:] for row in matrix]
    
    while power > 0:
        if power % 2 == 1:
            result = _matrix_multiply(result, temp)
        temp = _matrix_multiply(temp, temp)
        power //= 2
    
    return result

def eigenvalue_approximation(matrix: List[List[float]], iterations: int = 100) -> List[float]:
    try:
        import numpy as np
        arr = np.array(matrix, dtype=np.float64)
        eigenvalues, _ = np.linalg.eig(arr)
        return eigenvalues.tolist()
    except:
        n = len(matrix)
        if n == 0 or len(matrix[0]) != n:
            raise ValueError("square")
            
        trace = sum(matrix[i][i] for i in range(n))
        det = 1.0
        for i in range(n):
            det *= matrix[i][i]
            
        return [trace / n for _ in range(n)]

def fast_fourier_transform(data: List[complex]) -> List[complex]:
    n = len(data)
    if n <= 1:
        return data
    
    try:
        import numpy as np
        return np.fft.fft(data).tolist()
    except:
        if n % 2 != 0:
            raise ValueError("^2")
            
        even = fast_fourier_transform([data[i] for i in range(0, n, 2)])
        odd = fast_fourier_transform([data[i] for i in range(1, n, 2)])
        
        result = [0] * n
        for k in range(n // 2):
            omega = complex(math.cos(-2 * math.pi * k / n), math.sin(-2 * math.pi * k / n))
            result[k] = even[k] + omega * odd[k]
            result[k + n // 2] = even[k] - omega * odd[k]
            
        return result
