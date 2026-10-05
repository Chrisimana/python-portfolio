import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import date, timedelta

BACKGROUND_COLOR = "#f4f1de"
ACCENT_COLOR = "#3d5a80"
DONE_COLOR = "#81b29a"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habits.json")


# Mengelola penyimpanan dan logika streak untuk setiap kebiasaan (habit)
class HabitStore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.habits = self._load_data()

    # Memuat data kebiasaan dari file JSON, mengembalikan dictionary kosong jika belum ada
    def _load_data(self):
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    # Menyimpan seluruh data kebiasaan ke file JSON
    def _save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.habits, file, indent=4)

    # Menambahkan kebiasaan baru dengan streak awal 0
    def add_habit(self, name: str):
        if name not in self.habits:
            self.habits[name] = {"streak": 0, "last_completed": None}
            self._save_data()

    # Menghapus sebuah kebiasaan dari daftar
    def remove_habit(self, name: str):
        if name in self.habits:
            del self.habits[name]
            self._save_data()

    # Menandai sebuah kebiasaan selesai dilakukan hari ini, memperbarui streak sesuai aturan
    def mark_done_today(self, name: str):
        today_str = date.today().isoformat()
        yesterday_str = (date.today() - timedelta(days=1)).isoformat()
        habit = self.habits[name]

        if habit["last_completed"] == today_str:
            return False  # sudah ditandai selesai hari ini, tidak ada perubahan

        if habit["last_completed"] == yesterday_str:
            habit["streak"] += 1
        else:
            habit["streak"] = 1

        habit["last_completed"] = today_str
        self._save_data()
        return True

    # Mengembalikan seluruh data kebiasaan beserta streak-nya
    def get_all(self):
        return self.habits


# Class utama yang mengatur seluruh antarmuka GUI Habit Tracker
class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.store = HabitStore(DATA_FILE)

        self.root.title("Habit Tracker")
        self.root.configure(bg=BACKGROUND_COLOR, padx=25, pady=20)
        self.root.resizable(False, False)

        self._build_layout()
        self.refresh_list()

    # Membangun seluruh komponen tampilan (judul, daftar kebiasaan, tombol aksi)
    def _build_layout(self):
        title_label = tk.Label(
            self.root, text="HABIT TRACKER", font=("Helvetica", 16, "bold"),
            bg=BACKGROUND_COLOR, fg=ACCENT_COLOR,
        )
        title_label.pack(pady=(0, 15))

        self.list_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.list_frame.pack(fill="both")

        button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=(15, 0))

        add_button = tk.Button(button_frame, text="Tambah Kebiasaan", command=self.add_habit)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Hapus Kebiasaan", command=self.remove_habit)
        remove_button.pack(side=tk.LEFT, padx=5)

    # Menggambar ulang daftar kebiasaan beserta streak dan tombol "Selesai Hari Ini"
    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        habits = self.store.get_all()

        if not habits:
            empty_label = tk.Label(
                self.list_frame, text="Belum ada kebiasaan. Tambahkan satu untuk mulai!",
                bg=BACKGROUND_COLOR, fg="gray",
            )
            empty_label.pack(pady=10)
            return

        for name, info in habits.items():
            row = tk.Frame(self.list_frame, bg=BACKGROUND_COLOR)
            row.pack(fill="x", pady=4)

            name_label = tk.Label(
                row, text=name, font=("Helvetica", 11), width=20, anchor="w", bg=BACKGROUND_COLOR
            )
            name_label.pack(side=tk.LEFT)

            streak_label = tk.Label(
                row, text=f"Streak: {info['streak']} hari", font=("Helvetica", 10),
                width=14, bg=BACKGROUND_COLOR, fg=ACCENT_COLOR,
            )
            streak_label.pack(side=tk.LEFT)

            is_done_today = info["last_completed"] == date.today().isoformat()
            done_button = tk.Button(
                row,
                text="Sudah Selesai" if is_done_today else "Tandai Selesai",
                bg=DONE_COLOR if is_done_today else "SystemButtonFace",
                state="disabled" if is_done_today else "normal",
                command=lambda n=name: self.mark_done(n),
            )
            done_button.pack(side=tk.LEFT, padx=5)

    # Dipanggil saat tombol "Tambah Kebiasaan" ditekan
    def add_habit(self):
        name = simpledialog.askstring("Kebiasaan Baru", "Nama kebiasaan yang ingin dilacak:")
        if name:
            name = name.strip()
            if name:
                self.store.add_habit(name)
                self.refresh_list()

    # Dipanggil saat tombol "Hapus Kebiasaan" ditekan
    def remove_habit(self):
        habits = list(self.store.get_all().keys())
        if not habits:
            messagebox.showinfo("Tidak ada data", "Belum ada kebiasaan untuk dihapus.")
            return

        name = simpledialog.askstring(
            "Hapus Kebiasaan", f"Ketik nama kebiasaan yang ingin dihapus:\n{', '.join(habits)}"
        )
        if name and name.strip() in habits:
            self.store.remove_habit(name.strip())
            self.refresh_list()
        elif name:
            messagebox.showwarning("Tidak ditemukan", f"Kebiasaan '{name}' tidak ditemukan.")

    # Dipanggil saat tombol "Tandai Selesai" pada salah satu kebiasaan ditekan
    def mark_done(self, name):
        self.store.mark_done_today(name)
        self.refresh_list()


def main():
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()