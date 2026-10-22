import csv
from pathlib import Path
from tkinter import filedialog, messagebox

from database import get_results


def export_results():
    results = get_results()

    if not results:
        messagebox.showinfo(
            "Export Results",
            "There are no typing results to export."
        )
        return

    path = filedialog.asksaveasfilename(
        title="Export Typing History",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="typeflow_history.csv"
    )

    if not path:
        return

    columns = [
        "id", "wpm", "accuracy", "mistakes",
        "duration", "difficulty", "characters",
        "created_at"
    ]

    try:
        with Path(path).open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=columns
            )
            writer.writeheader()
            writer.writerows(results)

        messagebox.showinfo(
            "Export Complete",
            f"Your typing history was exported to:\n{path}"
        )

    except OSError as error:
        messagebox.showerror(
            "Export Failed",
            f"Could not save the file:\n{error}"
        )
