# TypeFlow — Typing Speed Test

A modern **Typing Speed Test** desktop application built with Python. TypeFlow helps users measure their typing speed, improve accuracy, track mistakes, and review their typing performance over time.

The application features timed typing challenges, multiple difficulty levels, real-time statistics, and a local database for storing test results.

## Features

* **Typing Speed Test** — Measure typing speed in words per minute (WPM).
* **Real-Time Statistics** — Monitor WPM, accuracy, and mistakes during a test.
* **Timed Challenges** — Choose 30-second, 60-second, or 120-second tests.
* **Difficulty Levels** — Practice using Easy, Medium, and Hard passages.
* **Automatic Results Saving** — Store completed test results in a local SQLite database.
* **Personal Best** — Track your highest recorded WPM.
* **Average Typing Speed** — View your average WPM across completed tests.
* **Typing History** — Review previous results, including accuracy, difficulty, and date.
* **Modern Interface** — Navigate through a clean dark-themed desktop application.
* **Local Data Storage** — Keep test history on your computer without requiring an online account.

## Technologies Used

| Technology           | Purpose                     |
| -------------------- | --------------------------- |
| Python               | Main programming language   |
| CustomTkinter        | Graphical user interface    |
| SQLite               | Local database              |
| `time`               | Timing and WPM calculations |
| `random`             | Selecting typing passages   |
| `tkinter.messagebox` | Displaying error messages   |

## Project Structure

```text
Typing-Speed-Test/
├── main.py
├── database.py
├── typing_test.py
├── passages.py
├── results.py
├── requirements.txt
└── README.md
```

### File Descriptions

* `main.py` — Starts the application and manages navigation.
* `database.py` — Creates the database and manages saved typing results.
* `typing_test.py` — Handles the typing interface, timer, and live statistics.
* `passages.py` — Stores and selects passages for each difficulty level.
* `results.py` — Displays typing results, statistics, and history.
* `requirements.txt` — Lists the required Python packages.
* `.gitignore` — Excludes temporary files and local database files.

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

### 4. Run the Application

```bash
python main.py
```

The application will create its local SQLite database automatically when it starts.

## How to Use

1. Open TypeFlow.
2. Select **Typing Test** from the sidebar.
3. Choose your preferred difficulty.
4. Select a test duration.
5. Start typing the displayed passage to begin the timer.
6. Monitor your typing speed, accuracy, and mistakes.
7. Finish the passage or let the timer expire.
8. Open **Results & History** to review your performance.
9. Repeat the test to practice and improve your score.

## Understanding the Statistics

**Words Per Minute (WPM)**

WPM estimates typing speed using the standard convention of five characters per word:

`WPM = Correct Characters / 5 / Elapsed Minutes`

**Accuracy**

Accuracy measures the percentage of typed characters that match the corresponding characters in the target passage:

`Accuracy = Correct Characters / Typed Characters × 100`

**Mistakes**

Mistakes count typed characters that do not match the corresponding passage characters, including extra characters beyond the passage.

These are simplified character-based measurements intended for practice and learning.

## Database

TypeFlow uses SQLite to save completed test results locally.

Each record includes:

* Test ID
* Words per minute
* Accuracy percentage
* Number of mistakes
* Difficulty level
* Test duration
* Date and time

The database file, `typing_history.db`, is generated automatically in the project directory.

## Learning Objectives

This project demonstrates practical programming concepts, including:

* Object-oriented programming using Python classes.
* Building a desktop GUI with CustomTkinter.
* Event handling and keyboard input.
* Timers and scheduled UI updates.
* Calculating typing speed and accuracy.
* Working with lists and dictionaries.
* Connecting Python to an SQLite database.
* Separating application logic into modules.
* Displaying and storing historical data.
* Organizing a project for GitHub.

## Limitations

* Typing passages are selected from a predefined collection.
* Statistics use a simplified character-based calculation.
* Results are stored locally and are not synchronized across devices.
* The application does not require an internet connection after dependencies have been installed.
* Typing performance can vary depending on the keyboard, typing style, and passage difficulty.

## Future Improvements

Potential future features include:

* More typing passages and custom text.
* Visual highlighting of correct and incorrect characters.
* Difficulty-specific leaderboards.
* Daily typing challenges.
* Typing progress charts.
* Exporting results to CSV.
* User profiles and separate score histories.
* Improved accuracy calculations and detailed typing analytics.

## Author

**Jose Navoa**

Aspiring Information Technology Student

*Built with Python as a learning project focused on desktop application development, keyboard input handling, performance statistics, and database management.*
