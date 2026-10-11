
import customtkinter as ctk
from database import (
    get_history,
    get_personal_best,
    get_total_tests,
    get_average_wpm
)


class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent, on_back, on_start):
        super().__init__(parent, fg_color="transparent")

        self.on_back = on_back
        self.on_start = on_start
        self.latest_result = None

        self.build_interface()

    def build_interface(self):
        ctk.CTkLabel(
            self,
            text="Your Results",
            font=ctk.CTkFont(size=30, weight="bold")
        ).pack(anchor="w", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            self,
            text="Review your performance and previous typing tests.",
            text_color="gray"
        ).pack(anchor="w", padx=30, pady=(0, 20))

        self.latest_frame = ctk.CTkFrame(
            self, fg_color="#202020", corner_radius=12
        )
        self.latest_frame.pack(fill="x", padx=30, pady=5)

        self.latest_label = ctk.CTkLabel(
            self.latest_frame,
            text="Complete a typing test to see your latest results.",
            font=ctk.CTkFont(size=17),
            justify="left"
        )
        self.latest_label.pack(anchor="w", padx=20, pady=20)

        summary = ctk.CTkFrame(self, fg_color="transparent")
        summary.pack(fill="x", padx=25, pady=15)

        self.total_label = self.make_stat(summary, "Total Tests", "0")
        self.average_label = self.make_stat(summary, "Average WPM", "0")
        self.best_label = self.make_stat(summary, "Personal Best", "0")

        ctk.CTkLabel(
            self,
            text="Typing History",
            font=ctk.CTkFont(size=21, weight="bold")
        ).pack(anchor="w", padx=30, pady=(10, 8))

        self.history_box = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(size=13),
            wrap="none"
        )
        self.history_box.pack(
            fill="both", expand=True, padx=30, pady=5
        )

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(pady=20)

        ctk.CTkButton(
            buttons,
            text="Start Typing Test",
            command=self.on_start,
            width=160
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            buttons,
            text="Back to Dashboard",
            command=self.on_back,
            fg_color="#404040",
            hover_color="#505050",
            width=170
        ).pack(side="left", padx=8)

        self.refresh_history()

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

    def set_latest_result(self, result):
        self.latest_result = result

        self.latest_label.configure(
            text=(
                f"Typing Speed: {result['wpm']:.2f} WPM\n"
                f"Accuracy: {result['accuracy']:.2f}%\n"
                f"Mistakes: {result['mistakes']}\n"
                f"Difficulty: {result['difficulty']}\n"
                f"Test Duration: {result['duration']} seconds"
            )
        )

        self.refresh_history()

    def refresh_history(self):
        total = get_total_tests()
        average = get_average_wpm()
        best = get_personal_best()

        self.total_label.configure(text=str(total))
        self.average_label.configure(text=str(average))
        self.best_label.configure(
            text=f"{best[0]:.2f}" if best else "0"
        )

        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")

        self.history_box.insert(
            "end",
            f"{'ID':<5} {'WPM':<10} {'Accuracy':<12} "
            f"{'Mistakes':<10} {'Level':<10} {'Duration':<10} Date\n"
        )
        self.history_box.insert("end", "-" * 100 + "\n")

        history = get_history()

        if not history:
            self.history_box.insert(
                "end", "No typing tests recorded yet.\n"
            )
        else:
            for row in history:
                test_id, wpm, accuracy, mistakes, difficulty, duration, date = row

                self.history_box.insert(
                    "end",
                    f"{test_id:<5} {wpm:<10.2f} {accuracy:<12.2f} "
                    f"{mistakes:<10} {difficulty:<10} "
                    f"{duration:<10} {date}\n"
                )

        self.history_box.configure(state="disabled")
