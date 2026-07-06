from alphaforge.evidence.evidence_engine import EvidenceEngine


_engine = EvidenceEngine()


def build_evidence(knowledge):

    return _engine.build(knowledge)