
import time
import customtkinter as ctk

from passages import get_passage_for_mode
from database import save_result


class TypingTestFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_back,
        on_complete,
        mode="Timed",
        duration=60,
        difficulty="Easy",
        custom_text=""
    ):
        super().__init__(parent, fg_color="transparent")

        self.on_back = on_back
        self.on_complete = on_complete
        self.mode = mode
        self.duration = duration
        self.difficulty = difficulty
        self.custom_text = custom_text

        self.passage = get_passage_for_mode(
            difficulty, custom_text
        )

        self.start_time = None
        self.remaining_time = duration
        self.finished = False
        self.timer_job = None

        self.title_label = ctk.CTkLabel(
            self,
            text="Typing Test",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=(15, 5))

        self.info_label = ctk.CTkLabel(
            self,
            text=f"{mode} Mode  |  {difficulty}",
            font=("Arial", 13)
        )
        self.info_label.pack(pady=5)

        self.timer_label = ctk.CTkLabel(
            self,
            text=self._timer_text(),
            font=("Arial", 22, "bold")
        )
        self.timer_label.pack(pady=10)

        self.passage_box = ctk.CTkTextbox(
            self,
            height=140,
            font=("Arial", 17),
            wrap="word"
        )
        self.passage_box.pack(
            fill="x", padx=25, pady=10
        )
        self.passage_box.insert("1.0", self.passage)
        self.passage_box.configure(state="disabled")

        self.input_box = ctk.CTkTextbox(
            self,
            height=140,
            font=("Arial", 16),
            wrap="word"
        )
        self.input_box.pack(
            fill="x", padx=25, pady=10
        )

        self.input_box.bind("<KeyRelease>", self.update_stats)

        self.stats_label = ctk.CTkLabel(
            self,
            text="WPM: 0  |  Accuracy: 100%  |  Mistakes: 0",
            font=("Arial", 15)
        )
        self.stats_label.pack(pady=10)

        self.finish_button = ctk.CTkButton(
            self,
            text="Finish Test",
            command=self.finish_test
        )
        self.finish_button.pack(pady=10)

        self.back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back,
            fg_color="gray"
        )
        self.back_button.pack(pady=5)

        self.input_box.focus_set()

    def _timer_text(self):
        if self.mode == "Endless":
            return "Time: Unlimited"

        return f"Time Remaining: {self.remaining_time}s"

    def update_stats(self, event=None):
        if self.finished:
            return

        typed = self.input_box.get("1.0", "end-1c")

        if self.start_time is None and typed:
            self.start_time = time.time()

            if self.mode == "Timed":
                self.timer_job = self.after(
                    1000, self.update_timer
                )

        elapsed = self.elapsed_seconds()

        minutes = max(elapsed / 60, 1 / 60)
        wpm = (len(typed) / 5) / minutes

        matching = sum(
            1 for index, char in enumerate(typed)
            if index < len(self.passage)
            and char == self.passage[index]
        )

        accuracy = (
            matching / len(typed) * 100
            if typed else 100
        )

        mistakes = sum(
            1 for index, char in enumerate(typed)
            if index >= len(self.passage)
            or char != self.passage[index]
        )

        self.stats_label.configure(
            text=(
                f"WPM: {wpm:.1f}  |  "
                f"Accuracy: {accuracy:.1f}%  |  "
                f"Mistakes: {mistakes}"
            )
        )

        if self.mode == "Endless" and len(typed) >= len(self.passage):
            self.finish_test()

    def elapsed_seconds(self):
        if self.start_time is None:
            return 0

        return max(0, int(time.time() - self.start_time))

    def update_timer(self):
        if self.finished or self.mode != "Timed":
            return

        elapsed = self.elapsed_seconds()
        self.remaining_time = max(
            0, self.duration - elapsed
        )

        self.timer_label.configure(
            text=self._timer_text()
        )

        if self.remaining_time <= 0:
            self.finish_test()
        else:
            self.timer_job = self.after(
                1000, self.update_timer
            )

    def finish_test(self):
        if self.finished:
            return

        self.finished = True

        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        typed = self.input_box.get("1.0", "end-1c")
        elapsed = self.elapsed_seconds()

        minutes = max(elapsed / 60, 1 / 60)
        raw_wpm = (len(typed) / 5) / minutes

        matching = sum(
            1 for index, char in enumerate(typed)
            if index < len(self.passage)
            and char == self.passage[index]
        )

        mistakes = sum(
            1 for index, char in enumerate(typed)
            if index >= len(self.passage)
            or char != self.passage[index]
        )

        accuracy = (
            matching / len(typed) * 100
            if typed else 100
        )

        correct_words = sum(
            1 for typed_word, target_word in zip(
                typed.split(), self.passage.split()
            )
            if typed_word == target_word
        )

        wpm = raw_wpm

        save_result(
            wpm=wpm,
            raw_wpm=raw_wpm,
            accuracy=accuracy,
            mistakes=mistakes,
            correct_chars=matching,
            total_chars=len(typed),
            duration=elapsed,
            difficulty=self.difficulty,
            mode=self.mode
        )

        result = {
            "wpm": round(wpm, 1),
            "raw_wpm": round(raw_wpm, 1),
            "accuracy": round(accuracy, 1),
            "mistakes": mistakes,
            "correct_chars": matching,
            "total_chars": len(typed),
            "correct_words": correct_words,
            "duration": elapsed,
            "difficulty": self.difficulty,
            "mode": self.mode
        }

        self.on_complete(result)

    def go_back(self):
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        self.finished = True
        self.on_back()
