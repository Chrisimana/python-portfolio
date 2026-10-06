MORSE_CODE_DICT = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
    "!": "-.-.--", "/": "-..-.", "(": "-.--.", ")": "-.--.-",
    "&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.", "-": "-....-", "_": "..--.-", '"': ".-..-.",
    "$": "...-..-", "@": ".--.-.",
}

MORSE_TO_TEXT_DICT = {morse: letter for letter, morse in MORSE_CODE_DICT.items()}


# Mengubah teks biasa menjadi kode Morse, setiap huruf dipisah spasi dan kata dipisah " / "
def text_to_morse(text: str) -> str:
    words = text.upper().split(" ")
    morse_words = []

    for word in words:
        morse_letters = []
        for char in word:
            if char in MORSE_CODE_DICT:
                morse_letters.append(MORSE_CODE_DICT[char])
        morse_words.append(" ".join(morse_letters))

    return " / ".join(morse_words)


# Mengubah kode Morse kembali menjadi teks biasa
def morse_to_text(morse: str) -> str:
    morse_words = morse.strip().split(" / ")
    text_words = []

    for morse_word in morse_words:
        letters = morse_word.strip().split(" ")
        text_letters = [MORSE_TO_TEXT_DICT.get(letter, "") for letter in letters if letter]
        text_words.append("".join(text_letters))

    return " ".join(text_words)


def print_menu():
    print("\n" + "=" * 40)
    print("      TEXT TO MORSE CODE CONVERTER")
    print("=" * 40)
    print("1. Teks ke Kode Morse")
    print("2. Kode Morse ke Teks")
    print("3. Keluar")


def main():
    while True:
        print_menu()
        choice = input("Pilih opsi (1-3): ").strip()

        if choice == "1":
            text = input("Masukkan teks: ")
            result = text_to_morse(text)
            print(f"\nKode Morse: {result}")

        elif choice == "2":
            print("Masukkan kode Morse (pisahkan huruf dengan spasi, kata dengan ' / '):")
            morse = input("> ")
            result = morse_to_text(morse)
            print(f"\nTeks: {result}")

        elif choice == "3":
            print("\nSampai jumpa!")
            break

        else:
            print("Opsi tidak valid. Mohon pilih antara 1 dan 3.")


if __name__ == "__main__":
    main()