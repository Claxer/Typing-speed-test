const textDisplay = document.getElementById("textDisplay");
const typingInput = document.getElementById("typingInput");
const startButton = document.getElementById("startButton");
const restartButton = document.getElementById("restartButton");
const tryAgainButton = document.getElementById("tryAgainButton");
const difficultySelect = document.getElementById("difficulty");
const themeButton = document.getElementById("themeButton");

const wpmDisplay = document.getElementById("wpm");
const accuracyDisplay = document.getElementById("accuracy");
const timerDisplay = document.getElementById("timer");
const mistakesDisplay = document.getElementById("mistakes");
const progressBar = document.getElementById("progressBar");
const statusMessage = document.getElementById("statusMessage");

const resultPanel = document.getElementById("resultPanel");
const historyTable = document.getElementById("historyTable");

const passages = {
    easy: [
        "Small steps can lead to big changes. Practice every day and keep learning new things. Stay patient and enjoy the journey.",
        "A good morning starts with a clear mind. Take your time, focus on your goals, and do your best in everything you do.",
        "Learning something new can be difficult at first. With enough practice, simple habits can help you improve every day."
    ],

    medium: [
        "Programming teaches us how to solve problems through logic, creativity, and patience. Every mistake is an opportunity to understand something new.",
        "Technology continues to change the way people communicate, learn, and work. Building useful skills today can open doors to better opportunities tomorrow.",
        "Consistency is often more important than motivation. Small improvements made regularly can eventually produce impressive results over time."
    ],

    hard: [
        "Efficient software requires thoughtful architecture, reliable testing, and careful attention to detail. Developers must balance performance, security, and maintainability.",
        "Debugging a complicated application requires patience, logical reasoning, and systematic investigation. A well-documented solution can prevent similar problems in the future.",
        "Modern applications frequently integrate asynchronous operations, sophisticated algorithms, and external services while maintaining a responsive user experience."
    ]
};

let selectedDuration = 30;
let timeLeft = selectedDuration;
let timerInterval = null;
let startTime = null;
let testActive = false;
let testFinished = false;
let currentPassage = "";
let testStarted = false;

const HISTORY_KEY = "typeflowHistory";
const THEME_KEY = "typeflowTheme";

function getHistory() {
    try {
        const savedHistory = JSON.parse(
            localStorage.getItem(HISTORY_KEY) || "[]"
        );

        return Array.isArray(savedHistory) ? savedHistory : [];
    } catch (error) {
        return [];
    }
}

function saveHistory(history) {
    try {
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    } catch (error) {
        statusMessage.textContent =
            "Your browser could not save the test history.";
    }
}

function getRandomPassage() {
    const selectedDifficulty = difficultySelect.value;
    const options = passages[selectedDifficulty];

    return options[Math.floor(Math.random() * options.length)];
}

function displayPassage() {
    textDisplay.innerHTML = "";

    for (let i = 0; i < currentPassage.length; i++) {
        const character = document.createElement("span");

        character.textContent = currentPassage[i];
        textDisplay.appendChild(character);
    }

    updateCharacterDisplay();
}

function updateCharacterDisplay() {
    const typedText = typingInput.value;
    const characters = textDisplay.querySelectorAll("span");

    let correctCharacters = 0;
    let mistakes = 0;

    characters.forEach((character, index) => {
        character.classList.remove("correct", "incorrect", "current");

        if (index < typedText.length) {
            if (typedText[index] === currentPassage[index]) {
                character.classList.add("correct");
                correctCharacters++;
            } else {
                character.classList.add("incorrect");
                mistakes++;
            }
        } else if (index === typedText.length) {
            character.classList.add("current");
        }
    });

    mistakesDisplay.textContent = mistakes;

    const accuracy = typedText.length > 0
        ? Math.round((correctCharacters / typedText.length) * 100)
        : 100;

    accuracyDisplay.innerHTML = `${accuracy}<span class="unit">%</span>`;

    const progress = currentPassage.length > 0
        ? (typedText.length / currentPassage.length) * 100
        : 0;

    progressBar.style.width = `${Math.min(progress, 100)}%`;

    updateWpm(correctCharacters);

    return {
        correctCharacters,
        mistakes,
        accuracy
    };
}

