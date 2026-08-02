"""
Stock Portfolio Tracker - Console application for building and saving
a stock portfolio from a predefined catalog of equities.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final, Iterable

# --- Configuration ------------------------------------------------------------

BANNER_WIDTH: Final[int] = 72
OUTPUT_DIR: Final[Path] = Path(__file__).resolve().parent
CSV_FILENAME: Final[str] = "portfolio.csv"
TXT_FILENAME: Final[str] = "portfolio.txt"

YES_RESPONSES: Final[frozenset[str]] = frozenset({"y", "yes"})
NO_RESPONSES: Final[frozenset[str]] = frozenset({"n", "no"})


@dataclass(frozen=True, slots=True)
class StockInfo:
    """Immutable record for a tradable stock in the catalog."""

    symbol: str
    company: str
    price: float


@dataclass(slots=True)
class Holding:
    """A stock position held in the portfolio."""

    stock: StockInfo
    quantity: int

    @property
    def total_value(self) -> float:
        """Return the market value of this holding."""
        return self.stock.price * self.quantity


# Hardcoded catalog: at least 15 stocks with symbol, company, and price.
_CATALOG_DATA: Final[tuple[tuple[str, str, float], ...]] = (
    ("AAPL", "Apple Inc.", 189.50),
    ("MSFT", "Microsoft Corporation", 415.20),
    ("GOOGL", "Alphabet Inc.", 171.30),
    ("AMZN", "Amazon.com Inc.", 186.40),
    ("NVDA", "NVIDIA Corporation", 875.60),
    ("META", "Meta Platforms Inc.", 502.80),
    ("TSLA", "Tesla Inc.", 248.90),
    ("JPM", "JPMorgan Chase & Co.", 198.75),
    ("V", "Visa Inc.", 278.40),
    ("JNJ", "Johnson & Johnson", 156.20),
    ("WMT", "Walmart Inc.", 68.35),
    ("PG", "Procter & Gamble Co.", 165.90),
    ("DIS", "The Walt Disney Company", 112.45),
    ("NFLX", "Netflix Inc.", 628.70),
    ("INTC", "Intel Corporation", 43.80),
    ("AMD", "Advanced Micro Devices Inc.", 162.15),
    ("BA", "The Boeing Company", 178.25),
)

STOCK_CATALOG: Final[dict[str, StockInfo]] = {
    symbol: StockInfo(symbol=symbol, company=company, price=price)
    for symbol, company, price in _CATALOG_DATA
}


# --- Input helpers ------------------------------------------------------------

def read_line(prompt: str) -> str:
    """
    Read a stripped line from the console.

    Raises:
        EOFError: When input ends unexpectedly.
        KeyboardInterrupt: When the user presses Ctrl+C.
    """
    try:
        return input(prompt).strip()
    except EOFError:
        print("\nInput ended unexpectedly.")
        raise


def ask_yes_no(prompt: str) -> bool:
    """
    Prompt until the user enters a yes or no response.

    Returns:
        True for yes, False for no or EOF.
    """
    while True:
        try:
            response = read_line(prompt).lower()
        except EOFError:
            return False

        if response in YES_RESPONSES:
            return True
        if response in NO_RESPONSES:
            return False

        print("Please enter 'y' for yes or 'n' for no.")


# --- Stock lookup -------------------------------------------------------------

def lookup_stock(symbol: str) -> StockInfo | None:
    """
    Find a stock by symbol using case-insensitive matching.

    Args:
        symbol: Ticker symbol entered by the user.

    Returns:
        Matching ``StockInfo``, or ``None`` if the symbol is unknown.
    """
    normalized = symbol.strip().upper()
    if not normalized:
        return None
    return STOCK_CATALOG.get(normalized)


def list_available_symbols() -> str:
    """Return a comma-separated list of valid ticker symbols."""
    return ", ".join(sorted(STOCK_CATALOG))


# --- Portfolio management -----------------------------------------------------

class Portfolio:
    """In-memory portfolio that merges duplicate symbol purchases."""

    def __init__(self) -> None:
        self._holdings: dict[str, Holding] = {}

    def add(self, stock: StockInfo, quantity: int) -> None:
        """
        Add shares to the portfolio, merging with an existing position.

        Args:
            stock: Stock to purchase.
            quantity: Number of shares (must be a positive integer).

        Raises:
            ValueError: If ``quantity`` is not positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        existing = self._holdings.get(stock.symbol)
        if existing:
            existing.quantity += quantity
        else:
            self._holdings[stock.symbol] = Holding(stock=stock, quantity=quantity)

    @property
    def holdings(self) -> list[Holding]:
        """Return holdings sorted alphabetically by symbol."""
        return sorted(self._holdings.values(), key=lambda item: item.stock.symbol)

    @property
    def is_empty(self) -> bool:
        """Return True when no holdings have been added."""
        return not self._holdings

    def grand_total(self) -> float:
        """Return the combined value of all holdings."""
        return sum(holding.total_value for holding in self.holdings)


