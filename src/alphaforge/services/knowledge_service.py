from alphaforge.knowledge.knowledge_engine import KnowledgeEngine


_engine = KnowledgeEngine()


def build_knowledge(financial):

    return _engine.build(financial)