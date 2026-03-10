from .base_solver import BaseSolver
from backend.utils.prompt_template import linear_algebra_solver_prompt


class LinearAlgebraSolver(BaseSolver):

    def __init__(self):

        super().__init__(linear_algebra_solver_prompt())