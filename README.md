# TypeFlow — Typing Speed Test

A modern **Typing Speed Test** desktop application built with Python. TypeFlow helps users measure their typing speed, improve accuracy, track mistakes, and review their typing performance over time.

The application features timed typing challenges, multiple difficulty levels, real-time statistics, character-by-character feedback, and a local database for storing test results.

## Features

* **Typing Speed Test** — Measure typing speed in words per minute (WPM).
* **Real-Time Statistics** — Monitor WPM, accuracy, and mistakes while typing.
* **Timed Challenges** — Choose 30-second, 60-second, or 120-second tests.
* **Difficulty Levels** — Practice using Easy, Medium, and Hard passages.
* **Automatic Timer** — The countdown starts when the user types the first character.
* **Automatic Test Completion** — The test finishes when the time runs out or the entire passage has been typed.
* **Character Highlighting** — Display correct, incorrect, and remaining characters in different colors.
* **Error Tracking** — Count incorrect characters and extra characters typed beyond the passage.
* **Live WPM Calculation** — Update typing speed as the user continues typing.
* **Accuracy Monitoring** — Calculate the percentage of correctly typed characters.
* **Restart and New Passage** — Reset the test and generate a new passage for additional practice.
* **Automatic Results Saving** — Store completed test results in a local SQLite database.
* **Personal Best** — Track your highest recorded WPM.
* **Average Typing Speed** — View your average WPM across completed tests.
* **Typing History** — Review previous results, including accuracy, difficulty, and date.
* **Modern Interface** — Navigate through a clean dark-themed desktop application.
* **Local Data Storage** — Keep test history on your computer without requiring an online account.
* **Modular Code Structure** — Separate the typing test, database, passages, results, and application navigation into different Python files.

## Technologies Used

| Technology           | Purpose                                                     |
| -------------------- | ----------------------------------------------------------- |
| Python               | Main programming language                                   |
| CustomTkinter        | Graphical user interface                                    |
| SQLite               | Local database for storing test results                     |
| `time`               | Tracking elapsed time and calculating typing speed          |
| `random`             | Selecting typing passages                                   |
| `tkinter.messagebox` | Displaying informational messages                           |
| `after()`            | Updating the countdown timer without freezing the interface |

## Project Structure

```text
Typing-Speed-Test/
├── main.py
├── database.py
├── typing_test.py
├── passages.py
├── results.py
├── requirements.txt
├── .gitignore
└── README.md
```

### File Descriptions

* `main.py` — Starts the application, creates the main interface, manages navigation, and handles completed test results.
* `database.py` — Creates the SQLite database and provides functions for saving and retrieving typing results and statistics.
* `typing_test.py` — Handles the typing interface, difficulty selection, test duration, countdown timer, character highlighting, and real-time statistics.
* `passages.py` — Stores and selects typing passages according to the selected difficulty.
* `results.py` — Displays typing statistics and previously recorded test results.
* `requirements.txt` — Lists the required Python packages.
* `.gitignore` — Excludes temporary files, Python cache files, virtual environments, and local database files.
* `README.md` — Contains the project documentation, installation instructions, and feature descriptions.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Typing-Speed-Test.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the Project Directory

```bash
cd Typing-Speed-Test
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Make sure Python is installed on your computer before installing the required packages.

### 4. Run the Application

```bash
python main.py
```

The application initializes its local SQLite database through the database module.

## How to Use

1. Open TypeFlow by running `main.py`.
2. Select **Typing Test** from the application sidebar.
3. Choose your preferred difficulty: Easy, Medium, or Hard.
4. Select a test duration of 30, 60, or 120 seconds.
5. Begin typing the displayed passage. The timer starts with your first character.
6. Observe the live WPM, accuracy percentage, and error count.
7. Check the passage for color-coded feedback:

   * **Green** — Correctly typed characters.
   * **Red** — Incorrectly typed characters.
   * **Gray** — Characters that have not yet been typed.
8. Complete the passage or allow the timer to expire.
9. Review the final test statistics.
10. Open **Results & History** to review previously saved results.
11. Select **New Passage / Restart** to practice again.

## Understanding the Statistics

### Words Per Minute (WPM)

WPM estimates typing speed using the standard convention of five characters per word. TypeFlow calculates its displayed WPM using correctly typed characters divided by five and the elapsed time in minutes.

`WPM = Correct Characters / 5 / Elapsed Minutes`

The live WPM value updates while typing. The program uses a minimum one-second calculation interval to avoid dividing by zero.

### Raw WPM

Raw WPM estimates typing speed using all typed characters, including incorrect characters.

`Raw WPM = Total Typed Characters / 5 / Elapsed Minutes`

Raw WPM represents typing speed before accounting for mistakes.

### Accuracy

Accuracy measures the percentage of typed characters that match the corresponding characters in the target passage.

`Accuracy = Correct Characters / Total Typed Characters × 100`

Accuracy starts at 100% before typing begins. Once typing starts, it changes according to the characters entered.

### Mistakes

Mistakes count typed characters that do not match the corresponding passage characters, including extra characters beyond the passage.

For example, if the target character is `a` but the user types `b`, that character is counted as an error.

These are simplified character-based measurements intended for practice and learning.

## Database

TypeFlow uses SQLite to store completed typing test results locally.

The database module manages saving results, retrieving previous attempts, and calculating statistics for the results page.

Depending on the database configuration in `database.py`, the generated database file may have a different name. The database filename configured in that file should be used when describing the project's local storage.

Saved results can include:

* Test ID
* Words per minute
* Accuracy percentage
* Number of mistakes
* Difficulty level
* Test duration
* Date and time

The database is stored locally, so results are not automatically shared or synchronized across devices.

## Error Handling and Test Controls

TypeFlow includes several controls intended to make the typing test easier to use:

* **Empty Test Protection** — Prevents a test from being completed before the user starts typing.
* **Timer Management** — Cancels scheduled timer updates when restarting or leaving the test.
* **Input Locking** — Disables typing input after a test is completed.
* **Restart Support** — Resets the timer, statistics, passage, and typing area.
* **Automatic Completion** — Prevents the test from continuing after the timer expires or the passage is completed.

## Learning Objectives

This project demonstrates practical programming concepts, including:

* Object-oriented programming using Python classes.
* Building a desktop GUI with CustomTkinter.
* Event handling and keyboard input.
* Timers and scheduled UI updates.
* Calculating typing speed and accuracy.
* Comparing strings character by character.
* Using loops and conditional statements.
* Working with lists and dictionaries.
* Connecting Python to an SQLite database.
* Organizing application logic into separate modules.
* Displaying and storing historical data.
* Handling user input and basic application errors.
* Organizing a project for GitHub.

## Limitations

* Typing passages are selected from a predefined collection.
* Statistics use simplified character-based calculations.
* The application does not currently provide online synchronization.
* Results are stored locally and are not shared between computers.
* Typing performance can vary depending on the keyboard, typing style, and passage difficulty.
* Raw WPM and displayed WPM use different character counts, so their values may differ.
* The application requires Python and its dependencies to be installed before it can run.

## Future Improvements

Potential future features include:

* More typing passages and custom text.
* Additional difficulty levels.
* Difficulty-specific leaderboards.
* Daily typing challenges.
* Visual typing progress charts.
* Exporting results to CSV.
* User profiles and separate score histories.
* Detailed typing analytics.
* Keyboard shortcut support.
* Personal achievements and typing streaks.
* Improved statistics and performance comparisons.

## Author

**Jose Navoa**

Aspiring Information Technology Student

*Built with Python as a learning project focused on desktop application development, keyboard input handling, performance statistics, and database management.*
