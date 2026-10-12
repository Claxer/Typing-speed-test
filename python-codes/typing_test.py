
import time
import customtkinter as ctk
from tkinter import messagebox
from passages import get_passage


class TypingTestFrame(ctk.CTkFrame):
    def __init__(self, parent, on_finish, on_back):
        super().__init__(parent, fg_color="transparent")

        self.on_finish = on_finish
        self.on_back = on_back

        self.difficulty = "Medium"
        self.duration = 60
        self.passage = ""

        self.started_at = None
        self.after_id = None
        self.running = False
        self.finished = False

        self.grid_columnconfigure(0, weight=1)

        # Page title
        ctk.CTkLabel(
            self,
            text="Typing Test",
            font=ctk.CTkFont(size=28, weight="bold")
        ).grid(
            row=0, column=0, sticky="w",
            padx=24, pady=(20, 4)
        )

        ctk.CTkLabel(
            self,
            text="Type the passage accurately before time runs out.",
            text_color="gray"
        ).grid(
            row=1, column=0, sticky="w",
            padx=24, pady=(0, 18)
        )

        # Difficulty and duration settings
        options = ctk.CTkFrame(self, corner_radius=12)
        options.grid(
            row=2, column=0, sticky="ew",
            padx=24, pady=(0, 14)
        )
        options.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            options,
            text="Difficulty"
        ).grid(
            row=0, column=0, padx=12, pady=(12, 4)
        )

        self.difficulty_menu = ctk.CTkOptionMenu(
            options,
            values=["Easy", "Medium", "Hard"],
            command=self.change_difficulty
        )
        self.difficulty_menu.set("Medium")
        self.difficulty_menu.grid(
            row=1, column=0, padx=12,
            pady=(0, 12), sticky="ew"
        )

        ctk.CTkLabel(
            options,
            text="Duration"
        ).grid(
            row=0, column=1, padx=12, pady=(12, 4)
        )

        self.duration_menu = ctk.CTkOptionMenu(
            options,
            values=["30 seconds", "60 seconds", "120 seconds"],
            command=self.change_duration
        )
        self.duration_menu.set("60 seconds")
        self.duration_menu.grid(
            row=1, column=1, padx=12,
            pady=(0, 12), sticky="ew"
        )

        self.timer_label = ctk.CTkLabel(
            options,
            text="60s",
            font=ctk.CTkFont(size=25, weight="bold")
        )
        self.timer_label.grid(
            row=0, column=2, rowspan=2,
            padx=12, pady=12
        )

        # Live statistics
        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.grid(
            row=3, column=0, sticky="ew",
            padx=24, pady=(0, 14)
        )
        stats.grid_columnconfigure((0, 1, 2), weight=1)

        self.wpm_label = self.make_stat(
            stats, "WPM", "0.0", 0
        )
        self.accuracy_label = self.make_stat(
            stats, "ACCURACY", "100%", 1
        )
        self.errors_label = self.make_stat(
            stats, "ERRORS", "0", 2
        )

        # Passage display
        self.passage_box = ctk.CTkTextbox(
            self,
            height=150,
            wrap="word",
            font=ctk.CTkFont(size=19),
            corner_radius=12
        )
        self.passage_box.grid(
            row=4, column=0, sticky="ew",
            padx=24, pady=(0, 12)
        )
        self.passage_box.configure(state="disabled")

        ctk.CTkLabel(
            self,
            text="Start typing below. The timer begins with your first character.",
            text_color="gray"
        ).grid(
            row=5, column=0, sticky="w",
            padx=24, pady=(0, 6)
        )

        # Typing input
        self.input_box = ctk.CTkTextbox(
            self,
            height=125,
            wrap="word",
            font=ctk.CTkFont(size=17),
            corner_radius=12
        )
        self.input_box.grid(
            row=6, column=0, sticky="ew",
            padx=24, pady=(0, 14)
        )
        self.input_box.bind("<KeyRelease>", self.handle_typing)

        # Action buttons
        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(
            row=7, column=0, sticky="ew",
            padx=24, pady=(0, 20)
        )

        ctk.CTkButton(
            buttons,
            text="New Passage / Restart",
            command=self.reset_test
        ).pack(side="left")

        ctk.CTkButton(
            buttons,
            text="Finish Test",
            command=self.finish_test
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="Back",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.leave_test
        ).pack(side="right")

        self.reset_test()

    # Create a statistics card
    def make_stat(self, parent, title, value, column):
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=6,
            pady=2
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="gray"
        ).pack(pady=(10, 2))

        label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=23, weight="bold")
        )
        label.pack(pady=(0, 10))

        return label

    # Change difficulty and generate a new passage
    def change_difficulty(self, value):
        self.difficulty = value
        self.reset_test()

    # Change the test duration
    def change_duration(self, value):
        self.duration = int(value.split()[0])
        self.reset_test()

    # Cancel an existing timer callback
    def cancel_timer(self):
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass

        self.after_id = None

    # Reset the test
    def reset_test(self):
        self.cancel_timer()

        self.running = False
        self.finished = False
        self.started_at = None

        self.passage = get_passage(self.difficulty)

        self.timer_label.configure(
            text=f"{self.duration}s"
        )
        self.wpm_label.configure(text="0.0")
        self.accuracy_label.configure(text="100%")
        self.errors_label.configure(text="0")

        # Display the passage
        self.passage_box.configure(state="normal")
        self.passage_box.delete("1.0", "end")
        self.passage_box.insert("1.0", self.passage)

        # FIX: Text tags require a single color string.
        # Do not use a tuple of colors here.
        self.passage_box.tag_config(
            "correct",
            foreground="#36b37e"
        )
        self.passage_box.tag_config(
            "incorrect",
            foreground="#ff5c5c"
        )
        self.passage_box.tag_config(
            "remaining",
            foreground="#B0B0B0"
        )

        self.passage_box.tag_add(
            "remaining", "1.0", "end"
        )
        self.passage_box.configure(state="disabled")

        # Clear the typing area
        self.input_box.configure(state="normal")
        self.input_box.delete("1.0", "end")
        self.input_box.focus_set()

    # Process typing and update statistics
    def handle_typing(self, event=None):
        if self.finished:
            return

        typed = self.input_box.get("1.0", "end-1c")

        if not typed:
            self.update_metrics(typed)
            self.highlight_text(typed)
            return

        # Start the timer when typing begins
        if not self.running:
            self.running = True
            self.started_at = time.monotonic()
            self.tick()

        self.update_metrics(typed)
        self.highlight_text(typed)

        # Finish if the complete passage has been typed
        if len(typed) >= len(self.passage):
            self.finish_test()

    # Calculate WPM, accuracy, and errors
    def update_metrics(self, typed):
        if self.started_at is None:
            elapsed = 0
        else:
            elapsed = max(
                1,
                int(time.monotonic() - self.started_at)
            )

        correct = sum(
            1
            for i, char in enumerate(typed[:len(self.passage)])
            if char == self.passage[i]
        )

        errors = sum(
            1
            for i, char in enumerate(typed)
            if i >= len(self.passage)
            or char != self.passage[i]
        )

        minutes = max(elapsed / 60, 1 / 60)

        raw_wpm = (len(typed) / 5) / minutes if typed else 0
        wpm = (correct / 5) / minutes if typed else 0

        accuracy = (
            correct / len(typed) * 100
            if typed else 100
        )

        self.wpm_label.configure(
            text=f"{wpm:.1f}"
        )
        self.accuracy_label.configure(
            text=f"{accuracy:.1f}%"
        )
        self.errors_label.configure(
            text=str(errors)
        )

        return {
            "wpm": round(wpm, 1),
            "raw_wpm": round(raw_wpm, 1),
            "accuracy": round(accuracy, 1),
            "correct_chars": correct,
            "incorrect_chars": errors,
            "typed_chars": len(typed)
        }

    # Highlight correct, incorrect, and remaining characters
    def highlight_text(self, typed):
        self.passage_box.configure(state="normal")

        self.passage_box.tag_remove(
            "correct", "1.0", "end"
        )
        self.passage_box.tag_remove(
            "incorrect", "1.0", "end"
        )
        self.passage_box.tag_remove(
            "remaining", "1.0", "end"
        )

        for index, char in enumerate(self.passage):
            start = f"1.0+{index}c"
            end = f"1.0+{index + 1}c"

            if index < len(typed):
                if typed[index] == char:
                    tag = "correct"
                else:
                    tag = "incorrect"
            else:
                tag = "remaining"

            self.passage_box.tag_add(
                tag, start, end
            )

        self.passage_box.configure(state="disabled")

    # Update the countdown timer
    def tick(self):
        if not self.running or self.finished:
            return

        elapsed = time.monotonic() - self.started_at
        remaining = max(
            0,
            self.duration - int(elapsed)
        )

        self.timer_label.configure(
            text=f"{remaining}s"
        )

        typed = self.input_box.get("1.0", "end-1c")
        self.update_metrics(typed)

        if elapsed >= self.duration:
            self.finish_test()
        else:
            self.after_id = self.after(
                200, self.tick
            )

    # Finish the test and send results to main.py
    def finish_test(self):
        if self.finished:
            return

        typed = self.input_box.get("1.0", "end-1c")

        if not typed.strip() and self.started_at is None:
            messagebox.showinfo(
                "No typing yet",
                "Type at least one character before finishing."
            )
            return

        elapsed = (
            0
            if self.started_at is None
            else min(
                self.duration,
                time.monotonic() - self.started_at
            )
        )

        self.cancel_timer()
        self.finished = True
        self.running = False

        self.input_box.configure(state="disabled")

        metrics = self.update_metrics(typed)
        metrics["difficulty"] = self.difficulty
        metrics["duration"] = self.duration
        metrics["elapsed_seconds"] = round(elapsed, 1)

        self.on_finish(metrics)

    # Return to the previous page
    def leave_test(self):
        self.cancel_timer()
        self.running = False
        self.on_back()
