import customtkinter as ctk
from tkinter import messagebox

from database import init_db, get_results, delete_result
from typing_test import TypingTestFrame
from dashboard import DashboardFrame
from achievements import get_achievements
from settings import get_daily_goal, update_daily_goal
from export import export_results


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TypeFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        init_db()

        self.title("TypeFlow - Typing Speed Test")
        self.geometry("1100x750")
        self.minsize(900, 650)

        self.sidebar = ctk.CTkFrame(
            self, width=200, corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(
            self, corner_radius=0
        )
        self.content.pack(
            side="right", fill="both", expand=True
        )

        ctk.CTkLabel(
            self.sidebar,
            text="TypeFlow",
            font=ctk.CTkFont(size=27, weight="bold")
        ).pack(padx=20, pady=(30, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="Typing Speed Test",
            text_color="gray"
        ).pack(pady=(0, 25))

        pages = [
            ("Dashboard", self.show_dashboard),
            ("Typing Test", self.show_typing_test),
            ("History", self.show_history),
            ("Achievements", self.show_achievements),
            ("Settings", self.show_settings)
        ]

        for label, command in pages:
            ctk.CTkButton(
                self.sidebar,
                text=label,
                command=command,
                height=40
            ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Export CSV",
            command=export_results,
            height=40
        ).pack(fill="x", padx=15, pady=(25, 5))

        ctk.CTkButton(
            self.sidebar,
            text="Exit",
            command=self.confirm_exit,
            fg_color="#8B3030",
            hover_color="#6E2424"
        ).pack(side="bottom", fill="x", padx=15, pady=20)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        DashboardFrame(self.content)

    def show_typing_test(self):
        self.clear_content()

        TypingTestFrame(
            self.content,
            on_complete=self.refresh_after_test
        ).pack(fill="both", expand=True, padx=20, pady=20)

    def refresh_after_test(self):
        # Refresh the dashboard when a test finishes.
        for widget in self.content.winfo_children():
            if isinstance(widget, DashboardFrame):
                widget.refresh()

    def show_history(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Typing History",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        search_row = ctk.CTkFrame(
            self.content, fg_color="transparent"
        )
        search_row.pack(fill="x", padx=20, pady=10)

        search_entry = ctk.CTkEntry(
            search_row,
            placeholder_text="Search date or difficulty..."
        )
        search_entry.pack(side="left", fill="x", expand=True)

        table = ctk.CTkTextbox(
            self.content, font=("Consolas", 13)
        )
        table.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        def refresh_history():
            table.configure(state="normal")
            table.delete("1.0", "end")

            rows = get_results(search_entry.get())

            table.insert(
                "end",
                "ID | DATE       | MODE   | WPM  | ACCURACY | ERRORS | SECONDS\n"
            )
            table.insert("end", "-" * 75 + "\n")

            for row in rows:
                table.insert(
                    "end",
                    f'{row["id"]:>2} | '
                    f'{row["created_at"]} | '
                    f'{row["difficulty"]:<6} | '
                    f'{row["wpm"]:>5.1f} | '
                    f'{row["accuracy"]:>7.1f}% | '
                    f'{row["mistakes"]:>6} | '
                    f'{row["duration"]:>7}\n'
                )

            if not rows:
                table.insert("end", "\nNo results found.")

            table.configure(state="disabled")

        def delete_selected():
            selection = table.get("sel.first", "sel.last").strip()

            if not selection:
                messagebox.showinfo(
                    "Delete Result",
                    "Highlight a result line first."
                )
                return

            try:
                result_id = int(selection.split("|")[0].strip())
            except (ValueError, IndexError):
                messagebox.showwarning(
                    "Delete Result",
                    "Select a valid result line."
                )
                return

            if messagebox.askyesno(
                "Confirm Delete",
                f"Delete typing result #{result_id}?"
            ):
                delete_result(result_id)
                refresh_history()

        ctk.CTkButton(
            search_row,
            text="Search",
            command=refresh_history,
            width=100
        ).pack(side="left", padx=8)

        buttons = ctk.CTkFrame(
            self.content, fg_color="transparent"
        )
        buttons.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkButton(
            buttons,
            text="Show All",
            command=lambda: (
                search_entry.delete(0, "end"),
                refresh_history()
            )
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            buttons,
            text="Delete Selected",
            command=delete_selected,
            fg_color="#8B3030",
            hover_color="#6E2424"
        ).pack(side="left")

        refresh_history()

    def show_achievements(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Achievements",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", padx=20, pady=20)

        achievements = get_achievements()
        unlocked = sum(
            item["unlocked"] for item in achievements
        )

        ctk.CTkLabel(
            self.content,
            text=f"Unlocked: {unlocked}/{len(achievements)}"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        for item in achievements:
            status = "UNLOCKED" if item["unlocked"] else "LOCKED"

            card = ctk.CTkFrame(
                self.content, corner_radius=10
            )
            card.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                card,
                text=f'{status}  |  {item["name"]}',
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=15, pady=(10, 2))

            ctk.CTkLabel(
                card,
                text=item["description"],
                text_color="gray"
            ).pack(anchor="w", padx=15, pady=(0, 10))

    def show_settings(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Settings",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", padx=20, pady=20)

        ctk.CTkLabel(
            self.content,
            text="Daily Practice Goal",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            self.content,
            text="Choose how many typing tests you want to complete each day.",
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=5)

        goal_entry = ctk.CTkEntry(
            self.content, width=200
        )
        goal_entry.pack(anchor="w", padx=20, pady=10)
        goal_entry.insert(0, str(get_daily_goal()))

        def save_goal():
            try:
                goal = update_daily_goal(goal_entry.get())
                messagebox.showinfo(
                    "Settings Saved",
                    f"Your daily goal is now {goal} tests."
                )
            except ValueError:
                messagebox.showerror(
                    "Invalid Goal",
                    "Enter a whole number from 1 to 100."
                )

        ctk.CTkButton(
            self.content,
            text="Save Goal",
            command=save_goal
        ).pack(anchor="w", padx=20, pady=5)

        ctk.CTkLabel(
            self.content,
            text="Your test history and settings are stored locally.",
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=20)

    def confirm_exit(self):
        if messagebox.askyesno(
            "Exit TypeFlow",
            "Are you sure you want to exit?"
        ):
            self.destroy()


if __name__ == "__main__":
    app = TypeFlowApp()
    app.mainloop()
