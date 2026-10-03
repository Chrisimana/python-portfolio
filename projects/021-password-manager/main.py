import tkinter as tk
from tkinter import messagebox
import random
import json
import os

BACKGROUND_COLOR = "#f0f4f8"
ACCENT_COLOR = "#3a6ea5"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
SYMBOLS = "!#$%&()*+-_"


# Menghasilkan password acak yang aman dengan kombinasi huruf, angka, dan simbol
class PasswordGenerator:
    def generate(self, length_letters=10, length_numbers=3, length_symbols=2):
        password_letters = [random.choice(LETTERS) for _ in range(length_letters)]
        password_numbers = [random.choice(NUMBERS) for _ in range(length_numbers)]
        password_symbols = [random.choice(SYMBOLS) for _ in range(length_symbols)]

        password_chars = password_letters + password_numbers + password_symbols
        random.shuffle(password_chars)

        return "".join(password_chars)


# Mengelola penyimpanan dan pencarian data login di dalam file JSON
class PasswordVault:
    def __init__(self, file_path):
        self.file_path = file_path

    # Membaca seluruh data dari file JSON, mengembalikan dictionary kosong jika belum ada
    def _load_data(self):
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    # Menyimpan sebuah entri baru (website, email, password) ke dalam file JSON
    def save_entry(self, website, email, password):
        data = self._load_data()
        data[website] = {"email": email, "password": password}

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    # Mencari entri berdasarkan nama website, mengembalikan None jika tidak ditemukan
    def find_entry(self, website):
        data = self._load_data()
        return data.get(website)


# Class utama yang mengatur seluruh antarmuka GUI Password Manager
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.generator = PasswordGenerator()
        self.vault = PasswordVault(DATA_FILE)

        self.root.title("Password Manager")
        self.root.configure(bg=BACKGROUND_COLOR, padx=30, pady=25)
        self.root.resizable(False, False)

        self._build_layout()

    # Membangun seluruh komponen tampilan (judul, input, tombol)
    def _build_layout(self):
        title_label = tk.Label(
            self.root,
            text="PASSWORD MANAGER",
            font=("Helvetica", 16, "bold"),
            bg=BACKGROUND_COLOR,
            fg=ACCENT_COLOR,
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        tk.Label(self.root, text="Website:", bg=BACKGROUND_COLOR).grid(row=1, column=0, sticky="e", pady=5)
        self.website_entry = tk.Entry(self.root, width=25)
        self.website_entry.grid(row=1, column=1, sticky="w", pady=5)

        search_button = tk.Button(self.root, text="Cari", command=self.search_entry)
        search_button.grid(row=1, column=2, sticky="w", padx=(5, 0))

        tk.Label(self.root, text="Email/Username:", bg=BACKGROUND_COLOR).grid(row=2, column=0, sticky="e", pady=5)
        self.email_entry = tk.Entry(self.root, width=35)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)
        self.email_entry.insert(0, "contoh@email.com")

        tk.Label(self.root, text="Password:", bg=BACKGROUND_COLOR).grid(row=3, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(self.root, width=25)
        self.password_entry.grid(row=3, column=1, sticky="w", pady=5)

        generate_button = tk.Button(self.root, text="Buat Password", command=self.generate_password)
        generate_button.grid(row=3, column=2, sticky="w", padx=(5, 0))

        add_button = tk.Button(
            self.root,
            text="Tambah & Simpan",
            width=36,
            bg=ACCENT_COLOR,
            fg="white",
            command=self.save_password,
        )
        add_button.grid(row=4, column=0, columnspan=3, pady=(15, 0))

    # Menghasilkan password acak dan mengisinya otomatis ke kolom password
    def generate_password(self):
        password = self.generator.generate()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    # Menyimpan data yang dimasukkan pengguna ke dalam vault (file JSON)
    def save_password(self):
        website = self.website_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not email or not password:
            messagebox.showwarning("Data tidak lengkap", "Mohon isi seluruh kolom sebelum menyimpan.")
            return

        is_confirmed = messagebox.askyesno(
            "Konfirmasi Penyimpanan",
            f"Detail berikut akan disimpan:\n\nWebsite: {website}\nEmail: {email}\nPassword: {password}\n\nApakah data sudah benar?",
        )

        if is_confirmed:
            self.vault.save_entry(website, email, password)
            self.website_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            messagebox.showinfo("Berhasil", f"Data untuk '{website}' berhasil disimpan.")

    # Mencari data login berdasarkan nama website yang dimasukkan
    def search_entry(self):
        website = self.website_entry.get().strip()

        if not website:
            messagebox.showwarning("Input kosong", "Mohon masukkan nama website yang ingin dicari.")
            return

        entry = self.vault.find_entry(website)

        if entry is None:
            messagebox.showinfo("Tidak ditemukan", f"Tidak ada data tersimpan untuk '{website}'.")
        else:
            messagebox.showinfo(
                website,
                f"Email: {entry['email']}\nPassword: {entry['password']}",
            )


# Titik masuk program
def main():
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()