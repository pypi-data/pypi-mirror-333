# cppmath

A fast library of mathematical algorithms in C++, optimized for Olympiad problems and high-performance computing.

## Installation

```bash
pip install cppmath
```

## Usage

```python
import cppmath

# High Precision Initialization
config = cppmath.initialize_precision(precision_bits=128, optimize_cache=True)

# Linear Algebra
matrix = [[1, 2], [3, 4]]
result = cppmath.fast_matrix_power(matrix, 10)
eigenvalues ​​= cppmath.eigenvalue_approximation(matrix)

# Optimization
objective = [1, 2, 3]
constraints = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
result = cppmath.optimization_solver(objective, constraints, method="genetic")

# Differential equations
coeffs = [1, 0.5, 0.25]
initial = [1.0, 0.0]
solution = cppmath.differential_equation_solver(coeffs, initial, step_size=0.01, num_steps=100)

# Numerical integration
function_coeffs = [1, 2, 3] # f(x) = 1 + 2x + 3x^2
integral = cppmath.numerical_integration(function_coeffs, 0, 1, intervals=1000)

# Monte Carlo simulation
points = cppmath.monte_carlo_simulation(dimensions=3, samples=1000, seed=42)
```

## Functionality

- High-performance linear algebras
- Optimization methods (genetic algorithms, simplex method)
- Solving differential equations
- Numerical integration
- Monte Carlo simulations
- Fast Fourier transform
- Distributed caching of computations

## Requirements

- Python 3.6+
- NumPy (optional, for better performance)
- requests (for distributed caching)

## License

MIT