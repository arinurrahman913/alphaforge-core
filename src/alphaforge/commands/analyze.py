from alphaforge.services.analyze_service import AnalyzeService
from alphaforge.reporting.console_report import ConsoleReport


def analyze(ticker: str):

    service = AnalyzeService()

    result = service.run(ticker)

    ConsoleReport().render(result)