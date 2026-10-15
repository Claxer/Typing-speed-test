# TypeFlow — Typing Speed Test

A modern **Typing Speed Test** desktop application built with Python. TypeFlow helps users measure their typing speed, improve accuracy, track mistakes, and monitor their typing performance over time.

The application features a progress dashboard, timed and endless typing modes, multiple difficulty levels, custom typing passages, real-time statistics, and a local SQLite database for storing completed test results.

## Features

### Typing Test

* **Typing Speed Test** — Measure typing speed in words per minute (WPM).
* **Timed Challenges** — Choose between 30-second, 60-second, and 120-second tests.
* **Endless Mode** — Practice typing without a countdown timer until the passage is completed.
* **Difficulty Levels** — Practice with Easy, Medium, and Hard passages.
* **Custom Passages** — Enter your own text to practice with preferred words, sentences, or paragraphs.
* **Random Passages** — Automatically select a passage based on the selected difficulty when custom text is not provided.
* **Automatic Timer** — The countdown begins when the user starts typing in timed mode.
* **Automatic Test Completion** — Finish when the timer expires or when the passage is completed in endless mode.
* **Real-Time Statistics** — Monitor WPM, accuracy, and mistakes while typing.
* **Error Tracking** — Count incorrect and extra characters.
* **Accuracy Monitoring** — Calculate the percentage of correctly matched characters.
* **Flexible Practice** — Select the preferred test mode, duration, and difficulty before starting.

### Progress Dashboard

* **Personal Best** — View the highest recorded WPM.
* **Total Tests** — Track the number of completed typing tests.
* **Average WPM** — Review average typing speed across saved attempts.
* **Average Accuracy** — Monitor overall typing accuracy.
* **Progress Overview** — Review recent WPM values to observe changes in typing performance.
* **Recent Performance** — Access previous test results and compare attempts over time.

### Results and Statistics

* **Detailed Test Results** — Review WPM, raw WPM, accuracy, mistakes, and character counts.
* **Correct Character Tracking** — Record the number of characters that match the target passage.
* **Mistake Statistics** — Monitor typing errors across completed tests.
* **Test Duration Tracking** — Save the elapsed time for each completed test.
* **Difficulty and Mode Tracking** — Store the selected difficulty and typing mode with each result.
* **Recent Test History** — Review the latest completed attempts.
* **Persistent Results** — Keep saved statistics between application sessions using SQLite.
* **Recent Average WPM** — Calculate average typing speed across recent tests.

### Interface and Data Management

* **Modern Dark Theme** — Use a clean desktop interface built with CustomTkinter.
* **Dashboard Navigation** — Access the typing test, progress overview, and results history.
* **Local Data Storage** — Store test results on the computer without requiring an online account.
* **Modular Code Structure** — Separate the application, typing test, database, passages, and results into individual Python files.
* **Database Initialization** — Create the required SQLite table when the application starts.
* **Database Compatibility** — Add supported statistics columns to an existing `test_results` table when they are missing.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| CustomTkinter | Desktop graphical user interface |
| SQLite | Local storage for test results and statistics |
| `time` | Track elapsed time and calculate typing speed |
| `random` | Select random typing passages |
| `datetime` | Record the date and time of completed tests |
| `sqlite3` | Connect to and manage the SQLite database |
| `after()` | Schedule timer updates without blocking the interface |

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

* `main.py` — Starts the application, displays the progress dashboard, manages navigation, provides typing test settings, and handles completed results.
* `database.py` — Initializes the SQLite database and provides functions for saving test results, retrieving history, and calculating statistics.
* `typing_test.py` — Handles the typing interface, timed and endless modes, difficulty settings, custom passages, timer updates, and real-time typing statistics.
* `passages.py` — Stores predefined passages and selects text according to the selected difficulty or custom input.
* `results.py` — Displays saved performance statistics, personal best, average WPM, accuracy, total tests, mistakes, and recent test history.
* `requirements.txt` — Lists the Python packages required to run the application.
* `.gitignore` — Excludes temporary files, Python cache files, virtual environments, and local database files.
* `README.md` — Documents the project's features, installation, usage, and implementation.

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

The `requirements.txt` file should contain:

```text
customtkinter
```

Make sure Python is installed on your computer before installing the required package.

### 4. Run the Application

```bash
python main.py
```

The application initializes the SQLite database when it starts.

## How to Use

### Starting a Typing Test

1. Run `main.py` to open TypeFlow.
2. Review the progress dashboard for your personal best, total tests, average WPM, and average accuracy.
3. Choose your preferred typing mode:
   * **Timed** — Complete the test within the selected time limit.
   * **Endless** — Practice without a countdown until the passage is completed.
4. Choose a duration of 30, 60, or 120 seconds for timed mode.
5. Select Easy, Medium, or Hard difficulty.
6. Optionally enter custom text. Leave the custom passage field empty to use a randomly selected passage.
7. Click **Start Typing Test**.
8. Begin typing the displayed passage. In timed mode, the countdown starts with the first character.
9. Monitor your WPM, accuracy, and mistakes.
10. Finish the passage or allow the timer to expire.
11. Review your final statistics.
12. Open **View Results and History** to review your previous attempts.

### Using Custom Passages

The custom passage field lets users practice with their own text instead of the predefined passages.

1. Enter a sentence, paragraph, or longer text into the custom passage field.
2. Choose a typing mode and difficulty.
3. Start the test.
4. Type the custom passage displayed by the application.

When custom text is provided, it takes priority over the predefined passage collection.

### Reviewing Progress

