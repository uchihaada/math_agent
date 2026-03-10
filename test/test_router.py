import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.router_agent import route_problem


parsed_problem = {
    "problem_text": "Find derivative of x^2 tan(x)",
    "topics": ["calculus"],
    "variables": ["x"],
    "constraints": [],
    "needs_clarification": False
}

result = route_problem(parsed_problem)

print(result)