function getElapsedSeconds() {
    if (!startTime) {
        return 0;
    }

    return Math.max(0, (Date.now() - startTime) / 1000);
}

function updateWpm(correctCharacters) {
    const elapsedMinutes = getElapsedSeconds() / 60;

    if (elapsedMinutes <= 0) {
        wpmDisplay.textContent = "0";
        return;
    }

    const currentWpm = Math.round(
        (correctCharacters / 5) / elapsedMinutes
    );

    wpmDisplay.textContent = currentWpm;
}

function startTest() {
    if (testActive) {
        typingInput.focus();
        return;
    }

    if (testFinished) {
        resetTest();
    }

    if (!testStarted) {
        currentPassage = getRandomPassage();
        displayPassage();
        testStarted = true;
    }

    testActive = true;
    startTime = Date.now();

    typingInput.disabled = false;
    typingInput.focus();

    startButton.disabled = true;
    startButton.textContent = "Test Running...";
    statusMessage.textContent = "Type the passage as accurately as possible.";

    timerInterval = setInterval(updateTimer, 100);
}

function updateTimer() {
    if (!testActive) {
        return;
    }

    const elapsed = getElapsedSeconds();

    timeLeft = Math.max(
        0,
        selectedDuration - Math.floor(elapsed)
    );

    timerDisplay.innerHTML = `${timeLeft}<span class="unit">s</span>`;

    if (timeLeft <= 0) {
        finishTest();
    }
}

function handleTyping() {
    if (!testActive || testFinished) {
        return;
    }

    // Prevent typing beyond the displayed passage.
    if (typingInput.value.length > currentPassage.length) {
        typingInput.value = typingInput.value.slice(
            0,
            currentPassage.length
        );
    }

    const stats = updateCharacterDisplay();

    if (typingInput.value.length === currentPassage.length) {
        finishTest();
    } else if (typingInput.value.length > 0) {
        statusMessage.textContent = "Keep going. Stay focused!";
    }

    return stats;
}

function finishTest() {
    if (testFinished) {
        return;
    }

    testActive = false;
    testFinished = true;

    clearInterval(timerInterval);

    if (startTime) {
        const elapsed = getElapsedSeconds();

        timeLeft = Math.max(
            0,
            selectedDuration - Math.floor(elapsed)
        );
    }

    timerDisplay.innerHTML = `${timeLeft}<span class="unit">s</span>`;

    typingInput.disabled = true;
    startButton.disabled = false;
    startButton.textContent = "Start Test →";

    const stats = updateCharacterDisplay();
    const elapsedMinutes = getElapsedSeconds() / 60;

    const finalWpm = elapsedMinutes > 0
        ? Math.round(
            (stats.correctCharacters / 5) / elapsedMinutes
        )
        : 0;

    document.getElementById("finalWpm").textContent = finalWpm;
    document.getElementById("finalAccuracy").textContent =
        `${stats.accuracy}%`;
    document.getElementById("finalMistakes").textContent =
        stats.mistakes;
    document.getElementById("finalCharacters").textContent =
        typingInput.value.length;

    statusMessage.textContent = "Test completed! Check your results.";

    resultPanel.classList.remove("hidden");

    saveTestResult({
        wpm: finalWpm,
        accuracy: stats.accuracy,
        mistakes: stats.mistakes,
        characters: typingInput.value.length,
        duration: selectedDuration,
        difficulty: difficultySelect.value,
        date: new Date().toISOString()
    });

    updateDashboard();

    resultPanel.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}

function resetTest() {
    clearInterval(timerInterval);

    timerInterval = null;
    timeLeft = selectedDuration;
    startTime = null;
    testActive = false;
    testFinished = false;
    testStarted = false;

    typingInput.value = "";
    typingInput.disabled = true;

    startButton.disabled = false;
    startButton.textContent = "Start Test →";

    timerDisplay.innerHTML =
        `${selectedDuration}<span class="unit">s</span>`;

    wpmDisplay.textContent = "0";
    accuracyDisplay.innerHTML = '100<span class="unit">%</span>';
    mistakesDisplay.textContent = "0";
    progressBar.style.width = "0%";

    statusMessage.textContent = "Ready when you are.";

    resultPanel.classList.add("hidden");

    currentPassage = getRandomPassage();
    displayPassage();
}

