def format_money(value: float | int | None) -> str:
    """
    Convert large numbers to K / M / B / T format.
    """

    if value is None:
        return "-"

    negative = value < 0
    value = abs(value)

    if value >= 1_000_000_000_000:
        result = f"${value/1_000_000_000_000:.2f}T"

    elif value >= 1_000_000_000:
        result = f"${value/1_000_000_000:.2f}B"

    elif value >= 1_000_000:
        result = f"${value/1_000_000:.2f}M"

    elif value >= 1_000:
        result = f"${value/1_000:.2f}K"

    else:
        result = f"${value:.2f}"

    if negative:
        result = "-" + result

    return result


def format_percent(value: float | None) -> str:

    if value is None:
        return "-"

    return f"{value * 100:.2f}%"


def format_number(value: float | int | None) -> str:

    if value is None:
        return "-"

    return f"{value:,.2f}"