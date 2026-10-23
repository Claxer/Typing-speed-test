# TypeFlow — Typing Speed Test

A modern **Typing Speed Test** desktop application built with Python. TypeFlow helps users measure their typing speed, improve accuracy, track mistakes, and monitor their typing performance over time.

Built with **Python, CustomTkinter, SQLite, and Matplotlib**, TypeFlow provides a clean dark-themed interface with timed typing tests, difficulty levels, live statistics, a progress dashboard, achievements, daily practice goals, and saved test history.

## Features

### Typing Test

- **Typing Speed Test** — Measure typing speed in words per minute (WPM).
- **Timed Challenges** — Choose between 30-second, 60-second, and 120-second tests.
- **Difficulty Levels** — Practice with Easy, Medium, and Hard passages.
- **Random Passages** — Automatically select a practice passage based on the selected difficulty.
- **Automatic Timer** — Start the countdown when typing begins.
- **Pause and Resume** — Temporarily pause an active test and resume it later.
- **Restart Test** — Reset the current test and generate a new passage.
- **Manual Completion** — Finish a test before the timer expires.
- **Real-Time Statistics** — Monitor WPM, accuracy, and mistakes while typing.
- **Error Tracking** — Count incorrect and extra characters.
- **Accuracy Monitoring** — Calculate the percentage of correctly matched characters.
- **Automatic Result Saving** — Save completed tests to the local SQLite database.

### Progress Dashboard

- **Personal Best** — View the highest recorded WPM.
- **Total Tests** — Track the number of completed typing tests.
- **Average WPM** — Review average typing speed across saved attempts.
- **Average Accuracy** — Monitor overall typing accuracy.
- **Recent WPM Progress Chart** — Visualize recent typing speeds using Matplotlib.
- **Daily Practice Goal** — Track the number of tests completed toward a daily target.
- **Total Practice Time** — Review the combined duration of saved tests.
- **Total Characters Typed** — Monitor typing activity across completed tests.
- **Progress Overview** — View a summary of overall typing performance.

### Results and Statistics

- **Detailed Test Results** — Review WPM, accuracy, mistakes, duration, difficulty, and character count.
- **Mistake Statistics** — Track errors across completed tests.
- **Character Tracking** — Count the total characters entered during each test.
- **Test Duration Tracking** — Save the elapsed duration of completed tests.
- **Difficulty Tracking** — Record the selected difficulty with each result.
- **Recent Test History** — Review previous attempts in chronological order.
- **Persistent Results** — Keep saved statistics between application sessions using SQLite.
- **Searchable History** — Filter previous results by date or difficulty.
- **Delete Individual Results** — Remove selected records after confirmation.
- **CSV Export** — Export typing history for use in spreadsheet applications such as Microsoft Excel.

### Achievements

- **First Steps** — Complete your first typing test.
- **Getting Started** — Complete 10 typing tests.
- **Practice Pro** — Complete 50 typing tests.
- **Speed Demon** — Reach 60 WPM.
- **Speed Master** — Reach 100 WPM.
- **Keyboard Explorer** — Type 10,000 characters.
- **Daily Dedication** — Complete the configured daily practice goal.

Achievements are calculated from saved results. They update as the user completes more tests and reaches new milestones.

### Settings and Customization

- **Adjustable Daily Goal** — Set a target of 1 to 100 completed tests per day.
- **Persistent Settings** — Save the daily goal in SQLite.
- **Difficulty Selection** — Change between Easy, Medium, and Hard.
- **Duration Selection** — Select a 30-, 60-, or 120-second test.
- **Dark Appearance** — Use a clean, dark-themed desktop interface.
- **Navigation Sidebar** — Access the dashboard, typing test, history, achievements, and settings.
- **Local Data Storage** — Store results and preferences on the computer without requiring an online account.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| CustomTkinter | Desktop graphical user interface |
| SQLite | Local storage for typing results and settings |
| Matplotlib | Display the WPM progress chart |
| `sqlite3` | Create, query, and update the database |
| `time` | Measure elapsed time and calculate typing speed |
| `random` | Select random practice passages |
| `datetime` | Determine the current date for daily goals |
| `csv` | Export typing history |
| `pathlib` | Manage database and export file paths |
| `tkinter` | File dialogs and confirmation messages |
| `after()` | Schedule timer updates without blocking the interface |

