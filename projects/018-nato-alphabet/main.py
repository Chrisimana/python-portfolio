import tkinter as tk
from tkinter import messagebox

BACKGROUND_COLOR = "#0d1b2a"
ACCENT_COLOR = "#e0a458"
TEXT_COLOR = "#f1f1f1"
OUTPUT_BG = "#1b263b"


# Menyimpan data alfabet fonetik NATO dan menangani logika konversi kata
class NatoConverter:
    def __init__(self):
        self.nato_alphabet = {
            "A": "Alfa", "B": "Bravo", "C": "Charlie", "D": "Delta",
            "E": "Echo", "F": "Foxtrot", "G": "Golf", "H": "Hotel",
            "I": "India", "J": "Juliett", "K": "Kilo", "L": "Lima",
            "M": "Mike", "N": "November", "O": "Oscar", "P": "Papa",
            "Q": "Quebec", "R": "Romeo", "S": "Sierra", "T": "Tango",
            "U": "Uniform", "V": "Victor", "W": "Whiskey", "X": "Xray",
            "Y": "Yankee", "Z": "Zulu",
        }

    # Mengubah sebuah kata menjadi pasangan
    def convert_word(self, word: str):
        phonetic_pairs = []
        invalid_chars = []

        for char in word:
            if char.isalpha():
                phonetic_pairs.append((char.upper(), self.nato_alphabet[char.upper()]))
            elif not char.isspace():
                invalid_chars.append(char)

        return phonetic_pairs, invalid_chars


# Class utama yang mengatur seluruh antarmuka GUI
class NatoApp:
    def __init__(self, root):
        self.root = root
        self.converter = NatoConverter()

        self.root.title("NATO Alphabet Converter")
        self.root.configure(bg=BACKGROUND_COLOR, padx=25, pady=20)
        self.root.resizable(False, False)

        self._build_layout()

    # Membangun seluruh komponen tampilan
    def _build_layout(self):
        title_label = tk.Label(
            self.root,
            text="NATO ALPHABET CONVERTER",
            font=("Helvetica", 16, "bold"),
            bg=BACKGROUND_COLOR,
            fg=ACCENT_COLOR,
        )
        title_label.pack(pady=(0, 15))

        instruction_label = tk.Label(
            self.root,
            text="Masukkan sebuah kata untuk diubah menjadi kode fonetik NATO:",
            font=("Helvetica", 10),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )
        instruction_label.pack()

        self.word_entry = tk.Entry(self.root, width=35, font=("Helvetica", 12))
        self.word_entry.pack(pady=10)
        self.word_entry.bind("<Return>", lambda event: self.handle_convert())

        convert_button = tk.Button(
            self.root,
            text="Konversi",
            font=("Helvetica", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=BACKGROUND_COLOR,
            command=self.handle_convert,
        )
        convert_button.pack(pady=(0, 15))

        self.output_text = tk.Text(
            self.root,
            width=45,
            height=10,
            font=("Courier", 11),
            bg=OUTPUT_BG,
            fg=TEXT_COLOR,
            wrap="word",
            state="disabled",
        )
        self.output_text.pack()

    # Menampilkan teks hasil konversi ke dalam kotak output
    def _display_output(self, text: str):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state="disabled")

    # Dipanggil saat pengguna menekan tombol Konversi atau tombol Enter
    def handle_convert(self):
        word = self.word_entry.get().strip()

        if not word:
            messagebox.showwarning("Input kosong", "Mohon masukkan sebuah kata terlebih dahulu.")
            return

        phonetic_pairs, invalid_chars = self.converter.convert_word(word)
        output_lines = [f"{char} -> {code}" for char, code in phonetic_pairs]

        output_text = "\n".join(output_lines)

        if invalid_chars:
            output_text += f"\n\nKarakter diabaikan (bukan huruf): {', '.join(invalid_chars)}"

        self._display_output(output_text)


# Titik masuk program
def main():
    root = tk.Tk()
    app = NatoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()