function saveTestResult(result) {
    const history = getHistory();

    history.unshift(result);

    // Keep the latest 100 completed tests.
    saveHistory(history.slice(0, 100));
}

function updateDashboard() {
    const history = getHistory();

    const personalBest = history.length > 0
        ? Math.max(...history.map(test => Number(test.wpm) || 0))
        : 0;

    const averageWpm = history.length > 0
        ? Math.round(
            history.reduce(
                (total, test) => total + (Number(test.wpm) || 0),
                0
            ) / history.length
        )
        : 0;

    const averageAccuracy = history.length > 0
        ? Math.round(
            history.reduce(
                (total, test) => total + (Number(test.accuracy) || 0),
                0
            ) / history.length
        )
        : 0;

    document.getElementById("personalBest").innerHTML =
        `${personalBest} <small>WPM</small>`;

    document.getElementById("averageWpm").innerHTML =
        `${averageWpm} <small>WPM</small>`;

    document.getElementById("totalTests").textContent =
        history.length;

    document.getElementById("averageAccuracy").textContent =
        `${averageAccuracy}%`;

    document.getElementById("historyCount").textContent =
        `${history.length} test${history.length === 1 ? "" : "s"}`;

    renderHistory(history);
}

function renderHistory(history) {
    historyTable.innerHTML = "";

    if (history.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 5;
        cell.className = "empty-state";
        cell.textContent = "No tests yet. Complete your first test!";

        row.appendChild(cell);
        historyTable.appendChild(row);

        return;
    }

    history.slice(0, 10).forEach(test => {
        const row = document.createElement("tr");

        const date = new Date(test.date);
        const dateText = Number.isNaN(date.getTime())
            ? "Unknown date"
            : date.toLocaleString([], {
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            });

        const values = [
            dateText,
            `${Number(test.wpm) || 0} WPM`,
            `${Number(test.accuracy) || 0}%`,
            Number(test.mistakes) || 0,
            `${test.duration || 30}s · ${test.difficulty || "medium"}`
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        historyTable.appendChild(row);
    });
}

function changeDuration(duration) {
    if (testActive) {
        return;
    }

    selectedDuration = duration;
    resetTest();

    document.querySelectorAll("#durationOptions .option")
        .forEach(button => {
            button.classList.toggle(
                "active",
                Number(button.dataset.duration) === duration
            );
        });
}

function toggleTheme() {
    document.body.classList.toggle("light-theme");

    const isLight = document.body.classList.contains("light-theme");

    themeButton.textContent = isLight ? "☾" : "☼";

    try {
        localStorage.setItem(
            THEME_KEY,
            isLight ? "light" : "dark"
        );
    } catch (error) {
        // The theme still works for the current session.
    }
}

function loadTheme() {
    try {
        const savedTheme = localStorage.getItem(THEME_KEY);

        if (savedTheme === "light") {
            document.body.classList.add("light-theme");
            themeButton.textContent = "☾";
        } else {
            themeButton.textContent = "☼";
        }
    } catch (error) {
        themeButton.textContent = "☼";
    }
}

// Start and restart controls.
startButton.addEventListener("click", startTest);
restartButton.addEventListener("click", resetTest);
tryAgainButton.addEventListener("click", resetTest);

// Typing input.
typingInput.addEventListener("input", handleTyping);

// Clicking the passage focuses the typing area when available.
textDisplay.addEventListener("click", () => {
    if (testActive) {
        typingInput.focus();
    }
});

// Duration controls.
document.querySelectorAll("#durationOptions .option")
    .forEach(button => {
        button.addEventListener("click", () => {
            changeDuration(Number(button.dataset.duration));
        });
    });

// Difficulty changes prepare a new passage.
difficultySelect.addEventListener("change", () => {
    if (!testActive) {
        resetTest();
    }
});

// Theme control.
themeButton.addEventListener("click", toggleTheme);

// Clear saved statistics.
document.getElementById("clearHistoryButton")
    .addEventListener("click", () => {
        const confirmed = confirm(
            "Are you sure you want to clear all typing test history?"
        );

        if (!confirmed) {
            return;
        }

        saveHistory([]);
        updateDashboard();

        statusMessage.textContent = "Your test history has been cleared.";
    });

// Initialize the application.
loadTheme();
resetTest();
updateDashboard();
