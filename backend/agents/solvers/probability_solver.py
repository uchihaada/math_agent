from .base_solver import BaseSolver
from backend.utils.prompt_template import probability_solver_prompt


class ProbabilitySolver(BaseSolver):

    def __init__(self):

        super().__init__(probability_solver_prompt())