## Project Structure

```text
TypeFlow_Enhanced/
├── main.py
├── database.py
├── passages.py
├── typing_test.py
├── dashboard.py
├── achievements.py
├── settings.py
├── stats_manager.py
├── export.py
├── requirements.txt
├── README.md
└── typeflow.db
```

### File Descriptions

- `main.py` — Starts the application, creates the main window, manages navigation, and displays the dashboard, typing test, history, achievements, and settings.
- `database.py` — Initializes the SQLite database and provides functions for saving results, retrieving history, storing settings, counting daily tests, and deleting records.
- `passages.py` — Stores predefined passages and randomly selects text according to the chosen difficulty.
- `typing_test.py` — Handles typing input, countdown timing, pause and resume controls, test restarting, live statistics, and result saving.
- `dashboard.py` — Displays overall typing statistics, the daily practice goal, total practice time, character count, and a WPM progress chart.
- `achievements.py` — Checks completed tests, typing speed milestones, total characters, and daily practice goals.
- `settings.py` — Retrieves and updates the daily practice goal.
- `stats_manager.py` — Calculates total tests, personal best, average WPM, average accuracy, practice time, character count, mistakes, and recent WPM progress.
- `export.py` — Exports saved typing results to a CSV file.
- `requirements.txt` — Lists the required Python packages.
- `README.md` — Documents the application's features, installation, usage, and implementation.
- `typeflow.db` — The SQLite database, created automatically when the application initializes. It should not be manually created.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/TypeFlow_Enhanced.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the Project Directory

```bash
cd TypeFlow_Enhanced
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
customtkinter
matplotlib
```

Python's built-in `sqlite3`, `time`, `random`, `datetime`, `csv`, and `pathlib` modules do not require separate installation.

### 4. Run the Application

```bash
python main.py
```

The application initializes the SQLite database when it starts.

## How to Use

### Starting a Typing Test

1. Run `main.py` to open TypeFlow.
2. Open the **Dashboard** to review your saved typing statistics.
3. Select **Typing Test** from the navigation sidebar.
4. Choose a duration of 30, 60, or 120 seconds.
5. Select Easy, Medium, or Hard difficulty.
6. Read the displayed passage.
7. Start typing to begin the countdown.
8. Monitor your WPM, accuracy, and mistakes.
9. Use **Pause** to temporarily stop an active test and **Resume** to continue.
10. Use **Restart** to begin again with a new passage.
11. Select **Finish Test** to end the test early, or allow the timer to expire.
12. Review your final statistics.

Completed tests are saved in the local database.

### Reviewing the Dashboard

Open **Dashboard** to review:

- Total completed tests.
- Highest recorded WPM.
- Average WPM.
- Average accuracy.
- Recent WPM progress chart.
- Today's completed tests compared with the daily goal.
- Total practice time.
- Total characters typed.

The chart displays recent saved WPM values to help users observe changes in typing performance.

### Managing Typing History

1. Open **History**.
2. Enter a date or difficulty in the search field.
3. Select **Search** to filter results.
4. Select **Show All** to display the complete history.
5. Highlight a result line and choose **Delete Selected** to remove a record after confirmation.

Deleting a result removes that record from the database and affects statistics calculated from saved results.

### Exporting Results

1. Select **Export CSV** from the sidebar.
2. Choose a destination and filename.
3. Save the exported CSV file.
4. Open the file using a spreadsheet application.

The export contains saved test information, including WPM, accuracy, mistakes, duration, difficulty, character count, and date.

### Setting a Daily Practice Goal

1. Open **Settings**.
2. Enter a whole number between 1 and 100.
3. Select **Save Goal**.

The dashboard compares the number of tests completed today with the configured goal. The Daily Dedication achievement unlocks when the goal is reached.

### Checking Achievements

Open **Achievements** to view the available milestones and see which ones have been unlocked.

Achievement progress is based on saved typing results and the current daily goal.

## Understanding the Statistics

### Words Per Minute (WPM)

WPM estimates typing speed using the standard convention of five characters per word.

```text
WPM = Total Typed Characters / 5 / Elapsed Time in Minutes
```

The typing engine updates the displayed WPM while the test is active. The calculation uses elapsed time, with protection against division by zero.

### Accuracy

Accuracy measures the percentage of typed characters that match the corresponding characters in the target passage.

