from alphaforge.reasoning.reasoning_engine import ReasoningEngine

_engine = ReasoningEngine()


def build_reasoning(evidence):

    return _engine.build(evidence)