import tkinter as tk

BACKGROUND_COLOR = "#1a2e35"
CARD_COLOR = "#f5f0e6"
TEXT_COLOR = "#1a2e35"
TRUE_COLOR = "#2e8b57"
FALSE_COLOR = "#b22222"

# Daftar pertanyaan trivia: setiap item berisi teks pernyataan dan jawaban
QUESTION_DATA = [
    {"text": "Python pertama kali dirilis pada tahun 1991.", "answer": True},
    {"text": "HTML adalah sebuah bahasa pemrograman.", "answer": False},
    {"text": "Matahari terbit dari arah barat.", "answer": False},
    {"text": "Great Wall of China dapat dilihat dari luar angkasa dengan mata telanjang.", "answer": False},
    {"text": "Lumba-lumba adalah mamalia, bukan ikan.", "answer": True},
    {"text": "Dalam sepak bola, satu tim terdiri dari 11 pemain di lapangan.", "answer": True},
    {"text": "Venus adalah planet terdekat dengan Matahari.", "answer": False},
    {"text": "Gunung Everest adalah gunung tertinggi di dunia.", "answer": True},
    {"text": "Bahasa Python dinamai dari ular piton.", "answer": False},
    {"text": "Satu tahun cahaya adalah satuan untuk mengukur jarak, bukan waktu.", "answer": True},
]


# Merepresentasikan satu pertanyaan kuis beserta jawabannya
class Question:
    def __init__(self, text: str, answer: bool):
        self.text = text
        self.answer = answer


# Mengelola logika utama kuis: urutan pertanyaan, skor, dan validasi jawaban
class QuizBrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list
        self.current_question = None

    # Mengecek apakah masih ada pertanyaan yang tersisa
    def still_has_questions(self) -> bool:
        return self.question_number < len(self.question_list)

    # Mengambil pertanyaan berikutnya dan menyimpannya sebagai current_question
    def next_question(self) -> Question:
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        return self.current_question

    # Memeriksa jawaban pengguna terhadap jawaban yang benar, mengembalikan True/False
    def check_answer(self, user_answer: bool) -> bool:
        correct_answer = self.current_question.answer
        is_correct = user_answer == correct_answer

        if is_correct:
            self.score += 1

        return is_correct


# Class utama yang mengatur seluruh antarmuka GUI kuis
class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.root = tk.Tk()
        self.root.title("Kuis Benar/Salah")
        self.root.configure(bg=BACKGROUND_COLOR, padx=20, pady=20)
        self.root.resizable(False, False)

        self._build_layout()
        self.get_next_question()

        self.root.mainloop()

    # Membangun seluruh komponen tampilan 
    def _build_layout(self):
        self.score_label = tk.Label(
            self.root,
            text="Skor: 0",
            font=("Helvetica", 13, "bold"),
            bg=BACKGROUND_COLOR,
            fg="white",
        )
        self.score_label.pack(pady=(0, 15))

        self.canvas = tk.Canvas(width=320, height=250, bg=CARD_COLOR, highlightthickness=0)
        self.question_text = self.canvas.create_text(
            160, 125,
            width=280,
            text="",
            font=("Helvetica", 14, "italic"),
            fill=TEXT_COLOR,
        )
        self.canvas.pack(pady=10)

        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 11, "bold"),
            bg=BACKGROUND_COLOR,
            fg="white",
        )
        self.feedback_label.pack(pady=(5, 10))

        button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        button_frame.pack()

        self.true_button = tk.Button(
            button_frame,
            text="True",
            width=10,
            height=2,
            bg=TRUE_COLOR,
            fg="white",
            font=("Helvetica", 11, "bold"),
            command=lambda: self.answer_question(True),
        )
        self.true_button.pack(side=tk.LEFT, padx=10)

        self.false_button = tk.Button(
            button_frame,
            text="False",
            width=10,
            height=2,
            bg=FALSE_COLOR,
            fg="white",
            font=("Helvetica", 11, "bold"),
            command=lambda: self.answer_question(False),
        )
        self.false_button.pack(side=tk.LEFT, padx=10)

    # Mengambil pertanyaan berikutnya dan menampilkannya di kartu, atau menampilkan hasil akhir
    def get_next_question(self):
        self.canvas.itemconfig(self.question_text, fill=TEXT_COLOR)

        if self.quiz.still_has_questions():
            question = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=question.text)
        else:
            self.canvas.itemconfig(
                self.question_text,
                text=f"Kuis selesai!\nSkor akhir Anda: {self.quiz.score}/{len(self.quiz.question_list)}",
            )
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.feedback_label.config(text="Terima kasih telah mengikuti kuis ini!")

    # Dipanggil saat pengguna menekan tombol True atau False
    def answer_question(self, user_answer: bool):
        is_correct = self.quiz.check_answer(user_answer)

        if is_correct:
            self.feedback_label.config(text="Benar!", fg="#8fd19e")
        else:
            correct_text = "True" if self.quiz.current_question.answer else "False"
            self.feedback_label.config(text=f"Salah! Jawaban yang benar: {correct_text}", fg="#e08585")

        self.score_label.config(text=f"Skor: {self.quiz.score}")
        self.root.after(1000, self.get_next_question)


# Titik masuk program
def main():
    quiz_brain = QuizBrain([Question(q["text"], q["answer"]) for q in QUESTION_DATA])
    QuizInterface(quiz_brain)


if __name__ == "__main__":
    main()