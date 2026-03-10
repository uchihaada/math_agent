from .base_solver import BaseSolver
from backend.utils.prompt_template import algebra_solver_prompt


class AlgebraSolver(BaseSolver):

    def __init__(self):

        super().__init__(algebra_solver_prompt())