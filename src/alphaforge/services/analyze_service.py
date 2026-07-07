from alphaforge.engine.analysis_engine import AnalysisEngine


class AnalyzeService:
    """
    Main orchestration service.

    Temporary wrapper around AnalysisEngine.
    This keeps backward compatibility with Sprint 003.
    """

    def __init__(self):

        self.engine = AnalysisEngine()

    def run(self, ticker: str):

        return self.engine.run(ticker)