# --- User prompts -------------------------------------------------------------

def prompt_for_symbol() -> StockInfo:
    """
    Prompt until the user enters a valid catalog symbol.

    Returns:
        The matching ``StockInfo`` record.
    """
    while True:
        symbol_input = read_line("Enter stock symbol: ")
        stock = lookup_stock(symbol_input)

        if stock is None:
            print(
                f"Invalid symbol '{symbol_input}'. "
                f"Available symbols: {list_available_symbols()}"
            )
            continue

        return stock


def prompt_for_quantity() -> int:
    """
    Prompt until the user enters a positive integer quantity.

    Returns:
        A valid share quantity.
    """
    while True:
        raw_quantity = read_line("Enter quantity (positive integer): ")

        if not raw_quantity:
            print("Quantity cannot be empty.")
            continue

        if not raw_quantity.isdigit():
            print("Invalid quantity. Enter a whole number greater than zero.")
            continue

        quantity = int(raw_quantity)
        if quantity <= 0:
            print("Quantity must be a positive integer.")
            continue

        return quantity


def prompt_add_more() -> bool:
    """Return True when the user wants to add another stock."""
    return ask_yes_no("Add another stock to this portfolio? (y/n): ")


# --- Formatting ---------------------------------------------------------------

def format_currency(amount: float) -> str:
    """Format a numeric amount as USD with thousands separators."""
    return f"${amount:,.2f}"


def build_table_rows(holdings: Iterable[Holding]) -> list[tuple[str, ...]]:
    """
    Build row tuples for tabular portfolio display and export.

    Each row contains: Symbol, Company, Price, Quantity, Total Value.
    """
    rows: list[tuple[str, ...]] = []
    for holding in holdings:
        rows.append(
            (
                holding.stock.symbol,
                holding.stock.company,
                format_currency(holding.stock.price),
                str(holding.quantity),
                format_currency(holding.total_value),
            )
        )
    return rows


def render_ascii_table(
    headers: tuple[str, ...],
    rows: list[tuple[str, ...]],
    footer: str | None = None,
) -> str:
    """
    Render an aligned ASCII table with borders.

    Column widths expand to fit the widest cell in each column.
    """
    if not rows:
        body = ["| (no holdings) |"]
        width = len(body[0])
        lines = [
            "+" + "-" * (width - 2) + "+",
            body[0],
            "+" + "-" * (width - 2) + "+",
        ]
        if footer:
            lines.append(footer)
        return "\n".join(lines)

    col_count = len(headers)
    widths = [len(header) for header in headers]

    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def border(sep_left: str = "+", sep_mid: str = "+", sep_right: str = "+") -> str:
        parts = [sep_left]
        for width in widths:
            parts.append("-" * (width + 2))
            parts.append(sep_mid)
        return "".join(parts[:-1]) + sep_right

    def format_row(cells: tuple[str, ...]) -> str:
        padded = [
            f" {cells[index]:<{widths[index]}} "
            for index in range(col_count)
        ]
        return "|" + "|".join(padded) + "|"

    lines = [border(), format_row(headers), border(sep_mid="+")]
    for row in rows:
        lines.append(format_row(row))
    lines.append(border())

    if footer:
        lines.append(footer)

    return "\n".join(lines)


def print_portfolio_table(portfolio: Portfolio) -> None:
    """Print a formatted ASCII table of the portfolio and grand total."""
    headers = ("Symbol", "Company", "Price", "Quantity", "Total Value")
    rows = build_table_rows(portfolio.holdings)
    footer = f"GRAND TOTAL: {format_currency(portfolio.grand_total())}".rjust(
        BANNER_WIDTH
    )
    print()
    print(render_ascii_table(headers, rows, footer=footer))
    print()


# --- Persistence --------------------------------------------------------------

