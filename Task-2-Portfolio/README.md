# Stock Portfolio Tracker

> A professional console application for building, viewing, and saving stock portfolios.

Build a portfolio from a predefined catalog of 17 equities, view a formatted summary table, and export results to CSV and plain-text files.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Output Files](#output-files)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Project Overview

The Stock Portfolio Tracker lets users assemble a personal stock portfolio by selecting symbols from a hardcoded catalog and specifying share quantities. Duplicate purchases of the same symbol are merged automatically. When finished, the application displays an ASCII table with per-holding values and a grand total, then optionally saves the report to disk.

The program is written in Python 3.11+ using only the standard library, with modular functions, type hints, docstrings, and robust input validation.

---

## Features

| Feature | Description |
| --- | --- |
| Stock catalog | 17 predefined stocks with symbol, company name, and price |
| Case-insensitive lookup | Symbols such as `aapl` and `AAPL` resolve identically |
| Repeated additions | Add as many holdings as needed in one session |
| Quantity validation | Accepts only positive integers |
| Invalid symbol rejection | Unknown tickers are rejected with available symbols shown |
| Duplicate merging | Additional shares of the same symbol update quantity in place |
| ASCII table | Aligned columns for Symbol, Company, Price, Quantity, Total Value |
| Grand total | Combined portfolio value displayed below the table |
| File export | Saves to `portfolio.csv` and `portfolio.txt` |
| Timestamped archives | Also writes `portfolio_YYYYMMDD_HHMMSS.csv/.txt` |
| Save prompt | User chooses whether to persist each portfolio |
| Replay loop | Option to build another portfolio without restarting |
| Error handling | Graceful handling of invalid input, I/O errors, Ctrl+C, and EOF |

---

## Folder Structure

```text
Task-2-Portfolio/
├── main.py          # Application source code
├── README.md        # Project documentation
├── portfolio.csv    # Latest portfolio export (created on save)
├── portfolio.txt    # Latest text report (created on save)
└── portfolio_*.csv  # Timestamped archive copies (created on save)
    portfolio_*.txt
```

---

## Requirements

- **Python 3.11+**
- No third-party packages (standard library only)

---

## Installation

1. Clone or download this repository.
2. Open a terminal and navigate to the project folder:

   ```bash
   cd Task-2-Portfolio
   ```

3. Confirm Python 3.11 or newer is installed:

   ```bash
   python --version
   ```

---

## Usage

Run the application from the `Task-2-Portfolio` directory:

```bash
python main.py
```

### Workflow

1. Enter a **stock symbol** (case-insensitive).
2. Enter a **quantity** (positive whole number).
3. Choose whether to **add another stock**.
4. Review the **formatted portfolio table** and grand total.
5. Choose whether to **save** to file.
6. Choose whether to **build another portfolio**.

Press **Ctrl+C** at any time to exit.

### Available Symbols

`AAPL`, `AMD`, `AMZN`, `BA`, `DIS`, `GOOGL`, `INTC`, `JNJ`, `JPM`, `META`, `MSFT`, `NFLX`, `NVDA`, `PG`, `TSLA`, `V`, `WMT`

---

## Sample Output

```text
========================================================================
                        STOCK PORTFOLIO TRACKER
========================================================================
Build a portfolio from the catalog below.
Available symbols (17): AAPL, AMD, AMZN, BA, DIS, GOOGL, INTC, JNJ, ...
Press Ctrl+C at any time to exit.

Enter stock symbol: aapl
Enter quantity (positive integer): 10
Added 10 share(s) of AAPL (Apple Inc.) at $189.50 each.
Add another stock to this portfolio? (y/n): y
Enter stock symbol: msft
Enter quantity (positive integer): 5
Added 5 share(s) of MSFT (Microsoft Corporation) at $415.20 each.
Add another stock to this portfolio? (y/n): y
Enter stock symbol: aapl
Enter quantity (positive integer): 2
Added 2 share(s) of AAPL (Apple Inc.) at $189.50 each.
Add another stock to this portfolio? (y/n): n

+--------+----------------------------+-----------+----------+-------------+
| Symbol | Company                    | Price     | Quantity | Total Value |
+--------+----------------------------+-----------+----------+-------------+
| AAPL   | Apple Inc.                 | $189.50   | 12       | $2,274.00   |
| MSFT   | Microsoft Corporation      | $415.20   | 5        | $2,076.00   |
+--------+----------------------------+-----------+----------+-------------+
                                              GRAND TOTAL: $4,350.00

Save this portfolio to file? (y/n): y

Portfolio saved successfully.
  Timestamp : 2026-08-02 23:45:10
  CSV       : portfolio.csv
  Text      : portfolio.txt
  Archive   : portfolio_20260802_234510.csv, portfolio_20260802_234510.txt

Build another portfolio? (y/n): n

Thank you for using Stock Portfolio Tracker. Goodbye!
```

---

## Output Files

### `portfolio.csv`

CSV export with a save timestamp, column headers, holding rows, and a grand total row.

### `portfolio.txt`

Human-readable report with the same timestamp and ASCII table shown in the console.

### Timestamped archives

Each save also creates `portfolio_YYYYMMDD_HHMMSS.csv` and `.txt` files so previous exports are preserved.

---

## Future Improvements

- Load stock prices from a live API or external CSV file
- Support fractional share quantities
- Portfolio performance tracking over time
- Sort and filter holdings in the display table
- JSON export format
- Load and edit previously saved portfolios
- Unit tests for portfolio math and file export logic

---

## License

This project is part of the CodeAlpha Python internship tasks and is provided for educational purposes. Feel free to use, modify, and distribute with attribution.
