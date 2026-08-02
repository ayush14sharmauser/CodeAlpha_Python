# Hangman Game

> A console-based Hangman word guessing game built with Python 3.

Guess the hidden word letter by letter before you run out of attempts.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Project Overview

Hangman is a classic word game where the player discovers a secret word by guessing one letter at a time. Each incorrect guess reduces the number of remaining attempts. The round ends when the full word is revealed (**win**) or all allowed incorrect guesses are used (**lose**).

This project is a standalone Python console application with modular functions, input validation, and a replay loop for continuous play.

---

## Features

| Feature | Description |
| --- | --- |
| Random word selection | Chooses from 12 programming-related words |
| Hidden word display | Underscores reveal correctly guessed letters |
| Attempt limit | Maximum of 6 incorrect guesses per round |
| Guess tracking | Shows all tried letters and wrong guesses separately |
| Input validation | Accepts only single alphabetic characters |
| Duplicate prevention | Warns when a letter was already guessed |
| Win / lose feedback | Clear end-of-round messages |
| Replay option | Play multiple rounds without restarting |
| Error handling | Handles invalid input, Ctrl+C, and EOF gracefully |
| Zero dependencies | Uses only the Python standard library |

---

## Folder Structure

```text
Task-1-Hangman/
├── main.py       # Game logic and console interface
└── README.md     # Project documentation
```

---

## Requirements

- **Python 3.9+** (uses `list[str]` type hints and `Final`)
- No third-party packages

---

## Installation

1. Clone or download this repository.
2. Open a terminal and navigate to the project folder:

   ```bash
   cd Task-1-Hangman
   ```

3. Confirm Python 3 is available:

   ```bash
   python --version
   ```

   On Linux or macOS you may use:

   ```bash
   python3 --version
   ```

---

## Usage

From the `Task-1-Hangman` directory, run:

```bash
python main.py
```

Or, on systems where `python3` is the default:

```bash
python3 main.py
```

### How to Play

1. A random word is selected when the round starts.
2. Enter **one letter** when prompted.
3. Correct letters appear in the word display.
4. Wrong letters reduce your remaining attempts.
5. Win by revealing the entire word before attempts reach zero.
6. At the end of a round, enter **y** to play again or **n** to quit.
7. Press **Ctrl+C** at any time to exit.

---

## Sample Output

```text
========================================
       WELCOME TO HANGMAN!
========================================
Guess the hidden word one letter at a time.
You have 6 incorrect guesses before you lose.
Press Ctrl+C at any time to quit.
Good luck!

========================================
Word (6 letters): _ _ _ _ _ _
Guessed: None
Wrong:   None
6 attempts remaining
========================================
Enter a letter: p

========================================
Word (6 letters): P _ _ _ _ _
Guessed: P
Wrong:   None
6 attempts remaining
========================================
Enter a letter: x
Sorry, 'X' is not in the word.

========================================
Word (6 letters): P _ _ _ _ _
Guessed: P, X
Wrong:   X
5 attempts remaining
========================================
Enter a letter: y
Good guess! 'Y' is in the word.

...

****************************************
  Congratulations! You guessed 'PYTHON'!
  YOU WIN!
****************************************

Play again? (y/n): n

Thanks for playing Hangman. Goodbye!
```

---

## Future Improvements

- Difficulty levels (easy, medium, hard) based on word length
- Word categories loaded from an external file
- ASCII art hangman stages for visual feedback
- Session win/loss statistics
- Two-player mode with a custom secret word
- Optional hint system with an attempt penalty
- Unit tests for core game logic

---

## License

This project is part of the CodeAlpha Python internship tasks and is provided for educational purposes. Feel free to use, modify, and distribute with attribution.
