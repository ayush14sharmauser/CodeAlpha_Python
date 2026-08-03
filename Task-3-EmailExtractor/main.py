"""
Email Extractor - Console application that reads text from a file,
extracts email addresses with regular expressions, validates them,
and saves the cleaned results to an output file.
"""

from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterable

# --- Configuration ------------------------------------------------------------

BANNER_WIDTH: Final[int] = 72
APP_DIR: Final[Path] = Path(__file__).resolve().parent
INPUT_FILE: Final[Path] = APP_DIR / "input.txt"
OUTPUT_FILE: Final[Path] = APP_DIR / "output.txt"

# Pattern to locate email-like tokens in free-form text.
EMAIL_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

# Stricter pattern used for final validation after extraction.
STRICT_EMAIL_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


@dataclass(frozen=True, slots=True)
class ExtractionReport:
    """Summary statistics produced by an extraction run."""

    total_found: int
    unique_valid: int
    invalid_ignored: int
    duplicates_removed: int
    valid_emails: tuple[str, ...]


# --- File I/O -----------------------------------------------------------------

def read_input_file(filepath: Path) -> str:
    """
    Read and return the full contents of the input file.

    Args:
        filepath: Path to the source text file.

    Returns:
        File contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read.
    """
    if not filepath.is_file():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    return filepath.read_text(encoding="utf-8")


def write_output_file(filepath: Path, emails: Iterable[str]) -> None:
    """
    Write one email address per line to the output file.

    Args:
        filepath: Destination file path.
        emails: Validated email addresses to persist.

    Raises:
        OSError: If the file cannot be written.
    """
    content = "\n".join(emails)
    if content:
        content += "\n"
    filepath.write_text(content, encoding="utf-8")


# --- Extraction and validation ------------------------------------------------

def extract_email_candidates(text: str) -> list[str]:
    """
    Find all email-like substrings in ``text`` using regular expressions.

    Args:
        text: Raw input text.

    Returns:
        A list of candidate email strings in discovery order.
    """
    return EMAIL_PATTERN.findall(text)


def is_valid_email(email: str) -> bool:
    """
    Validate an extracted email with additional structural rules.

    Rejects addresses with consecutive dots, leading/trailing dots in
    the local or domain part, invalid label placement, or malformed TLDs.

    Args:
        email: Candidate email string.

    Returns:
        True when the email passes validation, False otherwise.
    """
    if not STRICT_EMAIL_PATTERN.fullmatch(email):
        return False

    local_part, domain = email.rsplit("@", 1)

    if not local_part or not domain:
        return False

    if ".." in email:
        return False

    if local_part.startswith(".") or local_part.endswith("."):
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    if domain.startswith("-") or domain.endswith("-"):
        return False

    tld = domain.rsplit(".", 1)[-1]
    if not tld.isalpha() or len(tld) < 2:
        return False

    domain_labels = domain.split(".")
    if any(not label or label.startswith("-") or label.endswith("-") for label in domain_labels):
        return False

    return True


def process_candidates(candidates: list[str]) -> ExtractionReport:
    """
    Validate, deduplicate, and sort extracted email candidates.

    Duplicate detection is case-insensitive. Valid emails are returned
    in lowercase sorted alphabetical order.

    Args:
        candidates: Raw regex matches from the input text.

    Returns:
        An ``ExtractionReport`` with statistics and cleaned emails.
    """
    total_found = len(candidates)
    invalid_ignored = 0
    duplicates_removed = 0
    seen: set[str] = set()
    valid_emails: list[str] = []

    for candidate in candidates:
        if not is_valid_email(candidate):
            invalid_ignored += 1
            continue

        normalized = candidate.lower()
        if normalized in seen:
            duplicates_removed += 1
            continue

        seen.add(normalized)
        valid_emails.append(normalized)

    valid_emails.sort()

    return ExtractionReport(
        total_found=total_found,
        unique_valid=len(valid_emails),
        invalid_ignored=invalid_ignored,
        duplicates_removed=duplicates_removed,
        valid_emails=tuple(valid_emails),
    )


# --- Console output -----------------------------------------------------------

def print_banner() -> None:
    """Print the application title banner."""
    border = "=" * BANNER_WIDTH
    print(f"\n{border}")
    print("EMAIL EXTRACTOR".center(BANNER_WIDTH))
    print(border)


def print_section(title: str) -> None:
    """Print a section heading."""
    print(f"\n{title}")
    print("-" * len(title))


def print_report(report: ExtractionReport, elapsed_seconds: float) -> None:
    """
    Display extraction statistics and the list of valid emails.

    Args:
        report: Extraction results and summary counts.
        elapsed_seconds: Total runtime for the extraction process.
    """
    print_section("Extraction Summary")
    print(f"  Total emails found     : {report.total_found}")
    print(f"  Unique valid emails    : {report.unique_valid}")
    print(f"  Invalid entries ignored: {report.invalid_ignored}")
    print(f"  Duplicates removed     : {report.duplicates_removed}")
    print(f"  Execution time         : {elapsed_seconds:.4f} seconds")

    print_section("Valid Emails")
    if report.valid_emails:
        for email in report.valid_emails:
            print(f"  {email}")
    else:
        print("  (none)")


def print_file_status(input_path: Path, output_path: Path) -> None:
    """Print input and output file paths."""
    print_section("Files")
    print(f"  Input : {input_path}")
    print(f"  Output: {output_path}")


# --- Application flow ---------------------------------------------------------

def run_extraction() -> int:
    """
    Execute the full email extraction workflow.

    Returns:
        Process exit code (0 for success, 1 for failure).
    """
    print_banner()
    print_file_status(INPUT_FILE, OUTPUT_FILE)

    start_time = time.perf_counter()

    try:
        text = read_input_file(INPUT_FILE)
    except FileNotFoundError as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        print(
            f"Create an '{INPUT_FILE.name}' file in {APP_DIR} and run again.",
            file=sys.stderr,
        )
        return 1
    except OSError as exc:
        print(f"\nError reading input file: {exc}", file=sys.stderr)
        return 1

    candidates = extract_email_candidates(text)
    report = process_candidates(candidates)

    try:
        write_output_file(OUTPUT_FILE, report.valid_emails)
    except OSError as exc:
        print(f"\nError writing output file: {exc}", file=sys.stderr)
        return 1

    elapsed = time.perf_counter() - start_time
    print_report(report, elapsed)

    print(f"\nSaved {report.unique_valid} email(s) to '{OUTPUT_FILE.name}'.")
    print("\nEmail extraction completed successfully.\n")
    return 0


def main() -> None:
    """Entry point for the Email Extractor application."""
    exit_code = run_extraction()
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
