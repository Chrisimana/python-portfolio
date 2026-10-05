import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import date

BACKGROUND_COLOR = "#1d3557"
ACCENT_COLOR = "#e63946"
TEXT_COLOR = "#f1faee"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workouts.csv")


# Mengelola penyimpanan dan pembacaan data latihan (workout) dari file CSV
class WorkoutStore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.fieldnames = ["date", "exercise", "sets", "reps", "weight"]

    # Menambahkan satu entri latihan baru ke file CSV
    def add_workout(self, exercise, sets, reps, weight):
        file_exists = os.path.exists(self.file_path)

        with open(self.file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "date": date.today().isoformat(),
                "exercise": exercise,
                "sets": sets,
                "reps": reps,
                "weight": weight,
            })

    # Mengambil seluruh riwayat latihan yang tersimpan, urutan terbaru di atas
    def get_all_workouts(self):
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            records = list(reader)

        return list(reversed(records))

    # Menghapus seluruh riwayat latihan yang tersimpan
    def clear_all(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


# Class utama yang mengatur seluruh antarmuka GUI Workout Tracker
class WorkoutTrackerApp:
    def __init__(self, root):
        self.root = root
        self.store = WorkoutStore(DATA_FILE)

        self.root.title("Workout Tracker")
        self.root.configure(bg=BACKGROUND_COLOR, padx=25, pady=20)
        self.root.resizable(False, False)

        self._build_layout()
        self.refresh_table()

    # Membangun seluruh komponen tampilan (judul, form input, tabel riwayat)
    def _build_layout(self):
        title_label = tk.Label(
            self.root, text="WORKOUT TRACKER", font=("Helvetica", 16, "bold"),
            bg=BACKGROUND_COLOR, fg=ACCENT_COLOR,
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15))

        tk.Label(self.root, text="Latihan:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, sticky="e", pady=4)
        self.exercise_entry = tk.Entry(self.root, width=20)
        self.exercise_entry.grid(row=1, column=1, pady=4, padx=5)

        tk.Label(self.root, text="Set:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=2, sticky="e", pady=4)
        self.sets_entry = tk.Entry(self.root, width=6)
        self.sets_entry.grid(row=1, column=3, pady=4, padx=5)

        tk.Label(self.root, text="Repetisi:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, sticky="e", pady=4)
        self.reps_entry = tk.Entry(self.root, width=20)
        self.reps_entry.grid(row=2, column=1, pady=4, padx=5)

        tk.Label(self.root, text="Beban (kg):", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=2, sticky="e", pady=4)
        self.weight_entry = tk.Entry(self.root, width=6)
        self.weight_entry.grid(row=2, column=3, pady=4, padx=5)

        add_button = tk.Button(self.root, text="Tambah Latihan", bg=ACCENT_COLOR, fg="white", command=self.add_workout)
        add_button.grid(row=3, column=0, columnspan=2, pady=(10, 15), sticky="we")

        clear_button = tk.Button(self.root, text="Hapus Semua Riwayat", command=self.clear_history)
        clear_button.grid(row=3, column=2, columnspan=2, pady=(10, 15), sticky="we")

        columns = ("date", "exercise", "sets", "reps", "weight")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

        headings = {
            "date": "Tanggal", "exercise": "Latihan", "sets": "Set",
            "reps": "Repetisi", "weight": "Beban (kg)",
        }
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=110, anchor="center")

        self.table.grid(row=4, column=0, columnspan=4, pady=(0, 5))

    # Menggambar ulang seluruh baris tabel riwayat latihan dari data terbaru
    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for record in self.store.get_all_workouts():
            self.table.insert("", tk.END, values=(
                record["date"], record["exercise"], record["sets"],
                record["reps"], record["weight"],
            ))

    # Dipanggil saat tombol "Tambah Latihan" ditekan
    def add_workout(self):
        exercise = self.exercise_entry.get().strip()
        sets = self.sets_entry.get().strip()
        reps = self.reps_entry.get().strip()
        weight = self.weight_entry.get().strip()

        if not exercise or not sets or not reps or not weight:
            messagebox.showwarning("Data tidak lengkap", "Mohon isi seluruh kolom sebelum menambahkan.")
            return

        if not (sets.isdigit() and reps.isdigit()):
            messagebox.showwarning("Input tidak valid", "Set dan Repetisi harus berupa angka bulat.")
            return

        try:
            float(weight)
        except ValueError:
            messagebox.showwarning("Input tidak valid", "Beban harus berupa angka.")
            return

        self.store.add_workout(exercise, sets, reps, weight)

        self.exercise_entry.delete(0, tk.END)
        self.sets_entry.delete(0, tk.END)
        self.reps_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)

        self.refresh_table()

    # Dipanggil saat tombol "Hapus Semua Riwayat" ditekan
    def clear_history(self):
        is_confirmed = messagebox.askyesno("Konfirmasi", "Hapus seluruh riwayat latihan? Tindakan ini tidak dapat dibatalkan.")
        if is_confirmed:
            self.store.clear_all()
            self.refresh_table()


def main():
    root = tk.Tk()
    app = WorkoutTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()