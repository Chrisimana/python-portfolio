import random

# Daftar kata yang bisa dipilih secara acak untuk permainan
WORD_LIST = [
    "python", "developer", "keyboard", "algorithm", "function",
    "variable", "computer", "internet", "software", "terminal",
]

MAX_ATTEMPTS = 6

HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    """,
]


# Memilih satu kata secara acak dari daftar kata
def choose_word():
    return random.choice(WORD_LIST)


# Membangun tampilan kata, menunjukkan huruf yang sudah ditebak dan sisanya berupa garis bawah
def get_display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


# Menampilkan tahap gantungan saat ini berdasarkan jumlah tebakan salah
def print_hangman(wrong_guesses):
    print(HANGMAN_STAGES[wrong_guesses])


# Meminta pemain memasukkan satu huruf valid yang belum pernah ditebak
def get_guess(guessed_letters):
    while True:
        guess = input("Tebak sebuah huruf: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Mohon masukkan satu huruf saja.")
        elif guess in guessed_letters:
            print("Anda sudah menebak huruf itu. Coba huruf lain.")
        else:
            return guess


# Loop utama permainan yang menjalankan satu ronde Hangman
def main():
    word = choose_word()
    guessed_letters = set()
    wrong_guesses = 0

    print("=" * 40)
    print("              HANGMAN")
    print("=" * 40)
    print(f"Kata memiliki {len(word)} huruf. Anda memiliki {MAX_ATTEMPTS} kesempatan salah tebak.")

    while wrong_guesses < MAX_ATTEMPTS:
        print_hangman(wrong_guesses)
        print(f"Kata: {get_display_word(word, guessed_letters)}")
        print(f"Huruf yang sudah ditebak: {', '.join(sorted(guessed_letters)) or 'Belum ada'}")
        print(f"Tebakan salah: {wrong_guesses}/{MAX_ATTEMPTS}")

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in word:
            print("Tebakan benar!")
        else:
            wrong_guesses += 1
            print("Tebakan salah!")

        if all(letter in guessed_letters for letter in word):
            print(f"\nSelamat! Anda berhasil menebak kata: {word}")
            return

    print_hangman(wrong_guesses)
    print(f"\nKesempatan Anda habis! Kata yang benar adalah: {word}")


if __name__ == "__main__":
    while True:
        main()
        again = input("\nApakah Anda ingin bermain lagi? (Y/N): ").strip().lower()
        if again not in ("y", "yes"):
            print("Terima kasih telah bermain Hangman. Sampai jumpa!")
            break
