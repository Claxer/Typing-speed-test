import customtkinter as ctk
from tkinter import messagebox
from database import create_tables, save_result, get_statistics
from typing_test import TypingTestFrame
from results import ResultsFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TypingSpeedApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Test")
        self.geometry("1100x760")
        self.minsize(900, 650)
        self.configure(fg_color="#101114")
        create_tables()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#17181c")
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="TYPEFLOW", font=ctk.CTkFont(size=23, weight="bold")
        ).pack(anchor="w", padx=22, pady=(28, 4))
        ctk.CTkLabel(
            self.sidebar, text="Typing practice", text_color="gray"
        ).pack(anchor="w", padx=22, pady=(0, 30))

        self.content = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self.pages["dashboard"] = self.build_dashboard()
        self.pages["test"] = TypingTestFrame(self.content, self.complete_test, lambda: self.show_page("dashboard"))
        self.pages["results"] = ResultsFrame(self.content, lambda: self.show_page("dashboard"),
                                               lambda: self.show_page("test"))
        self.pages["settings"] = self.build_settings()

        for name, label in [
            ("dashboard", "Dashboard"),
            ("test", "Typing Test"),
            ("results", "Results & History"),
            ("settings", "Settings")
        ]:
            ctk.CTkButton(
                self.sidebar, text=label, anchor="w", height=42,
                fg_color="transparent", hover_color="#292b31",
                command=lambda page=name: self.show_page(page)
            ).pack(fill="x", padx=12, pady=4)

        ctk.CTkLabel(
            self.sidebar, text="VERSION 2.0", text_color="gray"
        ).pack(side="bottom", anchor="w", padx=22, pady=20)

        self.show_page("dashboard")

    def build_dashboard(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(page, text="Dashboard", font=ctk.CTkFont(size=30, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 4)
        )
        ctk.CTkLabel(page, text="Build speed through consistent, accurate practice.",
                     text_color="gray").grid(row=1, column=0, sticky="w", padx=28, pady=(0, 22))

        stats_frame = ctk.CTkFrame(page, fg_color="transparent")
        stats_frame.grid(row=2, column=0, sticky="ew", padx=20)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.dashboard_stats = []
        for col, (title, value) in enumerate([
            ("Tests Completed", "0"), ("Personal Best", "0 WPM"), ("Average WPM", "0 WPM")
        ]):
            card = ctk.CTkFrame(stats_frame, corner_radius=12)
            card.grid(row=0, column=col, sticky="ew", padx=8, pady=4)
            ctk.CTkLabel(card, text=title, text_color="gray").pack(pady=(16, 5))
            label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=25, weight="bold"))
            label.pack(pady=(0, 16))
            self.dashboard_stats.append(label)

        welcome = ctk.CTkFrame(page, corner_radius=14)
        welcome.grid(row=3, column=0, sticky="ew", padx=28, pady=24)
        ctk.CTkLabel(welcome, text="Ready for a new personal best?",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(
            welcome, text="Choose a difficulty and test duration. Your results will be saved automatically.",
            text_color="gray", wraplength=650, justify="left"
        ).pack(anchor="w", padx=24, pady=(0, 20))
        ctk.CTkButton(welcome, text="Start Typing Test", height=42,
                      command=lambda: self.show_page("test")).pack(anchor="w", padx=24, pady=(0, 24))

        tip = ctk.CTkFrame(page, corner_radius=12, fg_color="#1b1d22")
        tip.grid(row=4, column=0, sticky="ew", padx=28, pady=(0, 20))
        ctk.CTkLabel(tip, text="PRACTICE TIP", text_color="#76a9fa",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(16, 5))
        ctk.CTkLabel(tip, text="Prioritize accuracy. Speed usually improves as correct typing becomes a habit.",
                     wraplength=650, justify="left").pack(anchor="w", padx=20, pady=(0, 16))
        return page

    def build_settings(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(page, text="Settings", font=ctk.CTkFont(size=30, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=28, pady=(28, 12)
        )
        appearance_card = ctk.CTkFrame(page, corner_radius=12)
        appearance_card.grid(row=1, column=0, sticky="ew", padx=28, pady=8)
        ctk.CTkLabel(appearance_card, text="Appearance", font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=20, pady=(18, 8)
        )
        ctk.CTkLabel(appearance_card, text="Choose how the application looks.", text_color="gray").pack(
            anchor="w", padx=20, pady=(0, 10)
        )
        self.appearance_menu = ctk.CTkOptionMenu(
            appearance_card, values=["Dark", "Light", "System"], command=self.change_appearance
        )
        self.appearance_menu.set("Dark")
        self.appearance_menu.pack(anchor="w", padx=20, pady=(0, 18))

        info = ctk.CTkFrame(page, corner_radius=12)
        info.grid(row=2, column=0, sticky="ew", padx=28, pady=8)
        ctk.CTkLabel(info, text="About TypeFlow", font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=20, pady=(18, 8)
        )
        ctk.CTkLabel(
            info, text="A local typing practice application built with Python, CustomTkinter, and SQLite.\n"
                       "Your typing results are stored on this computer.",
            text_color="gray", justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 18))
        return page

    def change_appearance(self, value):
        ctk.set_appearance_mode(value.lower())

    def refresh_dashboard(self):
        stats = get_statistics()
        values = [
            str(stats["total_tests"]),
            f'{stats["personal_best"]:.1f} WPM',
            f'{stats["average_wpm"]:.1f} WPM'
        ]
        for label, value in zip(self.dashboard_stats, values):
            label.configure(text=value)

    def show_page(self, page_name):
        for page in self.pages.values():
            page.grid_forget()
        page = self.pages[page_name]
        page.grid(row=0, column=0, sticky="nsew")
        if page_name == "dashboard":
            self.refresh_dashboard()
        elif page_name == "results":
            page.refresh()
        elif page_name == "test":
            page.reset_test()

    def complete_test(self, result):
        try:
            save_result(result)
            self.pages["results"].refresh()
            self.show_page("results")
        except Exception as error:
            messagebox.showerror("Save Error", f"Could not save your result.\n\n{error}")
            self.show_page("dashboard")


if __name__ == "__main__":
    app = TypingSpeedApp()
    app.mainloop()
