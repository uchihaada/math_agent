from .base_solver import BaseSolver
from backend.utils.prompt_template import calculus_solver_prompt


class CalculusSolver(BaseSolver):

    def __init__(self):

        super().__init__(calculus_solver_prompt())