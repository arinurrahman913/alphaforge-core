class ScanReport:

    def render(self, results: list, top_n: int | None = None) -> None:

        if top_n is not None:
            results = results[:top_n]

        print("=" * 100)
        print("SCAN RESULTS".center(100))
        print("=" * 100)
        print()
        print(
            "Composite score is a heuristic ranking (financial + technical "
            "+ institutional signal),"
        )
        print(
            "not a validated prediction model. Use it to prioritize deeper "
            "research, not as a buy signal."
        )
        print()

        header = (
            f"{'#':<4}{'Ticker':<8}{'Company':<24}{'Cap':<7}{'Grade':<7}"
            f"{'Trend':<18}{'Inst. New':<10}{'Score':>8}"
        )
        print(header)
        print("-" * 100)

        for rank, r in enumerate(results, start=1):

            grade = r.financial_grade or "-"
            trend = (r.technical_trend or "-")[:17]
            company = (r.company_name or r.ticker)[:22]

            print(
                f"{rank:<4}{r.ticker:<8}{company:<24}{r.cap_category:<7}{grade:<7}"
                f"{trend:<18}{r.institutional_new_positions:<10}"
                f"{r.composite_score:>8.1f}"
            )

        print("-" * 100)
        print()

        failed = [r for r in results if not r.has_data]

        if failed:
            print(f"{len(failed)} ticker(s) returned no usable data:")
            for r in failed:
                reasons = "; ".join(r.errors) if r.errors else "unknown error"
                print(f"  {r.ticker}: {reasons}")
            print()

        top_new_positions = [
            r for r in results if r.institutional_new_positions > 0
        ]

        if top_new_positions:
            print("New institutional positions this quarter:")
            for r in top_new_positions:
                print(
                    f"  {r.ticker} — {r.institutional_new_positions} "
                    f"tracked fund(s) opened a new position"
                )
            print()
