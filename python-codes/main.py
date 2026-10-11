
import customtkinter as ctk
from tkinter import messagebox

from database import create_tables, save_result
from typing_test import TypingTestFrame
from results import ResultsFrame


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TypingSpeedTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        create_tables()

        self.title("Typing Speed Test")
        self.geometry("1150x750")
        self.minsize(950, 650)
        self.configure(fg_color="#111111")

        self.current_page = None
        self.latest_result = None

        self.build_layout()
        self.show_dashboard()

    def build_layout(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#181818"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="TYPEFLOW",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=22, pady=(30, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="Typing Speed Test",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=22, pady=(0, 35))

        self.add_nav_button("Dashboard", self.show_dashboard)
        self.add_nav_button("Typing Test", self.show_typing_test)
        self.add_nav_button("Results & History", self.show_results)

        ctk.CTkLabel(
            self.sidebar,
            text="Python Desktop Project\nVersion 1.0",
            text_color="gray",
            font=ctk.CTkFont(size=11),
            justify="left"
        ).pack(side="bottom", anchor="w", padx=22, pady=25)

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#111111"
        )
        self.content.pack(side="left", fill="both", expand=True)

    def add_nav_button(self, text, command):
        ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            anchor="w",
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#292929",
            text_color="#E5E7EB",
            font=ctk.CTkFont(size=14)
        ).pack(fill="x", padx=12, pady=4)

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()
            self.current_page = None

    def show_dashboard(self):
        self.clear_page()

        self.current_page = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        self.current_page.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.current_page,
            text="Welcome to TypeFlow",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(anchor="w", padx=35, pady=(40, 8))

        ctk.CTkLabel(
            self.current_page,
            text="Improve your typing speed, accuracy, and consistency.",
            text_color="gray",
            font=ctk.CTkFont(size=15)
        ).pack(anchor="w", padx=35, pady=(0, 25))

        hero = ctk.CTkFrame(
            self.current_page,
            fg_color="#1D2939",
            corner_radius=16
        )
        hero.pack(fill="x", padx=35, pady=10)

        ctk.CTkLabel(
            hero,
            text="Practice makes progress.",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#93C5FD"
        ).pack(anchor="w", padx=25, pady=(25, 8))

        ctk.CTkLabel(
            hero,
            text=(
                "Take a timed typing test and discover your words per "
                "minute, accuracy, and mistakes. Your results are saved locally."
            ),
            font=ctk.CTkFont(size=14),
            wraplength=650,
            justify="left"
        ).pack(anchor="w", padx=25, pady=(0, 20))

        ctk.CTkButton(
            hero,
            text="Start Typing Test",
            command=self.show_typing_test,
            width=180,
            height=42
        ).pack(anchor="w", padx=25, pady=(0, 25))

        features = ctk.CTkFrame(
            self.current_page,
            fg_color="transparent"
        )
        features.pack(fill="x", padx=30, pady=20)

        self.create_feature_card(
            features, "01", "Typing Speed",
            "Measure your typing speed in WPM."
        )
        self.create_feature_card(
            features, "02", "Accuracy",
            "Track correct and incorrect characters."
        )
        self.create_feature_card(
            features, "03", "Progress",
            "Review your saved results and best score."
        )

        ctk.CTkLabel(
            self.current_page,
            text="Choose a section from the sidebar to get started.",
            text_color="gray"
        ).pack(anchor="w", padx=35, pady=10)

    def create_feature_card(self, parent, number, title, description):
        card = ctk.CTkFrame(
            parent,
            fg_color="#202020",
            corner_radius=12
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            card,
            text=number,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(anchor="w", padx=15, pady=4)

        ctk.CTkLabel(
            card,
            text=description,
            text_color="gray",
            wraplength=180,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 18))

    def show_typing_test(self):
        self.clear_page()

        self.current_page = TypingTestFrame(
            self.content,
            on_complete=self.handle_test_complete,
            on_back=self.show_dashboard
        )

    def handle_test_complete(self, result):
        self.latest_result = result

        try:
            save_result(
                result["wpm"],
                result["accuracy"],
                result["mistakes"],
                result["difficulty"],
                result["duration"]
            )
        except Exception as error:
            messagebox.showerror(
                "Save Error",
                f"The test finished, but the result could not be saved.\n\n{error}"
            )

        self.show_results()

    def show_results(self):
        self.clear_page()

        self.current_page = ResultsFrame(
            self.content,
            on_back=self.show_dashboard,
            on_start=self.show_typing_test
        )

        if self.latest_result is not None:
            self.current_page.set_latest_result(self.latest_result)


if __name__ == "__main__":
    app = TypingSpeedTestApp()
    app.mainloop()
