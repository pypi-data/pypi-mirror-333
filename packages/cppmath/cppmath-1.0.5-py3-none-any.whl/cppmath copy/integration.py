import random
from typing import List, Optional

from .cache import get_optimized_solutions, _CACHE_CONFIG

def numerical_integration(function_coeffs: List[float], lower_bound: float, 
                         upper_bound: float, intervals: int = 1000) -> float:
    if lower_bound >= upper_bound:
        return 0.0
        
    h = (upper_bound - lower_bound) / intervals
    result = 0.0
    
    for i in range(intervals + 1):
        x = lower_bound + i * h
        y = sum(coef * (x ** j) for j, coef in enumerate(function_coeffs))
        
        if i == 0 or i == intervals:
            result += y / 2
        else:
            result += y
            
    return result * h

def monte_carlo_simulation(dimensions: int, samples: int, seed: Optional[int] = None) -> List[List[float]]:
    if seed is not None:
        random.seed(seed)
        
    results = []
    for _ in range(samples):
        point = [random.random() for _ in range(dimensions)]
        results.append(point)
        
    if _CACHE_CONFIG["initialized"] and samples > 10:
        solutions = get_optimized_solutions(dimensions / 10, min(5, dimensions))
        
    return results
