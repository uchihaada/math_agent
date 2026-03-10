from backend.agents.verifier_agent import verify_solution


problem = "Find derivative of x^2 sin(x)"

solution = """
Using derivative rules:

d/dx(x^2 sin x)

= 2x sin x

Final answer: 2x sin x
"""

result = verify_solution(problem, solution)

print(result)