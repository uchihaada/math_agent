import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.parser_agent import parse_question

question = "Find derivative of determinant | x x^2 ; x^3 2x |"

result = parse_question(question)

print(result)