def current_timestamp() -> str:
    """Return the current local time formatted for filenames and headers."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_slug() -> str:
    """Return a filesystem-safe timestamp for archived portfolio files."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_portfolio_csv(portfolio: Portfolio, filepath: Path, saved_at: str) -> None:
    """
    Write portfolio holdings to a CSV file.

    Args:
        portfolio: Portfolio to export.
        filepath: Destination CSV path.
        saved_at: Human-readable save timestamp for metadata row.
    """
    headers = ("Symbol", "Company", "Price", "Quantity", "Total Value")

    with filepath.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Saved At", saved_at])
        writer.writerow([])
        writer.writerow(headers)

        for holding in portfolio.holdings:
            writer.writerow(
                [
                    holding.stock.symbol,
                    holding.stock.company,
                    f"{holding.stock.price:.2f}",
                    holding.quantity,
                    f"{holding.total_value:.2f}",
                ]
            )

        writer.writerow([])
        writer.writerow(["Grand Total", f"{portfolio.grand_total():.2f}"])


def save_portfolio_txt(portfolio: Portfolio, filepath: Path, saved_at: str) -> None:
    """
    Write portfolio holdings to a plain-text report file.

    Args:
        portfolio: Portfolio to export.
        filepath: Destination text path.
        saved_at: Human-readable save timestamp for the report header.
    """
    headers = ("Symbol", "Company", "Price", "Quantity", "Total Value")
    rows = build_table_rows(portfolio.holdings)
    footer = f"GRAND TOTAL: {format_currency(portfolio.grand_total())}".rjust(
        BANNER_WIDTH
    )

    report_lines = [
        "STOCK PORTFOLIO REPORT",
        f"Saved At: {saved_at}",
        "",
        render_ascii_table(headers, rows, footer=footer),
        "",
    ]

    filepath.write_text("\n".join(report_lines), encoding="utf-8")


def save_portfolio(portfolio: Portfolio) -> None:
    """
    Save the portfolio to timestamped and standard output files.

    Creates:
        - portfolio.csv / portfolio.txt (latest save)
        - portfolio_<timestamp>.csv / portfolio_<timestamp>.txt (archive)
    """
    saved_at = current_timestamp()
    slug = timestamp_slug()

    csv_path = OUTPUT_DIR / CSV_FILENAME
    txt_path = OUTPUT_DIR / TXT_FILENAME
    archive_csv = OUTPUT_DIR / f"portfolio_{slug}.csv"
    archive_txt = OUTPUT_DIR / f"portfolio_{slug}.txt"

    try:
        save_portfolio_csv(portfolio, csv_path, saved_at)
        save_portfolio_txt(portfolio, txt_path, saved_at)
        save_portfolio_csv(portfolio, archive_csv, saved_at)
        save_portfolio_txt(portfolio, archive_txt, saved_at)
    except OSError as exc:
        print(f"Error saving portfolio: {exc}", file=sys.stderr)
        return

    print("\nPortfolio saved successfully.")
    print(f"  Timestamp : {saved_at}")
    print(f"  CSV       : {csv_path.name}")
    print(f"  Text      : {txt_path.name}")
    print(f"  Archive   : {archive_csv.name}, {archive_txt.name}")


# --- Application flow ---------------------------------------------------------

def print_welcome() -> None:
    """Display the application title and brief instructions."""
    border = "=" * BANNER_WIDTH
    print(f"\n{border}")
    print("STOCK PORTFOLIO TRACKER".center(BANNER_WIDTH))
    print(border)
    print("Build a portfolio from the catalog below.")
    print(f"Available symbols ({len(STOCK_CATALOG)}): {list_available_symbols()}")
    print("Press Ctrl+C at any time to exit.\n")


def build_portfolio() -> Portfolio:
    """
    Interactively collect holdings and return a populated portfolio.

    Returns:
        A ``Portfolio`` instance containing user-selected holdings.
    """
    portfolio = Portfolio()

    while True:
        try:
            stock = prompt_for_symbol()
            quantity = prompt_for_quantity()
        except ValueError as exc:
            print(exc)
            continue

        portfolio.add(stock, quantity)
        print(
            f"Added {quantity} share(s) of {stock.symbol} "
            f"({stock.company}) at {format_currency(stock.price)} each."
        )

        if not prompt_add_more():
            break

    return portfolio


def run_portfolio_session() -> None:
    """Build one portfolio, display it, and optionally save it."""
    portfolio = build_portfolio()

    if portfolio.is_empty:
        print("\nNo stocks were added to the portfolio.")
        return

    print_portfolio_table(portfolio)

    if ask_yes_no("Save this portfolio to file? (y/n): "):
        save_portfolio(portfolio)


def main() -> None:
    """Entry point for the Stock Portfolio Tracker."""
    print_welcome()

    try:
        while True:
            run_portfolio_session()

            if not ask_yes_no("\nBuild another portfolio? (y/n): "):
                break
    except (KeyboardInterrupt, EOFError):
        print()

    print("\nThank you for using Stock Portfolio Tracker. Goodbye!")


if __name__ == "__main__":
    main()
