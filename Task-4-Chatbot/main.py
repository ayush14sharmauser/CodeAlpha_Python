"""
CodeAlpha Task 4 - Production-Quality Python Console Chatbot.

A modular, type-hinted, standard-library-only chatbot with a variety
of useful commands: greetings, date/time/day lookups, calculator,
jokes, quotes, help, and a friendly command loop.
"""

from __future__ import annotations

import random
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from typing import Callable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BOT_NAME: str = "PyBot"
BOT_VERSION: str = "1.0.0"


# ---------------------------------------------------------------------------
# Data: Jokes and Quotes
# ---------------------------------------------------------------------------

JOKES: List[str] = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "How many programmers does it take to change a light bulb? "
    "None - that's a hardware problem.",
    "Why did the developer go broke? Because he used up all his cache.",
    "A SQL query walks into a bar, sees two tables and asks: "
    "\"Can I join you?\"",
    "Why do Java developers wear glasses? Because they don't C#.",
    "There are 10 types of people in the world: those who understand "
    "binary and those who don't.",
    "Why was the JavaScript developer sad? Because he didn't Node "
    "how to Express himself.",
    "Programmer's wife: \"Go to the store and buy a loaf of bread. "
    "If they have eggs, get a dozen.\" - He came home with 12 loaves "
    "of bread.",
    "Why did the Python programmer get rejected at a job interview? "
    "He couldn't handle Java exceptions.",
    "What's a programmer's favorite hangout place? Foo Bar.",
    "Debugging: Being the detective in a crime movie where you are "
    "also the murderer.",
    "Why do programmers always mix up Halloween and Christmas? "
    "Because Oct 31 equals Dec 25.",
]

QUOTES: List[str] = [
    "\"The only way to do great work is to love what you do.\" "
    "- Steve Jobs",
    "\"Code is like humor. When you have to explain it, it's bad.\" "
    "- Cory House",
    "\"First, solve the problem. Then, write the code.\" - John Johnson",
    "\"Experience is the name everyone gives to their mistakes.\" "
    "- Oscar Wilde",
    "\"The best error message is the one that never shows up.\" "
    "- Thomas Fuchs",
    "\"Simplicity is the soul of efficiency.\" - Austin Freeman",
    "\"Make it work, make it right, make it fast.\" - Kent Beck",
    "\"Before software can be reusable it first has to be usable.\" "
    "- Ralph Johnson",
    "\"Programs must be written for people to read, and only "
    "incidentally for machines to execute.\" - Harold Abelson",
    "\"Any fool can write code that a computer can understand. "
    "Good programmers write code that humans can understand.\" "
    "- Martin Fowler",
    "\"Talk is cheap. Show me the code.\" - Linus Torvalds",
    "\"Learning to write programs stretches your mind, and helps "
    "you think better.\" - Bill Gates",
]


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


class Colors:
    """ANSI escape codes for attractive console formatting."""

    RESET: str = "\033[0m"
    BOLD: str = "\033[1m"
    DIM: str = "\033[2m"

    RED: str = "\033[31m"
    GREEN: str = "\033[32m"
    YELLOW: str = "\033[33m"
    BLUE: str = "\033[34m"
    MAGENTA: str = "\033[35m"
    CYAN: str = "\033[36m"
    WHITE: str = "\033[37m"


def _supports_color() -> bool:
    """Return True if the terminal appears to support ANSI colors."""
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    if sys.platform.startswith("win"):
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            STD_OUTPUT_HANDLE = -11
            handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            mode = ctypes.c_ulong()
            if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                return False
            new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(handle, new_mode)
            return True
        except Exception:
            return False
    return True


_COLOR_SUPPORTED: bool = _supports_color()


def _c(text: str, color: str, bold: bool = False) -> str:
    """Return *text* wrapped in the given color code (if supported)."""
    if not _COLOR_SUPPORTED:
        return text
    prefix = ""
    if bold:
        prefix += Colors.BOLD
    prefix += color
    return f"{prefix}{text}{Colors.RESET}"


def banner(text: str, width: int = 60, char: str = "=") -> str:
    """Return *text* centered inside a banner line of *width* chars."""
    return text.center(width, char)


def separator(width: int = 60, char: str = "-") -> str:
    """Return a horizontal separator string."""
    return char * width


# ---------------------------------------------------------------------------
# Input / Output wrappers
# ---------------------------------------------------------------------------


