# Task 4 – Production-Quality Python Console Chatbot

## Project Overview

This project is a **production-quality, modular Python console chatbot** built for CodeAlpha Task 4. It uses only the **Python standard library** (no external dependencies) and is written in clean, PEP 8–compliant code with type hints, docstrings, and robust exception handling throughout.

The chatbot is designed to be friendly and useful.  It greets users, answers questions about date/time/day, tells jokes, shares motivational quotes, performs basic arithmetic calculations, offers a command reference via `help`, and keeps the conversation going until the user types `bye`, `exit`, or `quit`.

---

## Features

- **Greeting responses** – recognises `hello`, `hi`, `hey`.
- **Goodbye responses** – recognises `bye`, `goodbye`, `exit`, `quit` and exits cleanly.
- **How are you?** – responds to questions like `how are you`, `how's it going`, etc.
- **Current time** – `time` / `current time` / `what time is it`
- **Current date** – `date` / `current date` / `what date is it`
- **Current day** – `day` / `current day` / `what day is it`
- **Tell its own name** – `your name`, `what is your name`, `who are you`
- **Help command** – `help`, `commands`, `what can you do`, `help me`
- **Calculator** – supports `+`, `-`, `*`, `/` and arbitrary expressions:
  - `2+5`, `10 / 2`, `7*8`, `20-4`, `2 + 3 * 4`, etc.
  - Safe evaluation, zero-division protection, parenthesised sub-expressions.
- **Random jokes** – 12 programmer jokes minimum (actually 12!)
- **Random motivational quotes** – 12 programmer/developer quotes (actually 12!)
- **Unknown command handler** – friendly reply when the bot doesn't understand.
- **Robust input handling** – ignores extra whitespace (leading/trailing/internal), case-insensitive input, and tolerant of varied phrasing.
- **Attractive console formatting** – ANSI colours (auto-detected; gracefully falls back on non-TTY streams).
- **Continuous conversation loop** until the user exits.
- **KeyboardInterrupt / EOF handling** for clean exits.

---

## Folder Structure

```
Task-4-Chatbot/
│
├── main.py          # Modular chatbot entry point and command dispatch
└── README.md        # This documentation
```

---

## Requirements

| Requirement            | Details
| ---------------------- | ------------------------------------------------------ |
| **Python version**     | Python 3.11 or newer (uses modern type-hint syntax & stdlib features) |
| **External libraries** | **None.** All features are implemented using the Python standard library only. |

---

## Installation

Because the project uses **only the Python standard library**, no `pip install` is required.

1. Ensure you have **Python 3.11+** available on your system:

   ```bash
   python --version
   ```

2. Clone or download the project so you have a local copy of the `Task-4-Chatbot` folder. No additional setup is needed.

---

## Usage

From the `CodeAlpha_Python` directory, run:

```bash
python Task-4-Chatbot/main.py
```

Or, from inside the `Task-4-Chatbot` directory:

```bash
python main.py
```

You will be greeted with a welcome banner and a `[You]` prompt. Start typing commands.  Type `help` at any time to see the full list, and `bye` (or `exit` / `quit`) to leave.

### Command quick-reference summary

| Command category      | Example input(s)                                            |
| ---------------- | ---------------------------------------------------------- |
| Greeting       | `hello`, `hi`, `hey`, `Hello there!`                      |
| How are you?   | `how are you`, `how's it going`                           |
| Time           | `time`, `what time is it`                                 |
| Date           | `date`, `what is the date`                                 |
| Day            | `day`, `what day is it`                                    |
| Name           | `your name`, `who are you`                                 |
| Joke           | `joke`, `tell me a joke`                                   |
| Quote          | `quote`, `motivational quote`, `motivate me`                 |
| Help           | `help`, `commands`, `what can you do`                        |
| Calculator     | `2+5`, `10 / 2`, `7*8`, `20-4`, `(2 + 3) * 4`        |
| Exit           | `bye`, `goodbye`, `exit`, `quit`                            |

---

## Example Conversation

```
================  Welcome to PyBot v1.0.0  ===============
------------------------------------------------------------

[Info] Type 'help' to see available commands, or 'bye' to quit.

[You] hello

[PyBot] Hello! Great to see you today. How can I help?

[You] how are you

[PyBot] I'm doing fantastic, thank you for asking! How about you?

[You] time

[PyBot] The current time is 09:47:12 PM.

[You] date

[PyBot] Today's date is August 03, 2026.

[You] day

[PyBot] Today is Monday.

[You] 2+5

[PyBot] Calculation result: 7

[You] 10/2

[PyBot] Calculation result: 5

[You] joke

[PyBot] Why do programmers prefer dark mode? Because light attracts bugs!

[You] quote

[PyBot] "Talk is cheap. Show me the code." – Linus Torvalds

[You] help

[PyBot] Available Commands:

  Greeting:
    Keywords: 'hello', 'hi', 'hey'
    Say hello and start a friendly conversation.

  ...
  (full list shown)
  ...

[You] bye

[PyBot] Goodbye! It was lovely chatting with you. Take care!
```

*(Exact greetings, jokes and quotes are randomised, so each conversation is a little different every time.)*

---

## Future Improvements

Ideas for enhancing the chatbot in future iterations:

1. **Natural Language / Fuzzy Matching** – replace simple keyword matching with a small TF-IDF or Levenshtein-distance fuzzy matcher so the bot understands close misspellings.
2. **Persistent user memory** – save a JSON/SQLite session history so the bot remembers prior conversations, user preferences across restarts.
3. **More calculator features** – modulus `%`, exponentiation `**`, square roots, trigonometric functions, and a custom safe expression parser instead of `eval`.
4. **Unit / currency conversion** – convert between km ↔ miles, kg ↔ lb, USD ↔ EUR (perhaps via a cached rates table).
5. **Weather / news lookups** – optional stdlib `urllib` + public APIs (opt-in, to keep offline-only mode).
6. **Unit tests** – `pytest` suite against the `dispatch` and `calculate` functions.
7. **Configuration file** – allow the user to customise the bot's name, colours, and the default set of jokes/quotes via JSON without editing source code.
8. **Internationalisation (i18n)** – support multiple UI languages via `gettext`.
9. **Logging** – structured `logging` module support for debug/audit trails.
10. **Web / GUI frontends** – wrap the pure core `dispatch()` function with a Flask API, Tkinter, or PySimpleGUI UI.

---

## License

MIT License – see the top-level project `README.md` for the canonical project-wide license, or apply MIT per-file:

> **MIT License**
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
