
import time
import customtkinter as ctk
from passages import get_passage


class TypingTestFrame(ctk.CTkFrame):
    def __init__(self, parent, on_complete, on_back):
        super().__init__(parent, fg_color="transparent")

        self.on_complete = on_complete
        self.on_back = on_back

        self.difficulty = "Easy"
        self.duration = 60
        self.passage = ""
        self.start_time = None
        self.remaining_time = 60
        self.timer_running = False
        self.finished = False
        self.timer_job = None

        self.pack(fill="both", expand=True)
        self.build_interface()

    def build_interface(self):
        ctk.CTkLabel(
            self,
            text="Typing Test",
            font=ctk.CTkFont(size=30, weight="bold")
        ).pack(anchor="w", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            self,
            text="Type the passage as accurately as possible.",
            text_color="gray"
        ).pack(anchor="w", padx=30, pady=(0, 20))

        settings = ctk.CTkFrame(self, fg_color="#202020", corner_radius=12)
        settings.pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(settings, text="Difficulty").pack(
            side="left", padx=(15, 8), pady=15
        )

        self.difficulty_menu = ctk.CTkOptionMenu(
            settings,
            values=["Easy", "Medium", "Hard"],
            command=self.change_difficulty,
            width=120
        )
        self.difficulty_menu.pack(side="left", padx=5, pady=15)

        ctk.CTkLabel(settings, text="Duration").pack(
            side="left", padx=(20, 8), pady=15
        )

        self.duration_menu = ctk.CTkOptionMenu(
            settings,
            values=["30 seconds", "60 seconds", "120 seconds"],
            command=self.change_duration,
            width=140
        )
        self.duration_menu.set("60 seconds")
        self.duration_menu.pack(side="left", padx=5, pady=15)

        self.timer_label = ctk.CTkLabel(
            self,
            text="60",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#60A5FA"
        )
        self.timer_label.pack(pady=(20, 10))

        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.pack(fill="x", padx=30, pady=10)

        self.wpm_label = self.make_stat(stats, "WPM", "0")
        self.accuracy_label = self.make_stat(stats, "Accuracy", "100%")
        self.mistakes_label = self.make_stat(stats, "Mistakes", "0")

        self.passage_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=17),
            wraplength=850,
            justify="left",
            anchor="w"
        )
        self.passage_label.pack(fill="x", padx=35, pady=(15, 10))

        self.text_box = ctk.CTkTextbox(
            self,
            height=150,
            font=ctk.CTkFont(size=16),
            wrap="word"
        )
        self.text_box.pack(fill="x", padx=30, pady=10)
        self.text_box.bind("<KeyRelease>", self.on_typing)

        self.status_label = ctk.CTkLabel(
            self,
            text="Choose your settings, then start typing.",
            text_color="gray"
        )
        self.status_label.pack(pady=5)

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(pady=15)

        ctk.CTkButton(
            buttons,
            text="New Passage",
            command=self.reset_test,
            width=140
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            buttons,
            text="Back to Dashboard",
            command=self.leave_test,
            fg_color="#404040",
            hover_color="#505050",
            width=170
        ).pack(side="left", padx=8)

        self.reset_test()

    def make_stat(self, parent, title, value):
        card = ctk.CTkFrame(parent, fg_color="#202020", corner_radius=10)
        card.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            card,
            text=title,
            text_color="gray"
        ).pack(pady=(12, 3))

        label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=(0, 12))

        return label

    def change_difficulty(self, value):
        self.difficulty = value
        self.reset_test()

    def change_duration(self, value):
        durations = {
            "30 seconds": 30,
            "60 seconds": 60,
            "120 seconds": 120
        }

        self.duration = durations[value]
        self.reset_test()

    def reset_test(self):
        if self.timer_job is not None:
            try:
                self.after_cancel(self.timer_job)
            except Exception:
                pass

        self.timer_job = None
        self.timer_running = False
        self.finished = False
        self.start_time = None
        self.remaining_time = self.duration
        self.passage = get_passage(self.difficulty)

        self.passage_label.configure(text=self.passage)
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")

        self.timer_label.configure(text=str(self.duration))
        self.wpm_label.configure(text="0")
        self.accuracy_label.configure(text="100%")
        self.mistakes_label.configure(text="0")
        self.status_label.configure(
            text="Start typing to begin the timer.",
            text_color="gray"
        )

        self.text_box.focus_set()

    def on_typing(self, event=None):
        if self.finished:
            return

        typed_text = self.text_box.get("1.0", "end-1c")

        if not self.timer_running and typed_text:
            self.start_time = time.time()
            self.timer_running = True
            self.status_label.configure(
                text="Test in progress...",
                text_color="#60A5FA"
            )
            self.update_timer()

        self.update_statistics(typed_text)

        if len(typed_text) >= len(self.passage):
            self.finish_test()

    def update_statistics(self, typed_text):
        correct_chars = 0

        for index, character in enumerate(typed_text):
            if index < len(self.passage):
                if character == self.passage[index]:
                    correct_chars += 1

        mistakes = len(typed_text) - correct_chars

        if self.start_time is not None:
            elapsed = max(time.time() - self.start_time, 1)
            wpm = (correct_chars / 5) / (elapsed / 60)
        else:
            wpm = 0

        if typed_text:
            accuracy = (correct_chars / len(typed_text)) * 100
        else:
            accuracy = 100

        self.wpm_label.configure(text=str(round(wpm)))
        self.accuracy_label.configure(text=f"{accuracy:.1f}%")
        self.mistakes_label.configure(text=str(mistakes))

    def update_timer(self):
        if self.finished or not self.timer_running:
            return

        elapsed = time.time() - self.start_time
        self.remaining_time = max(0, self.duration - int(elapsed))

        self.timer_label.configure(text=str(self.remaining_time))

        if self.remaining_time <= 0:
            self.finish_test()
        else:
            self.timer_job = self.after(200, self.update_timer)

    def finish_test(self):
        if self.finished:
            return

        self.finished = True
        self.timer_running = False

        if self.timer_job is not None:
            try:
                self.after_cancel(self.timer_job)
            except Exception:
                pass

            self.timer_job = None

        typed_text = self.text_box.get("1.0", "end-1c")

        correct_chars = sum(
            1 for index, character in enumerate(typed_text)
            if index < len(self.passage)
            and character == self.passage[index]
        )

        mistakes = len(typed_text) - correct_chars

        if self.start_time is not None:
            elapsed = max(time.time() - self.start_time, 1)
            wpm = (correct_chars / 5) / (elapsed / 60)
        else:
            wpm = 0

        accuracy = (
            (correct_chars / len(typed_text)) * 100
            if typed_text else 100
        )

        self.wpm_label.configure(text=str(round(wpm)))
        self.accuracy_label.configure(text=f"{accuracy:.1f}%")
        self.mistakes_label.configure(text=str(mistakes))
        self.timer_label.configure(text="0")
        self.text_box.configure(state="disabled")

        self.status_label.configure(
            text="Test completed! View your results.",
            text_color="#4ADE80"
        )

        result = {
            "wpm": round(wpm, 2),
            "accuracy": round(accuracy, 2),
            "mistakes": mistakes,
            "difficulty": self.difficulty,
            "duration": self.duration,
            "correct_chars": correct_chars,
            "typed_chars": len(typed_text)
        }

        self.on_complete(result)

    def leave_test(self):
        if self.timer_job is not None:
            try:
                self.after_cancel(self.timer_job)
            except Exception:
                pass

        self.timer_job = None
        self.timer_running = False
        self.on_back()
