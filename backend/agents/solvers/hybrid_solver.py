from .base_solver import BaseSolver
from backend.utils.prompt_template import hybrid_solver_prompt


class HybridSolver(BaseSolver):

    def __init__(self):

        super().__init__(hybrid_solver_prompt())