def print_bot(message: str) -> None:
    """Print a bot response with friendly formatting."""
    label = _c(f"[{BOT_NAME}]", Colors.CYAN, bold=True)
    print(f"\n{label} {message}\n")


def print_error(message: str) -> None:
    """Print an error message with red formatting."""
    label = _c("[Error]", Colors.RED, bold=True)
    print(f"\n{label} {message}\n")


def print_info(message: str) -> None:
    """Print an informational message with yellow formatting."""
    label = _c("[Info]", Colors.YELLOW, bold=True)
    print(f"\n{label} {message}\n")


def prompt_user() -> str:
    """Prompt the user for input and return the stripped string."""
    prefix = _c("[You]", Colors.GREEN, bold=True)
    try:
        raw = input(f"{prefix} ")
    except EOFError:
        return "bye"
    return raw.strip()


# ---------------------------------------------------------------------------
# Normalization & matching
# ---------------------------------------------------------------------------


def normalize_input(text: str) -> str:
    """Normalize user input: strip whitespace, collapse internal spaces.

    Parameters
    ----------
    text : str
        The raw user input string.

    Returns
    -------
    str
        A lowercase copy of *text* with leading/trailing whitespace
        removed and any run of internal whitespace collapsed to a
        single space.
    """
    lowered = text.lower()
    collapsed = re.sub(r"\s+", " ", lowered)
    return collapsed.strip()


def contains_any(text: str, keywords: Tuple[str, ...]) -> bool:
    """Return True if *text* contains any of the given *keywords*."""
    return any(keyword in text for keyword in keywords)


def equals_any(text: str, keywords: Tuple[str, ...]) -> bool:
    """Return True if *text* exactly equals any of the given *keywords*."""
    return any(text == keyword for keyword in keywords)


# ---------------------------------------------------------------------------
# Calculator
# ---------------------------------------------------------------------------


# Characters allowed inside a calculator expression.
_CALC_ALLOWED = set("0123456789+-*/(). ")

# Arithmetic operators that separate terms.
_CALC_OPERATORS = frozenset("+-*/")


def _balanced_parentheses(text: str) -> bool:
    """Return True if every '(' in *text* has a matching ')'.

    Also ensures no closing parenthesis appears before its opening one.
    """
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def _contains_operator(text: str) -> bool:
    """Return True when *text* contains at least one arithmetic operator."""
    # Skip a leading minus sign that is a unary (not an infix operator).
    stripped = text.strip()
    if stripped.startswith("-"):
        stripped = stripped[1:]
    return any(op in stripped for op in _CALC_OPERATORS)


def is_calculator_expression(text: str) -> bool:
    """Return True if *text* looks like a math expression we can evaluate.

    Parameters
    ----------
    text : str
        The normalized user input string.

    Returns
    -------
    bool
        True if the text looks like a safe arithmetic expression using only
        digits, spaces, parentheses, and the + - * / operators, with
        balanced parentheses and at least one infix operator.
    """
    if not text:
        return False
    if not set(text) <= _CALC_ALLOWED:
        return False
    if not _balanced_parentheses(text):
        return False
    if not _contains_operator(text):
        return False
    # Quick structural check: empty parentheses "()" are never valid.
    if "()" in text:
        return False
    return True


def calculate(expression: str) -> Optional[float]:
    """Safely evaluate an arithmetic expression string.

    Only supports numbers, parentheses, +, -, *, / operators.
    Returns ``None`` if evaluation fails for any reason.

    Parameters
    ----------
    expression : str
        A simple arithmetic expression such as ``"2 + 5 * 3"``.

    Returns
    -------
    float or None
        The numeric result, or ``None`` on failure.
    """
    if not is_calculator_expression(expression):
        return None
    try:
        result = eval(  # noqa: S307
            expression,
            {"__builtins__": {}},
            {},
        )
    except ZeroDivisionError:
        raise
    except (SyntaxError, TypeError, NameError, OverflowError, ValueError):
        return None
    if isinstance(result, (int, float)):
        return float(result)
    return None


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


@dataclass
class Command:
    """Represents a command understood by the chatbot."""

    name: str
    keywords: Tuple[str, ...]
    description: str
    handler: Callable[[str], str]


def _random_response(options: List[str]) -> str:
    """Pick a single random element from *options*."""
    return random.choice(options)


