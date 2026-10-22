import time
import customtkinter as ctk

from passages import get_passage
from database import save_result


class TypingTestFrame(ctk.CTkFrame):
    def __init__(self, master, on_complete=None):
        super().__init__(master, fg_color="transparent")

        self.on_complete = on_complete
        self.duration = 30
        self.remaining = 30
        self.difficulty = "Easy"
        self.passage = ""
        self.started_at = None
        self.elapsed_before_pause = 0
        self.running = False
        self.finished = False
        self.after_id = None

        ctk.CTkLabel(
            self,
            text="Typing Test",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", pady=(0, 18))

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", pady=5)

        self.duration_menu = ctk.CTkOptionMenu(
            controls,
            values=["30", "60", "120"],
            command=self.change_duration
        )
        self.duration_menu.pack(side="left", padx=(0, 10))

        self.difficulty_menu = ctk.CTkOptionMenu(
            controls,
            values=["Easy", "Medium", "Hard"],
            command=self.change_difficulty
        )
        self.difficulty_menu.pack(side="left", padx=10)

        self.timer_label = ctk.CTkLabel(
            self, text="30 seconds",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.timer_label.pack(pady=10)

        self.passage_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=18),
            wraplength=750,
            justify="left"
        )
        self.passage_label.pack(fill="x", pady=15)

        self.text_input = ctk.CTkTextbox(
            self,
            height=150,
            font=ctk.CTkFont(size=16),
            wrap="word"
        )
        self.text_input.pack(fill="x", pady=10)
        self.text_input.bind("<KeyRelease>", self.on_typing)

        self.stats_label = ctk.CTkLabel(
            self,
            text="WPM: 0 | Accuracy: 100% | Mistakes: 0"
        )
        self.stats_label.pack(pady=10)

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(pady=10)

        self.pause_button = ctk.CTkButton(
            buttons,
            text="Pause",
            command=self.toggle_pause,
            state="disabled"
        )
        self.pause_button.pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Restart",
            command=self.restart
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Finish Test",
            command=self.finish_test
        ).pack(side="left", padx=5)

        self.restart()

    def change_duration(self, value):
        if not self.running and not self.finished:
            self.duration = int(value)
            self.restart()

    def change_difficulty(self, value):
        if not self.running and not self.finished:
            self.difficulty = value
            self.restart()

    def restart(self):
        self.cancel_timer()

        self.duration = int(self.duration_menu.get())
        self.difficulty = self.difficulty_menu.get()
        self.remaining = self.duration
        self.passage = get_passage(self.difficulty)
        self.started_at = None
        self.elapsed_before_pause = 0
        self.running = False
        self.finished = False

        self.passage_label.configure(text=self.passage)
        self.text_input.configure(state="normal")
        self.text_input.delete("1.0", "end")
        self.pause_button.configure(
            text="Pause", state="disabled"
        )
        self.timer_label.configure(
            text=f"{self.remaining} seconds"
        )
        self.stats_label.configure(
            text="WPM: 0 | Accuracy: 100% | Mistakes: 0"
        )

    def cancel_timer(self):
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

    def on_typing(self, event=None):
        if self.finished or not self.running and self.started_at is not None:
            return

        if not self.running:
            if self.started_at is None:
                self.started_at = time.monotonic()
                self.running = True
                self.pause_button.configure(state="normal")
                self.tick()
            else:
                return

        self.update_stats()

    def get_typed_text(self):
        return self.text_input.get("1.0", "end-1c")

    def calculate_stats(self):
        typed = self.get_typed_text()
        elapsed = self.get_elapsed()

        correct = sum(
            1 for i, char in enumerate(typed)
            if i < len(self.passage)
            and char == self.passage[i]
        )

        mistakes = sum(
            1 for i, char in enumerate(typed)
            if i >= len(self.passage)
            or char != self.passage[i]
        )

        accuracy = (
            correct / len(typed) * 100
            if typed else 100
        )

        wpm = (
            len(typed) / 5 / (elapsed / 60)
            if elapsed > 0 else 0
        )

        return wpm, accuracy, mistakes, len(typed)

    def get_elapsed(self):
        if self.started_at is None:
            return 0

        if self.running:
            return max(
                0,
                time.monotonic()
                - self.started_at
                + self.elapsed_before_pause
            )

        return self.elapsed_before_pause

    def update_stats(self):
        wpm, accuracy, mistakes, _ = self.calculate_stats()

        self.stats_label.configure(
            text=(
                f"WPM: {wpm:.1f} | "
                f"Accuracy: {accuracy:.1f}% | "
                f"Mistakes: {mistakes}"
            )
        )

    def tick(self):
        self.after_id = None

        if not self.running or self.finished:
            return

        elapsed = self.get_elapsed()
        self.remaining = max(
            0, self.duration - int(elapsed)
        )

        self.timer_label.configure(
            text=f"{self.remaining} seconds"
        )
        self.update_stats()

        if self.remaining <= 0:
            self.finish_test()
        else:
            self.after_id = self.after(200, self.tick)

    def toggle_pause(self):
        if self.finished:
            return

        if self.running:
            self.elapsed_before_pause = self.get_elapsed()
            self.running = False
            self.cancel_timer()
            self.pause_button.configure(text="Resume")
            self.text_input.configure(state="disabled")
        else:
            if self.started_at is None:
                return

            self.started_at = time.monotonic()
            self.running = True
            self.pause_button.configure(text="Pause")
            self.text_input.configure(state="normal")
            self.text_input.focus_set()
            self.tick()

    def finish_test(self):
        if self.finished:
            return

        self.finished = True
        self.running = False
        self.cancel_timer()
        self.pause_button.configure(state="disabled")
        self.text_input.configure(state="disabled")

        elapsed = min(
            self.duration,
            max(1, int(self.get_elapsed()))
        )

        wpm, accuracy, mistakes, characters = (
            self.calculate_stats()
        )

        save_result(
            wpm,
            accuracy,
            mistakes,
            elapsed,
            self.difficulty,
            characters
        )

        self.timer_label.configure(text="Test completed!")

        self.stats_label.configure(
            text=(
                f"Final WPM: {wpm:.1f} | "
                f"Accuracy: {accuracy:.1f}% | "
                f"Mistakes: {mistakes}"
            )
        )

        if self.on_complete:
            self.on_complete()

        self.passage_label.configure(
            text=f"Your result: {wpm:.1f} WPM"
        )
