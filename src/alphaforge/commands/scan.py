from alphaforge.reporting.scan_report import ScanReport
from alphaforge.services.scan_service import load_watchlist, run_scan

DEFAULT_WATCHLIST_PATH = "data/watchlist.txt"


def scan(watchlist_path: str = DEFAULT_WATCHLIST_PATH, top_n: int = 3) -> None:

    tickers = load_watchlist(watchlist_path)

    if not tickers:
        print(
            f"Watchlist at '{watchlist_path}' is empty or not found. "
            f"Add tickers (one per line) and try again."
        )
        return

    print(f"Scanning {len(tickers)} ticker(s) from '{watchlist_path}'...")
    print()

    results = run_scan(tickers)

    ScanReport().render(results, top_n=top_n)
