from alphaforge.foundation.version import APP_NAME, APP_VERSION


class ScanReport:
    """
    Renders scan results as a ranking table, followed by a detailed
    breakdown for the top N candidates. A full per-ticker detail block
    (like ConsoleReport for `analyze`) isn't printed for every ticker —
    with 50-100 tickers that would be unreadable. The table gives the
    overview; the detail section gives the "why" for whichever
    candidates are actually worth reading about.
    """

    def render(self, results: list, top_n: int = 3) -> None:

        print("=" * 80)
        print(f"{APP_NAME} v{APP_VERSION}".center(80))
        print("=" * 80)
        print()
        print("Investment Intelligence Operating System")
        print()

        print("=" * 80)
        print(f"SCAN RESULTS — {len(results)} tickers analyzed")
        print("=" * 80)
        print()

        self._render_table(results)

        failed = [r for r in results if r.errors]

        if failed:
            print()
            print(
                f"Note: {len(failed)} ticker(s) had partial data errors "
                f"(see detail below)."
            )

        print()

        for result in results[:top_n]:
            self._render_detail(result)

        print("=" * 80)
        print(
            f"Scan complete. {len(results)} tickers processed, "
            f"{len(failed)} with errors."
        )
        print("=" * 80)

    def _render_table(self, results: list) -> None:

        # Explicit trailing space on every field (not just relying on
        # the width to leave a gap) so columns never run together even
        # if a value is longer than its field width — e.g. an unusual
        # ticker or a long institutional label.
        columns = (
            f"{'Rank':<5} {'Ticker':<7} {'Composite':<10} "
            f"{'Financial':<16} {'Technical':<18} {'Institutional':<24}"
        )

        print(columns)
        print("-" * len(columns))

        for i, result in enumerate(results, start=1):

            financial_label = "-"
            if result.financial_score is not None:
                financial_label = (
                    f"{result.financial_score.grade} "
                    f"({result.financial_score.total}/"
                    f"{result.financial_score.maximum})"
                )

            technical_label = result.technical_trend or "-"
            institutional_label = self._institutional_label(result)

            print(
                f"{i:<5} {result.ticker:<7} {result.composite_score:<10} "
                f"{financial_label:<16} {technical_label:<18} "
                f"{institutional_label:<24}"
            )

    def _institutional_label(self, result) -> str:

        ownership = result.institutional_ownership

        if ownership is None or ownership.total_funds_holding == 0:
            return "NONE"

        count = ownership.total_funds_holding
        fund_word = "fund" if count == 1 else "funds"

        return f"{result.institutional_signal} ({count} {fund_word})"

    def _render_detail(self, result) -> None:

        print("=" * 80)
        label = result.company_name or result.ticker
        print(f"CANDIDATE DETAIL — {result.ticker} ({label})")
        print("=" * 80)
        print(f"Composite Score : {result.composite_score} / 100")
        print()

        if result.financial_score is not None:
            print(
                f"Financial     : {result.financial_score.total}/"
                f"{result.financial_score.maximum} "
                f"(Grade {result.financial_score.grade})"
            )

        if result.technical_trend is not None:
            print(f"Technical     : {result.technical_trend}")

        ownership = result.institutional_ownership

        if ownership is not None and ownership.total_funds_holding > 0:
            print("Institutional :")

            for position in ownership.positions:
                if position.current_holding is None and position.change_type != "SOLD_OUT":
                    continue

                print(f"   - {position.fund_name:<32} {position.change_type}")

        if result.flags:
            print()
            print("Flags")
            print("-" * 5)
            for flag in result.flags:
                print(f"  + {flag}")

        if result.errors:
            print()
            print("Errors (partial data)")
            print("-" * 21)
            for error in result.errors:
                print(f"  ! {error}")

        print()
