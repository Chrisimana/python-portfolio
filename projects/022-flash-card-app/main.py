import tkinter as tk
import csv
import os

BACKGROUND_COLOR = "#f7f0da"
FONT_NAME = "Helvetica"
FLIP_DELAY_MS = 3000

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(DATA_DIR, "words_to_learn.csv")

# Data kosakata awal (Bahasa Prancis - Bahasa Inggris) sebagai dataset bawaan
DEFAULT_WORDS = [
    {"French": "le chat", "English": "the cat"},
    {"French": "la maison", "English": "the house"},
    {"French": "le livre", "English": "the book"},
    {"French": "l'eau", "English": "the water"},
    {"French": "le temps", "English": "the weather / time"},
    {"French": "la voiture", "English": "the car"},
    {"French": "manger", "English": "to eat"},
    {"French": "dormir", "English": "to sleep"},
    {"French": "parler", "English": "to speak"},
    {"French": "aujourd'hui", "English": "today"},
]


# Mengelola data kosakata: memuat, menyimpan progres, dan menghapus kata yang sudah dikuasai
class FlashcardData:
    def __init__(self, progress_file, default_words):
        self.progress_file = progress_file
        self.default_words = default_words
        self.words = self._load_words()

    # Memuat daftar kata dari file progres jika ada, jika tidak gunakan dataset bawaan
    def _load_words(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                loaded = list(reader)
                if loaded:
                    return loaded

        return list(self.default_words)

    # Menyimpan daftar kata yang masih tersisa (belum dikuasai) ke file CSV
    def save_progress(self):
        with open(self.progress_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["French", "English"])
            writer.writeheader()
            writer.writerows(self.words)

    # Menghapus satu kata dari daftar karena pengguna sudah menguasainya
    def remove_word(self, word_entry):
        if word_entry in self.words:
            self.words.remove(word_entry)
            self.save_progress()

    # Mengecek apakah masih ada kata yang tersisa untuk dipelajari
    def has_words(self) -> bool:
        return len(self.words) > 0


# Class utama yang mengatur seluruh antarmuka GUI kartu hafalan
class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.data = FlashcardData(PROGRESS_FILE, DEFAULT_WORDS)

        self.root.title("Flash Card App")
        self.root.configure(bg=BACKGROUND_COLOR, padx=20, pady=20)
        self.root.resizable(False, False)

        self.current_word = None
        self.flip_timer = None

        self._build_layout()
        self.next_card()

    # Membangun seluruh komponen tampilan (kartu, tombol aksi)
    def _build_layout(self):
        self.canvas = tk.Canvas(width=400, height=250, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.card_text = self.canvas.create_text(
            200, 125, text="", font=(FONT_NAME, 22, "italic"), fill="black"
        )
        self.canvas.pack(pady=(10, 15))

        button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        button_frame.pack()

        self.dont_know_button = tk.Button(
            button_frame, text="Belum Tahu", width=12, command=self.mark_dont_know
        )
        self.dont_know_button.pack(side=tk.LEFT, padx=10)

        self.know_button = tk.Button(
            button_frame, text="Sudah Tahu", width=12, command=self.mark_know
        )
        self.know_button.pack(side=tk.LEFT, padx=10)

        self.progress_label = tk.Label(
            self.root, text="", bg=BACKGROUND_COLOR, font=(FONT_NAME, 10)
        )
        self.progress_label.pack(pady=(15, 0))

    # Menampilkan sisi depan kartu (bahasa Prancis) dan menjadwalkan pembalikan otomatis
    def _show_front(self):
        self.canvas.itemconfig(self.card_text, text=self.current_word["French"], fill="black")

    # Menampilkan sisi belakang kartu (bahasa Inggris) setelah jeda waktu tertentu
    def _show_back(self):
        self.canvas.itemconfig(self.card_text, text=self.current_word["English"], fill="#3a6ea5")

    # Mengambil kata berikutnya dari daftar dan menampilkannya di kartu
    def next_card(self):
        if self.flip_timer is not None:
            self.root.after_cancel(self.flip_timer)

        if not self.data.has_words():
            self.canvas.itemconfig(self.card_text, text="Semua kata telah dikuasai!", fill="green")
            self.know_button.config(state="disabled")
            self.dont_know_button.config(state="disabled")
            self.progress_label.config(text="Selamat, hafalan Anda selesai!")
            return

        self.current_word = self.data.words[0]
        self._show_front()
        self.flip_timer = self.root.after(FLIP_DELAY_MS, self._show_back)
        self.progress_label.config(text=f"Sisa kata untuk dipelajari: {len(self.data.words)}")

    # Dipanggil saat pengguna menekan tombol "Sudah Tahu"
    def mark_know(self):
        self.data.remove_word(self.current_word)
        self.next_card()

    # Dipanggil saat pengguna menekan tombol "Belum Tahu", kata dipindah ke akhir antrean
    def mark_dont_know(self):
        word = self.data.words.pop(0)
        self.data.words.append(word)
        self.next_card()


# Titik masuk program
def main():
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()