from collections.abc import Mapping

from backend.models.schemas import ParserOutput, RouterOutput


def select_solver(topics):

    if len(topics) > 1:
        return "hybrid_solver"

    topic = topics[0]

    if topic == "calculus":
        return "calculus_solver"

    if topic == "algebra":
        return "algebra_solver"

    if topic == "probability":
        return "probability_solver"

    if topic == "linear_algebra":
        return "linear_algebra_solver"

    return "hybrid_solver"


def _read_topics(parsed_problem: ParserOutput | Mapping[str, object]):
    if isinstance(parsed_problem, ParserOutput):
        return parsed_problem.topics

    return parsed_problem["topics"]


def route_problem(parsed_problem: ParserOutput | Mapping[str, object]):

    topics = _read_topics(parsed_problem)

    solver = select_solver(topics)

    return RouterOutput(solver=solver)
