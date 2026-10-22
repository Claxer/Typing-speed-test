import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from statistics import get_statistics, get_recent_progress
from settings import get_daily_goal
from database import get_today_count


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.refresh()

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self,
            text="Progress Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", pady=(0, 20))

        stats = get_statistics()

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x")

        values = [
            ("Total Tests", stats["total_tests"]),
            ("Personal Best", f'{stats["best_wpm"]:.1f} WPM'),
            ("Average Speed", f'{stats["average_wpm"]:.1f} WPM'),
            ("Average Accuracy", f'{stats["average_accuracy"]:.1f}%')
        ]

        for title, value in values:
            card = ctk.CTkFrame(cards, corner_radius=12)
            card.pack(
                side="left", fill="both", expand=True,
                padx=5, pady=5
            )

            ctk.CTkLabel(
                card, text=title, text_color="gray"
            ).pack(padx=12, pady=(15, 5))

            ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(size=20, weight="bold")
            ).pack(padx=12, pady=(0, 15))

        goal = get_daily_goal()
        completed = get_today_count()

        ctk.CTkLabel(
            self,
            text=f"Today's Goal: {min(completed, goal)}/{goal} tests"
        ).pack(anchor="w", pady=(20, 5))

        progress = ctk.CTkProgressBar(self)
        progress.pack(fill="x")
        progress.set(min(completed / goal, 1))

        ctk.CTkLabel(
            self,
            text=(
                f'Total Practice: '
                f'{stats["total_practice_minutes"]:.1f} minutes'
                f'    |    Characters: {stats["total_characters"]}'
            ),
            text_color="gray"
        ).pack(anchor="w", pady=12)

        chart_data = get_recent_progress()

        figure = Figure(figsize=(7, 3), dpi=100)
        axis = figure.add_subplot(111)
        axis.set_title("Recent WPM Progress")
        axis.set_xlabel("Test")
        axis.set_ylabel("Words Per Minute")
        axis.grid(True, alpha=0.3)

        if chart_data["wpms"]:
            axis.plot(
                range(1, len(chart_data["wpms"]) + 1),
                chart_data["wpms"],
                marker="o"
            )
            axis.set_xticks(
                range(1, len(chart_data["labels"]) + 1)
            )
        else:
            axis.text(
                0.5, 0.5, "Complete a test to see your progress.",
                ha="center", va="center",
                transform=axis.transAxes
            )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure, master=self
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both", expand=True, pady=10
        )
