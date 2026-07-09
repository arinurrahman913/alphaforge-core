import sys

from alphaforge.commands.analyze import analyze
from alphaforge.commands.scan import scan
from alphaforge.foundation.version import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
)


def run() -> None:

    args = sys.argv

    if len(args) >= 3:

        command = args[1]

        if command == "analyze":
            analyze(args[2])
            return

        if command == "scan":
            scan(args[2])
            return

    print("=" * 34)
    print(f"      {APP_NAME} v{APP_VERSION}")
    print("=" * 34)
    print()
    print(APP_DESCRIPTION)
    print()
    print("Usage:")
    print("python -m alphaforge.main analyze <ticker>")
    print("python -m alphaforge.main scan <watchlist_file>")
