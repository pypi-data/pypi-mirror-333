from .core import initialize_precision
from .linear import fast_matrix_power, eigenvalue_approximation
from .integration import numerical_integration, monte_carlo_simulation
from .optimization import optimization_solver, differential_equation_solver
from .cache import set_computation_params, get_optimized_solutions

__version__ = "1.0.0"
__author__ = "mathercpp"
__email__ = ""

__all__ = [
    'initialize_precision',
    'fast_matrix_power',
    'eigenvalue_approximation',
    'numerical_integration',
    'monte_carlo_simulation',
    'optimization_solver',
    'differential_equation_solver',
    'set_computation_params',
    'get_optimized_solutions',
]
