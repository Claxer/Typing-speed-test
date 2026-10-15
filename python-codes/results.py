
import customtkinter as ctk

from database import (
    get_history,
    get_personal_best,
    get_total_tests,
    get_average_wpm,
    get_average_accuracy,
    get_total_mistakes,
    get_recent_average_wpm
)


class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent, on_back, on_start, result=None):
        super().__init__(parent, fg_color="transparent")

        self.on_back = on_back
        self.on_start = on_start
        self.result = result

        ctk.CTkLabel(
            self,
            text="Your Progress",
            font=("Arial", 28, "bold")
        ).pack(pady=15)

        self.show_summary()
        self.show_recent_history()

        ctk.CTkButton(
            self,
            text="Start Typing Test",
            command=self.on_start
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Back to Dashboard",
            command=self.on_back,
            fg_color="gray"
        ).pack(pady=5)

    def show_summary(self):
        container = ctk.CTkFrame(self)
        container.pack(fill="x", padx=15, pady=10)

        statistics = [
            ("Personal Best", f"{get_personal_best():.1f} WPM"),
            ("Total Tests", str(get_total_tests())),
            ("Average WPM", f"{get_average_wpm():.1f}"),
            ("Average Accuracy", f"{get_average_accuracy():.1f}%"),
            ("Total Mistakes", str(get_total_mistakes())),
            ("Recent Average", f"{get_recent_average_wpm():.1f} WPM")
        ]

        for index, (label, value) in enumerate(statistics):
            card = ctk.CTkFrame(container)
            card.grid(
                row=index // 3,
                column=index % 3,
                padx=6,
                pady=6,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=label,
                font=("Arial", 12)
            ).pack(padx=12, pady=(12, 3))

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 20, "bold")
            ).pack(padx=12, pady=(3, 12))

        for column in range(3):
            container.grid_columnconfigure(
                column, weight=1
            )

    def show_recent_history(self):
        ctk.CTkLabel(
            self,
            text="Recent Tests",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        history_box = ctk.CTkTextbox(
            self,
            height=220,
            font=("Consolas", 12)
        )
        history_box.pack(
            fill="both", expand=True, padx=15, pady=5
        )

        history = get_history(limit=10)

        if not history:
            history_box.insert(
                "end", "No tests completed yet.\n"
            )
        else:
            for item in history:
                history_box.insert(
                    "end",
                    f"Date: {item['date']}\n"
                    f"Mode: {item['mode']} | "
                    f"Difficulty: {item['difficulty']}\n"
                    f"WPM: {item['wpm']:.1f} | "
                    f"Accuracy: {item['accuracy']:.1f}% | "
                    f"Mistakes: {item['mistakes']}\n"
                    f"{'-' * 55}\n"
                )

        history_box.configure(state="disabled")
