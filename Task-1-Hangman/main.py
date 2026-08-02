"""
Hangman Game - A console-based word guessing game.

The player tries to guess a randomly selected word letter by letter
before running out of attempts.
"""

from __future__ import annotations

import random
import sys
from typing import Final, Sequence

# --- Game configuration -------------------------------------------------------

BANNER_WIDTH: Final[int] = 40
MAX_ATTEMPTS: Final[int] = 6

WORD_LIST: Final[tuple[str, ...]] = (
    "python",
    "hangman",
    "developer",
    "algorithm",
    "function",
    "variable",
    "keyboard",
    "software",
    "database",
    "network",
    "compiler",
    "debugger",
)

YES_RESPONSES: Final[frozenset[str]] = frozenset({"y", "yes"})
NO_RESPONSES: Final[frozenset[str]] = frozenset({"n", "no"})


# --- Word selection and display -----------------------------------------------

def choose_random_word(words: Sequence[str]) -> str:
    """
    Return a random word from ``words`` in lowercase.

    Raises:
        ValueError: If ``words`` is empty.
    """
    if not words:
        raise ValueError("Word list cannot be empty.")
    return random.choice(words).lower()


def format_hidden_word(word: str, correct_guesses: set[str]) -> str:
    """Return the word as underscores, revealing correctly guessed letters."""
    return " ".join(
        letter.upper() if letter in correct_guesses else "_"
        for letter in word
    )


def format_letters(letters: set[str]) -> str:
    """Return a sorted, comma-separated list of letters, or ``None``."""
    if not letters:
        return "None"
    return ", ".join(sorted(letter.upper() for letter in letters))


def format_attempts_remaining(count: int) -> str:
    """Return a grammatically correct attempts-remaining label."""
    if count == 1:
        return "1 attempt remaining"
    return f"{count} attempts remaining"


def has_guessed_word(word: str, correct_guesses: set[str]) -> bool:
    """Return True when every letter in ``word`` has been guessed."""
    return all(letter in correct_guesses for letter in word)


# --- Input handling -----------------------------------------------------------

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


def is_valid_letter(guess: str) -> bool:
    """Return True when ``guess`` is a single alphabetic character."""
    return len(guess) == 1 and guess.isalpha()


def prompt_for_letter(tried_letters: set[str]) -> str:
    """
    Prompt until the user enters a new, valid letter.

    Args:
        tried_letters: Letters already guessed in the current round.

    Returns:
        A lowercase letter that has not been tried yet.
    """
    while True:
        raw_guess = read_line("Enter a letter: ").lower()

        if not raw_guess:
            print("Input cannot be empty. Enter a single letter (A-Z).")
            continue

        if not is_valid_letter(raw_guess):
            print("Invalid input. Please enter a single letter (A-Z).")
            continue

        if raw_guess in tried_letters:
            print(
                f"You already guessed '{raw_guess.upper()}'. "
                "Try another letter."
            )
            continue

        return raw_guess


def ask_play_again() -> bool:
    """Return True when the player wants another round."""
    while True:
        try:
            response = read_line("\nPlay again? (y/n): ").lower()
        except EOFError:
            return False

        if response in YES_RESPONSES:
            return True
        if response in NO_RESPONSES:
            return False

        print("Please enter 'y' for yes or 'n' for no.")


# --- Game logic ---------------------------------------------------------------

def apply_guess(
    guess: str,
    word: str,
    correct_guesses: set[str],
    wrong_guesses: set[str],
) -> bool:
    """
    Record a guess and print feedback.

    Returns:
        True if the guess appears in the word, False otherwise.
    """
    display_letter = guess.upper()

    if guess in word:
        correct_guesses.add(guess)
        print(f"Good guess! '{display_letter}' is in the word.")
        return True

    wrong_guesses.add(guess)
    print(f"Sorry, '{display_letter}' is not in the word.")
    return False


# --- Console output -----------------------------------------------------------

def print_section(title: str, border_char: str = "=") -> None:
    """Print a centered title bordered by repeated characters."""
    border = border_char * BANNER_WIDTH
    print(f"\n{border}\n{title}\n{border}")


def print_welcome() -> None:
    """Display the welcome message and game rules."""
    print_section("       WELCOME TO HANGMAN!")
    print("Guess the hidden word one letter at a time.")
    print(f"You have {MAX_ATTEMPTS} incorrect guesses before you lose.")
    print("Press Ctrl+C at any time to quit.")
    print("Good luck!\n")


def print_game_state(
    word: str,
    correct_guesses: set[str],
    wrong_guesses: set[str],
    remaining_attempts: int,
) -> None:
    """Render the current board, guesses, and attempts left."""
    tried_letters = correct_guesses | wrong_guesses
    print(f"\n{'=' * BANNER_WIDTH}")
    print(f"Word ({len(word)} letters): {format_hidden_word(word, correct_guesses)}")
    print(f"Guessed: {format_letters(tried_letters)}")
    print(f"Wrong:   {format_letters(wrong_guesses)}")
    print(format_attempts_remaining(remaining_attempts))

    if remaining_attempts == 1:
        print("Careful — this is your last attempt!")
    elif remaining_attempts == 2:
        print("Only 2 attempts left.")

    print("=" * BANNER_WIDTH)


def print_win(word: str) -> None:
    """Display the win message."""
    print_section(
        f"  Congratulations! You guessed '{word.upper()}'!\n  YOU WIN!",
        border_char="*",
    )


def print_lose(word: str) -> None:
    """Display the lose message."""
    print_section(
        f"  Game Over! The word was '{word.upper()}'.\n  YOU LOSE!",
        border_char="!",
    )


def print_goodbye() -> None:
    """Display the exit message."""
    print("\nThanks for playing Hangman. Goodbye!")


# --- Round and program flow ---------------------------------------------------

def play_round() -> None:
    """
    Run a single round of Hangman.

    Displays the final board, then a win or lose message.
    """
    try:
        word = choose_random_word(WORD_LIST)
    except ValueError as exc:
        print(f"Error starting game: {exc}", file=sys.stderr)
        return

    correct_guesses: set[str] = set()
    wrong_guesses: set[str] = set()
    remaining_attempts = MAX_ATTEMPTS

    while remaining_attempts > 0 and not has_guessed_word(word, correct_guesses):
        print_game_state(
            word, correct_guesses, wrong_guesses, remaining_attempts
        )

        guess = prompt_for_letter(correct_guesses | wrong_guesses)

        if not apply_guess(guess, word, correct_guesses, wrong_guesses):
            remaining_attempts -= 1

    print_game_state(word, correct_guesses, wrong_guesses, remaining_attempts)

    if has_guessed_word(word, correct_guesses):
        print_win(word)
    else:
        print_lose(word)


def main() -> None:
    """Entry point for the Hangman game."""
    print_welcome()

    try:
        while True:
            play_round()
            if not ask_play_again():
                break
    except (KeyboardInterrupt, EOFError):
        print()  # Move to a new line after Ctrl+C on the prompt.

    print_goodbye()


if __name__ == "__main__":
    main()