```text
Accuracy = Correct Characters / Total Typed Characters × 100
```

Before typing begins, accuracy is displayed as 100%. Incorrect and extra characters reduce the accuracy score.

### Mistakes

Mistakes count typed characters that do not match their corresponding positions in the target passage. Characters typed beyond the passage length are also counted as mistakes.

### Personal Best

Personal best is the highest WPM recorded in the saved typing results.

### Average WPM

Average WPM is the arithmetic mean of the WPM values recorded across completed tests.

```text
Average WPM = Sum of Recorded WPM Values / Number of Completed Tests
```

### Practice Time

Practice time is calculated by adding the saved durations of completed tests. The dashboard displays the total in minutes.

### Daily Goal Progress

Daily goal progress compares the number of tests saved for the current date with the user's configured target.

## Database

TypeFlow uses SQLite for local data storage.

The application creates the following tables in `typeflow.db`:

### Results

The `results` table stores completed typing attempts.

Fields include:

- Test ID.
- WPM.
- Accuracy percentage.
- Number of mistakes.
- Test duration.
- Difficulty level.
- Number of typed characters.
- Completion date.

### Settings

The `settings` table stores application preferences.

The current implementation uses it to save the daily practice goal.

Results and settings remain available after the application closes. They are stored locally and are not automatically synchronized between computers.

**Important:** This enhanced version uses the `results` table in `typeflow.db`. Older TypeFlow versions may use a different database filename, such as `typing_history.db`, or a different table structure. Back up your existing database before replacing the older code. This standalone version does not automatically migrate every older database schema.

## Error Handling and Test Controls

TypeFlow includes controls intended to make the application more reliable:

- **Timer Management** — Cancels scheduled timer updates when a test finishes or restarts.
- **Duplicate Completion Protection** — Prevents a completed test from being saved repeatedly by the same completion handler.
- **Automatic Completion** — Ends a test when its countdown expires.
- **Pause and Resume** — Preserves elapsed time while the test is paused.
- **Database Initialization** — Creates the required database tables when the application starts.
- **Parameterized SQL Queries** — Passes values separately from SQL statements for database operations.
- **Export Error Handling** — Displays a message if a CSV file cannot be saved.
- **Delete Confirmation** — Asks for confirmation before removing a selected history record.
- **Input Validation** — Restricts the daily practice goal to values between 1 and 100.

## Learning Objectives

This project demonstrates practical programming concepts, including:

- Object-oriented programming using Python classes.
- Desktop application development with CustomTkinter.
- Keyboard input handling and GUI events.
- Timers and scheduled callbacks.
- Functions, loops, conditional statements, and dictionaries.
- String comparison and character-based calculations.
- Random selection using lists and the `random` module.
- SQLite database creation, insertion, retrieval, and deletion.
- Persistent settings and historical records.
- Data analysis and statistics calculations.
- Data visualization with Matplotlib.
- CSV file generation and export.
- Input validation and error handling.
- Modular code organization and documentation.

## Limitations

- The predefined passage collection is limited.
- The current version uses one passage per test rather than continuously generating text.
- Custom passage entry and endless mode are not included in this standalone implementation.
- Character-by-character color highlighting is not implemented.
- WPM and accuracy use simplified character-based calculations.
- There is no online synchronization or cloud backup.
- There are no user accounts or separate user profiles.
- Achievements are calculated from saved results rather than stored as independent unlock records.
- Daily goal tracking counts completed tests rather than measuring consecutive-day streaks.
- The progress chart displays recent WPM results, not a detailed accuracy or consistency analysis.
- The daily goal and test history are stored locally on the current computer.

## Future Improvements

Potential future enhancements include:

- Character-by-character correct and incorrect highlighting.
- Custom passage creation and saving.
- Endless mode with continuously generated text.
- More practice passages and typing categories.
- Improved adjusted WPM calculations that account for mistakes.
- Accuracy and typing consistency charts.
- Consecutive-day practice streaks.
- More achievements and daily challenges.
- Keyboard shortcuts and configurable preferences.
- Adjustable font sizes and light/dark theme selection.
- More advanced history filtering and comparison tools.
- Database migration support for older TypeFlow versions.
- Data backup and restore options.
- Automated tests for typing calculations, timers, and database functions.
- Improved accessibility and interface customization.

---

# TypeFlow — Web Edition

