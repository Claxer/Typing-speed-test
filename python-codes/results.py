import customtkinter as ctk
from database import get_statistics, get_history, get_recent_progress


class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent, on_back, on_start):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.on_start = on_start
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Your Progress", font=ctk.CTkFont(size=28, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=24, pady=(20, 16)
        )
        self.cards = ctk.CTkFrame(self, fg_color="transparent")
        self.cards.grid(row=1, column=0, sticky="ew", padx=18)
        self.cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_labels = []
        for index, (title, value) in enumerate([
            ("Tests Completed", "0"), ("Personal Best", "0 WPM"),
            ("Average WPM", "0 WPM"), ("Average Accuracy", "0%")
        ]):
            card = ctk.CTkFrame(self.cards, corner_radius=12)
            card.grid(row=0, column=index, sticky="ew", padx=6, pady=6)
            ctk.CTkLabel(card, text=title, text_color="gray").pack(pady=(12, 4))
            label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=21, weight="bold"))
            label.pack(pady=(0, 12))
            self.stat_labels.append(label)

        ctk.CTkLabel(self, text="Recent Test History", font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=2, column=0, sticky="w", padx=24, pady=(22, 8)
        )
        self.history_box = ctk.CTkTextbox(self, height=260, font=ctk.CTkFont(size=13))
        self.history_box.grid(row=3, column=0, sticky="nsew", padx=24, pady=(0, 14))
        self.history_box.configure(state="disabled")

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(row=4, column=0, sticky="ew", padx=24, pady=(0, 20))
        ctk.CTkButton(buttons, text="Start Typing Test", command=self.on_start).pack(side="left")
        ctk.CTkButton(buttons, text="Refresh", command=self.refresh).pack(side="left", padx=10)
        ctk.CTkButton(buttons, text="Back to Dashboard", command=self.on_back,
                      fg_color="transparent", border_width=1,
                      text_color=("gray10", "gray90")).pack(side="right")
        self.refresh()

    def refresh(self):
        stats = get_statistics()
        values = [
            str(stats["total_tests"]),
            f'{stats["personal_best"]:.1f} WPM',
            f'{stats["average_wpm"]:.1f} WPM',
            f'{stats["average_accuracy"]:.1f}%'
        ]
        for label, value in zip(self.stat_labels, values):
            label.configure(text=value)

        lines = ["DATE / TIME                 LEVEL     TIME      WPM      ACCURACY   ERRORS",
                 "-" * 76]
        history = get_history(30)
        if not history:
            lines.append("No tests saved yet. Complete a typing test to see your results here.")
        else:
            for row in history:
                _, date, difficulty, duration, wpm, accuracy, errors = row
                lines.append(f"{date:<22} {difficulty:<8} {duration:>3}s   {wpm:>6.1f}   {accuracy:>7.1f}%   {errors:>3}")
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        self.history_box.insert("1.0", "\n".join(lines))
        self.history_box.configure(state="disabled")