def handle_greeting(_: str) -> str:
    """Generate a friendly greeting response."""
    greetings = [
        "Hello! Great to see you today. How can I help?",
        "Hi there! I hope you're having an awesome day!",
        "Hey! Nice to meet you - what can I do for you?",
        "Greetings! I'm ready whenever you are.",
        "Hello, hello! Let's chat. What's on your mind?",
    ]
    return _random_response(greetings)


def handle_how_are_you(_: str) -> str:
    """Generate a response for \"how are you\"."""
    responses = [
        "I'm doing fantastic, thank you for asking! How about you?",
        "Feeling great - all circuits working perfectly! :-)",
        "I'm wonderful! Every day is a good day to chat with you.",
        "Running smoothly and ready to help! Thanks for asking.",
    ]
    return _random_response(responses)


def handle_time(_: str) -> str:
    """Return a formatted current-time string."""
    now = datetime.now()
    fmt = now.strftime("%I:%M:%S %p")
    return f"The current time is {_c(fmt, Colors.BLUE, bold=True)}."


def handle_date(_: str) -> str:
    """Return a formatted current-date string."""
    today = date.today()
    fmt = today.strftime("%B %d, %Y")
    return f"Today's date is {_c(fmt, Colors.BLUE, bold=True)}."


def handle_day(_: str) -> str:
    """Return a formatted current-weekday string."""
    today = date.today()
    day_name = today.strftime("%A")
    return f"Today is {_c(day_name, Colors.BLUE, bold=True)}."


def handle_name(_: str) -> str:
    """Return the bot's name and version."""
    return (
        f"My name is {_c(BOT_NAME, Colors.MAGENTA, bold=True)} "
        f"(version {BOT_VERSION}). I'm a friendly Python console chatbot!"
    )


def handle_joke(_: str) -> str:
    """Return a random programmer joke."""
    return _random_response(JOKES)


def handle_quote(_: str) -> str:
    """Return a random motivational quote."""
    return _random_response(QUOTES)


def handle_help(_: str) -> str:
    """Return a formatted help message listing every command."""
    lines: List[str] = []
    lines.append(_c("Available Commands:", Colors.CYAN, bold=True))
    lines.append("")
    for cmd in _ALL_COMMANDS:
        kw = ", ".join(f"'{k}'" for k in cmd.keywords)
        lines.append(f"  {_c(cmd.name, Colors.YELLOW, bold=True)}:")
        lines.append(f"    Keywords: {kw}")
        lines.append(f"    {cmd.description}")
        lines.append("")
    lines.append("Tip: You can also type a math expression such as "
                 "`2 + 5 * 3` and I'll calculate it for you!")
    return "\n".join(lines)


def handle_unknown(text: str) -> str:
    """Generate a friendly \"I didn't understand\" response."""
    templates = [
        "Hmm, I'm not quite sure what you mean by \"{}\". "
        "Type 'help' to see what I can do!",
        "I didn't catch that - \"{}\" isn't something I know. "
        "How about typing 'help' for a list of commands?",
        "Sorry! I don't have a command for \"{}\". "
        "Try 'joke', 'time', 'quote', or 'help' to get started.",
    ]
    return _random_response(templates).format(text)


# ---------------------------------------------------------------------------
# Command registry
# ---------------------------------------------------------------------------

# NOTE: The greeting command intentionally has loose keyword handling
# (see ``dispatch`` below), so the keywords here are a best-effort list.
_ALL_COMMANDS: List[Command] = [
    Command(
        name="Greeting",
        keywords=("hello", "hi", "hey"),
        description="Say hello and start a friendly conversation.",
        handler=handle_greeting,
    ),
    Command(
        name="How Are You",
        keywords=("how are you", "how r u", "how's it going"),
        description="Ask the bot how it's doing.",
        handler=handle_how_are_you,
    ),
    Command(
        name="Time",
        keywords=("time", "current time", "what time is it"),
        description="Tell the current local time.",
        handler=handle_time,
    ),
    Command(
        name="Date",
        keywords=("date", "current date", "what date is it", "what is the date"),
        description="Tell today's date.",
        handler=handle_date,
    ),
    Command(
        name="Day",
        keywords=("day", "current day", "what day is it", "what is the day"),
        description="Tell the current day of the week.",
        handler=handle_day,
    ),
    Command(
        name="Name",
        keywords=("your name", "what is your name", "who are you"),
        description="Tell the bot's name and version.",
        handler=handle_name,
    ),
    Command(
        name="Joke",
        keywords=("joke", "tell me a joke", "another joke"),
        description="Tell a random programming joke.",
        handler=handle_joke,
    ),
    Command(
        name="Quote",
        keywords=("quote", "motivate me", "motivational quote"),
        description="Share a random motivational quote.",
        handler=handle_quote,
    ),
    Command(
        name="Help",
        keywords=("help", "commands", "what can you do", "help me"),
        description="Show a list of every available command.",
        handler=handle_help,
    ),
]