TypeFlow also includes a browser-based version built with **HTML, CSS, and JavaScript**. The web edition lets users practice typing, track their performance, and review recent results directly in a web browser without installing Python packages.

## Web Version Features

### Typing Test

- **Timed Challenges** — Choose between 30-second, 60-second, and 120-second tests.
- **Difficulty Levels** — Practice with Easy, Medium, and Hard passages.
- **Live WPM** — Monitor estimated words per minute while typing.
- **Live Accuracy** — See the percentage of correctly typed characters.
- **Mistake Tracking** — Count characters that do not match the displayed passage.
- **Progress Bar** — Follow typing progress through the selected passage.
- **Instant Results** — View final WPM, accuracy, mistakes, and characters typed after a test.
- **Restart and Retry** — Reset the test or start another attempt.
- **Character Highlighting** — See correct and incorrect characters highlighted as you type.

### Web Dashboard and History

- **Personal Best** — View the highest saved WPM.
- **Average WPM** — Review average speed across saved tests.
- **Average Accuracy** — Review average accuracy across completed tests.
- **Total Tests** — Count completed typing sessions.
- **Recent Test History** — Review recent scores, accuracy, mistakes, duration, and difficulty.
- **Local Browser Storage** — Save test history and theme preferences using browser LocalStorage.
- **Dark and Light Themes** — Switch between dark and light appearance.
- **Responsive Layout** — Use the web interface on desktop and smaller screens.

## Web Technologies Used

| Technology | Purpose |
|---|---|
| HTML5 | Structures the web page and its controls |
| CSS3 | Styles the interface and responsive layout |
| JavaScript | Implements typing logic, timers, scoring, and dashboard updates |
| LocalStorage | Stores test history and theme preference in the browser |
| Google Fonts | Loads Inter and DM Mono typography when an internet connection is available |

## Web Project Structure

```text
typeflow-web/
├── index.html
├── style.css
└── script.js
```

### Web File Descriptions

- `index.html` — Contains the typing test interface, settings, live statistics, results panel, dashboard, and recent history table.
- `style.css` — Defines the dark/light themes, responsive layout, passage highlighting, statistic cards, and other visual styles.
- `script.js` — Handles passage selection, typing input, countdown timer, WPM and accuracy calculations, results, browser storage, test history, and theme switching.

## Running the Web Version

1. Download or clone the repository containing the `typeflow-web` folder.
2. Open the `typeflow-web` folder in Visual Studio Code or another code editor.
3. Make sure `index.html`, `style.css`, and `script.js` are in the same folder.
4. Open `index.html` in a web browser, or use the VS Code Live Server extension.

The web edition runs in the browser and does not require Python, CustomTkinter, SQLite, or Matplotlib.

## Web Version Data Storage

The web edition uses browser LocalStorage rather than the desktop application's SQLite database.

- Typing results are stored in the current browser.
- The latest 100 completed test results are retained.
- The dashboard displays the latest 10 results.
- Theme preference is saved in the browser.
- Data is not automatically shared or synchronized across browsers or devices.
- Clearing browser site data may remove saved web results.

**Note:** The desktop and web editions keep their data separately. Results saved in the Python application's SQLite database do not automatically appear in the web edition, and vice versa.

## Web Version Notes and Limitations

- The web edition uses a predefined collection of passages for each difficulty.
- Each test uses one passage.
- WPM is estimated from correctly typed characters, using five characters as one word.
- The countdown begins when the user selects **Start Test**.
- A test ends when the timer expires or the passage is completed.
- Browser LocalStorage is local to the current browser profile and is not a cloud database.
- Google Fonts requires an internet connection to load; fallback fonts are used if unavailable.
- The web version does not currently include the desktop edition's SQLite history search, CSV export, achievements, daily goals, or pause/resume controls.

## Publishing the Web Version

The web edition can be hosted as a static website using **GitHub Pages**:

1. Push the `typeflow-web` folder and its three files to your GitHub repository.
2. Open the repository's **Settings**.
3. Select **Pages**.
4. Choose the branch and folder containing the web files.
5. Save the settings and wait for GitHub Pages to publish the site.

Check GitHub Pages' current instructions for the exact publishing options available for your repository.

## Author

**Jose Navoa**

Aspiring Information Technology Student

*Built with Python as a learning project focused on desktop application development, typing performance analysis, data visualization, and database management.*