The dashboard provides a summary of overall typing performance.

Users can review:

* Highest recorded WPM.
* Total number of completed tests.
* Average WPM.
* Average accuracy.
* Recent WPM values.

The results page also provides recent test history, including the selected mode, difficulty, WPM, accuracy, mistakes, and completion date.

## Understanding the Statistics

### Words Per Minute (WPM)

WPM estimates typing speed using the standard convention of five characters per word.

The application calculates its displayed WPM using the total number of typed characters divided by five and the elapsed time in minutes.

`WPM = Total Typed Characters / 5 / Elapsed Minutes`

The displayed value updates while typing. The implementation uses a minimum one-second calculation interval to avoid dividing by zero.

### Raw WPM

Raw WPM estimates typing speed using all typed characters, including incorrect characters.

`Raw WPM = Total Typed Characters / 5 / Elapsed Minutes`

In the current implementation, displayed WPM and raw WPM use the same calculation. Therefore, their values are equal. A future improvement could calculate adjusted WPM separately to account for errors.

### Accuracy

Accuracy measures the percentage of typed characters that match the corresponding characters in the target passage.

`Accuracy = Correct Characters / Total Typed Characters × 100`

The application starts at 100% accuracy before any characters are entered. Accuracy is updated as the user types.

### Mistakes

Mistakes count typed characters that do not match their corresponding positions in the target passage. Extra characters beyond the passage are also counted as mistakes.

For example, if the target character is `a` but the user types `b`, that character is counted as an error.

### Correct Characters

Correct characters represent the number of typed characters that match the corresponding characters in the target passage.

This value is saved with the completed test to support additional performance analysis.

### Average WPM

Average WPM represents the arithmetic mean of the WPM values recorded across completed tests.

`Average WPM = Sum of Recorded WPM Values / Number of Completed Tests`

### Personal Best

Personal best represents the highest WPM value recorded in the local database.

### Recent Average WPM

Recent average WPM calculates the average speed across the five most recent completed tests, or fewer if fewer than five results are available.

## Database

TypeFlow uses SQLite to store completed typing test results locally.

The reconstructed database module uses the filename `typeflow.db` and creates a table named `test_results`.

Saved results can include:

* Test ID.
* WPM.
* Raw WPM.
* Accuracy percentage.
* Number of mistakes.
* Correct characters.
* Total typed characters.
* Elapsed test duration.
* Difficulty level.
* Typing mode.
* Date and time.

The database module also provides functions for retrieving test history, personal best, average WPM, average accuracy, total mistakes, recent average WPM, and progress data.

The database is stored locally. Results are not automatically synchronized between computers or uploaded to an online service.

**Important:** If you are continuing from an older TypeFlow version, check the existing database filename and schema before replacing `database.py`. The reconstructed version uses `typeflow.db`; your previous application may use a different database file and table structure.

## Error Handling and Test Controls

TypeFlow includes basic controls intended to keep the typing test functional:

* **Timer Management** — Cancels scheduled timer updates when finishing or leaving a test.
* **Duplicate Completion Protection** — Prevents the same test from being saved repeatedly by the completion handler.
* **Automatic Completion** — Ends timed tests when the countdown expires.
* **Endless Mode Completion** — Ends the test when the typed input reaches the passage length.
* **Local Database Storage** — Saves completed test results for later review.
* **Database Initialization** — Creates the database table and adds supported missing columns when necessary.

Some features from the earlier version, such as character-by-character color highlighting and a dedicated restart/new-passage control, may need to be restored separately if they were part of your original implementation.

## Learning Objectives

This project demonstrates practical programming concepts, including:

* Object-oriented programming using Python classes.
* Building desktop interfaces with CustomTkinter.
* Handling keyboard input and GUI events.
* Using scheduled callbacks for timers.
* Calculating typing speed, accuracy, and mistakes.
* Comparing strings character by character.
* Using loops and conditional statements.
* Working with lists and dictionaries.
* Creating and querying SQLite databases.
* Saving and retrieving historical data.
* Designing a modular application architecture.
* Building a dashboard from stored statistics.
* Handling custom user input.
* Organizing and documenting a Python project for GitHub.

## Limitations

* Predefined passages are selected from a limited collection.
* Endless mode uses a single passage per test rather than continuously generating new text.
* Typing statistics use simplified character-based calculations.
* Raw WPM and displayed WPM currently use the same formula.
* The progress overview displays recent WPM values as text rather than a graphical chart.
* Character-by-character color highlighting is not implemented in the reconstructed version.
* The application does not currently provide online synchronization or cloud backups.
* Results are stored locally and are not shared between computers.
* There are no separate user accounts or individual profiles.
* Typing performance may vary depending on the keyboard, typing style, and passage difficulty.
* The application requires Python and its dependencies to be installed before it can run.

## Future Improvements

Potential future enhancements include:

* Visual progress charts for WPM and accuracy.
* Additional typing passages and continuously generated endless-mode text.
* Character-by-character correct and incorrect highlighting.
* Separate adjusted WPM calculations that account for mistakes.
* Typing consistency and error-rate analysis.
* Personal achievements and typing streaks.
* Daily typing challenges.
* Keyboard shortcuts and customizable settings.
* Exporting test history to CSV.
* User profiles and separate score histories.
* Improved passage selection and custom passage management.
* More detailed performance comparisons between different tests.
* Improved accessibility and interface customization.

## Author

**Jose Navoa**

Aspiring Information Technology Student

*Built with Python as a learning project focused on desktop application development, keyboard input handling, performance statistics, and database management.*
