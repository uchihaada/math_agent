from .base_solver import BaseSolver
from .calculus_solver import CalculusSolver
from .algebra_solver import AlgebraSolver
from .probability_solver import ProbabilitySolver
from .linear_algebra_solver import LinearAlgebraSolver
from .hybrid_solver import HybridSolver

SOLVER_MAP = {
    "calculus_solver": CalculusSolver,
    "algebra_solver": AlgebraSolver,
    "probability_solver": ProbabilitySolver,
    "linear_algebra_solver": LinearAlgebraSolver,
    "hybrid_solver": HybridSolver,
}


def run_solver(solver_name: str) -> BaseSolver:
    solver_class = SOLVER_MAP.get(solver_name, HybridSolver)
    return solver_class()
