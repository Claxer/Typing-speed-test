
import customtkinter as ctk

from database import (
    create_tables,
    get_personal_best,
    get_total_tests,
    get_average_wpm,
    get_average_accuracy,
    get_progress_data
)
from typing_test import TypingTestFrame
from results import ResultsFrame


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TypeFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TypeFlow - Typing Speed Test")
        self.geometry("1000x750")
        self.minsize(850, 650)

        self.current_frame = None
        self.last_result = None

        self.show_dashboard()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        self.current_frame.pack(
            fill="both", expand=True, padx=20, pady=20
        )

    def show_dashboard(self):
        self.clear_frame()

        ctk.CTkLabel(
            self.current_frame,
            text="TypeFlow",
            font=("Arial", 34, "bold")
        ).pack(pady=(15, 3))

        ctk.CTkLabel(
            self.current_frame,
            text="Your personal typing improvement dashboard",
            font=("Arial", 14)
        ).pack(pady=(0, 20))

        stats = ctk.CTkFrame(self.current_frame)
        stats.pack(fill="x", pady=10)

        items = [
            ("Personal Best", f"{get_personal_best():.1f} WPM"),
            ("Total Tests", str(get_total_tests())),
            ("Average WPM", f"{get_average_wpm():.1f}"),
            ("Average Accuracy", f"{get_average_accuracy():.1f}%")
        ]

        for index, (label, value) in enumerate(items):
            card = ctk.CTkFrame(stats)
            card.grid(
                row=0, column=index,
                padx=6, pady=8, sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=label,
                font=("Arial", 12)
            ).pack(padx=10, pady=(12, 4))

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 20, "bold")
            ).pack(padx=10, pady=(4, 12))

            stats.grid_columnconfigure(
                index, weight=1
            )

        ctk.CTkLabel(
            self.current_frame,
            text="Start a Typing Test",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 10))

        settings = ctk.CTkFrame(self.current_frame)
        settings.pack(fill="x", pady=5)

        self.mode_var = ctk.StringVar(value="Timed")
        self.duration_var = ctk.StringVar(value="60")
        self.difficulty_var = ctk.StringVar(value="Medium")

        ctk.CTkLabel(
            settings, text="Mode"
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkOptionMenu(
            settings,
            variable=self.mode_var,
            values=["Timed", "Endless"]
        ).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(
            settings, text="Duration"
        ).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkOptionMenu(
            settings,
            variable=self.duration_var,
            values=["30", "60", "120"]
        ).grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkLabel(
            settings, text="Difficulty"
        ).grid(row=0, column=4, padx=10, pady=10)

        ctk.CTkOptionMenu(
            settings,
            variable=self.difficulty_var,
            values=["Easy", "Medium", "Hard"]
        ).grid(row=0, column=5, padx=10, pady=10)

        settings.grid_columnconfigure(
            tuple(range(6)), weight=1
        )

        ctk.CTkLabel(
            self.current_frame,
            text="Optional custom passage (leave empty for a random passage)"
        ).pack(anchor="w", pady=(15, 5))

        self.custom_text = ctk.CTkTextbox(
            self.current_frame, height=75
        )
        self.custom_text.pack(fill="x", pady=5)

        ctk.CTkButton(
            self.current_frame,
            text="Start Typing Test",
            height=42,
            command=self.start_test
        ).pack(pady=10)

        ctk.CTkButton(
            self.current_frame,
            text="View Results and History",
            command=self.show_results
        ).pack(pady=5)

        self.show_progress_summary()

    def show_progress_summary(self):
        data = get_progress_data()

        if not data["wpm"]:
            text = "Complete your first test to start tracking your progress."
        else:
            text = "Recent WPM: " + "  →  ".join(
                f"{value:.1f}" for value in data["wpm"][-8:]
            )

        ctk.CTkLabel(
            self.current_frame,
            text="Progress Overview",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self.current_frame,
            text=text,
            wraplength=850
        ).pack(pady=5)

    def start_test(self):
        mode = self.mode_var.get()
        duration = int(self.duration_var.get())
        difficulty = self.difficulty_var.get()
        custom_text = self.custom_text.get(
            "1.0", "end-1c"
        ).strip()

        self.clear_frame()

        self.current_frame.pack_forget()
        self.current_frame = TypingTestFrame(
            self,
            on_back=self.show_dashboard,
            on_complete=self.test_completed,
            mode=mode,
            duration=duration,
            difficulty=difficulty,
            custom_text=custom_text
        )
        self.current_frame.pack(
            fill="both", expand=True, padx=20, pady=20
        )

    def test_completed(self, result):
        self.last_result = result
        self.show_results()

    def show_results(self):
        self.clear_frame()

        self.current_frame.pack_forget()
        self.current_frame = ResultsFrame(
            self,
            on_back=self.show_dashboard,
            on_start=self.show_dashboard,
            result=self.last_result
        )
        self.current_frame.pack(
            fill="both", expand=True, padx=20, pady=20
        )


if __name__ == "__main__":
    create_tables()
    app = TypeFlowApp()
    app.mainloop()