GOODBYE_KEYWORDS: Tuple[str, ...] = ("bye", "goodbye", "exit", "quit")
GREETING_KEYWORDS: Tuple[str, ...] = ("hello", "hi", "hey")


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def dispatch(raw_input: str) -> Tuple[str, bool]:
    """Dispatch normalized user input to the correct command handler.

    Parameters
    ----------
    raw_input : str
        The raw, unnormalized text the user typed.

    Returns
    -------
    tuple of (str, bool)
        A tuple containing the bot's response string and a boolean
        ``should_exit`` flag indicating whether the user asked to quit.
    """
    normalized = normalize_input(raw_input)

    if not normalized:
        return "I didn't receive any input. Feel free to type a command or " \
               "'help' for a list!", False

    # 1) Goodbye check (exact match or contains core goodbye words)
    if equals_any(normalized, GOODBYE_KEYWORDS) or \
            contains_any(normalized, GOODBYE_KEYWORDS):
        farewells = [
            "Goodbye! It was lovely chatting with you. Take care!",
            "Bye for now! Come back anytime - I'll be here. \o/",
            "See you later! Have an incredible rest of your day.",
            "Farewell! Happy coding, and talk to you soon.",
        ]
        return _random_response(farewells), True

    # 2) Calculator check
    if is_calculator_expression(normalized):
        try:
            result = calculate(normalized)
        except ZeroDivisionError:
            return "Oops! You can't divide by zero. " \
                   "Please try a different expression.", False
        if result is None:
            return "Hmm, I couldn't evaluate that math expression. " \
                   "Could you try writing it differently?", False
        if result.is_integer():
            shown = str(int(result))
        else:
            shown = f"{result:g}"
        return f"Calculation result: {_c(shown, Colors.GREEN, bold=True)}", \
               False

    # 3) Exact keyword-first match for greeting words at start
    for kw in GREETING_KEYWORDS:
        if normalized == kw or normalized.startswith(kw + " "):
            return handle_greeting(normalized), False

    # 4) Iterate command list for substring / exact matches
    for command in _ALL_COMMANDS:
        if contains_any(normalized, command.keywords):
            return command.handler(normalized), False

    # 5) Unknown command handler
    return handle_unknown(raw_input.strip() or normalized), False


# ---------------------------------------------------------------------------
# Core chat loop
# ---------------------------------------------------------------------------


def print_welcome() -> None:
    """Print a colourful welcome banner when the chatbot starts."""
    print()
    print(_c(banner(f"  Welcome to {BOT_NAME} v{BOT_VERSION}  "),
             Colors.CYAN, bold=True))
    print(_c(separator(), Colors.DIM))
    print_info("Type 'help' to see available commands, or 'bye' to quit.")


def chat_loop() -> None:
    """Run the main interactive conversation loop.

    The loop prompts the user for input, dispatches the command, and
    prints the bot's response.  It terminates when the user issues a
    goodbye command or when an ``EOFError`` / ``KeyboardInterrupt`` is
    received.
    """
    print_welcome()

    while True:
        try:
            user_text = prompt_user()
        except KeyboardInterrupt:
            print()
            print_bot("Looks like you're leaving. Goodbye - have a great day!")
            break

        try:
            response, should_exit = dispatch(user_text)
        except Exception as exc:  # pragma: no cover - defensive fallback
            print_error(f"Unexpected error while handling your command: "
                        f"{exc!r}")
            continue

        print_bot(response)

        if should_exit:
            break


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Chatbot entry point. Returns a process exit code."""
    try:
        chat_loop()
    except Exception as exc:  # pragma: no cover - defensive top-level guard
        print_error(f"Fatal error: {exc!r}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
