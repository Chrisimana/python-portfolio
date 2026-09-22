import random

MIN_NUMBER = 1
MAX_NUMBER = 100

DIFFICULTY_ATTEMPTS = {
    "1": ("Mudah", 10),
    "2": ("Sedang", 7),
    "3": ("Sulit", 5),
}


# Meminta pemain memilih tingkat kesulitan dan mengembalikan jumlah percobaan
def choose_difficulty():
    print("Pilih tingkat kesulitan:")
    for key, (name, attempts) in DIFFICULTY_ATTEMPTS.items():
        print(f"{key}. {name} ({attempts} percobaan)")

    while True:
        choice = input("Masukkan pilihan Anda (1-3): ").strip()
        if choice in DIFFICULTY_ATTEMPTS:
            return DIFFICULTY_ATTEMPTS[choice]
        print("Pilihan tidak valid. Mohon pilih 1, 2, atau 3.")


# Meminta pemain memasukkan tebakan yang valid dalam rentang angka yang diperbolehkan
def get_guess():
    while True:
        try:
            guess = int(input(f"Tebak angka antara {MIN_NUMBER} dan {MAX_NUMBER}: "))
            if guess < MIN_NUMBER or guess > MAX_NUMBER:
                print(f"Mohon masukkan angka antara {MIN_NUMBER} dan {MAX_NUMBER}.")
                continue
            return guess
        except ValueError:
            print("Input tidak valid. Mohon masukkan bilangan bulat.")


# Memberikan petunjuk kepada pemain berdasarkan seberapa dekat tebakannya
def give_hint(guess, target):
    if guess < target:
        print("Terlalu rendah! Coba angka yang lebih tinggi.")
    elif guess > target:
        print("Terlalu tinggi! Coba angka yang lebih rendah.")


# Loop utama permainan yang menjalankan satu ronde Tebak Angka
def main():
    print("=" * 40)
    print("          TEBAK ANGKA")
    print("=" * 40)
    print(f"Saya sedang memikirkan sebuah angka antara {MIN_NUMBER} dan {MAX_NUMBER}.")

    difficulty_name, max_attempts = choose_difficulty()
    target_number = random.randint(MIN_NUMBER, MAX_NUMBER)

    print(f"\nTingkat kesulitan: {difficulty_name}. Anda memiliki {max_attempts} percobaan.\n")

    attempts_used = 0

    while attempts_used < max_attempts:
        guess = get_guess()
        attempts_used += 1

        if guess == target_number:
            print(f"\nBenar! Anda berhasil menebak angka dalam {attempts_used} percobaan.")
            return

        give_hint(guess, target_number)
        remaining = max_attempts - attempts_used
        print(f"Sisa percobaan: {remaining}\n")

    print(f"\nPercobaan Anda habis! Angka yang benar adalah {target_number}.")


if __name__ == "__main__":
    while True:
        main()
        again = input("\nApakah Anda ingin bermain lagi? (Y/N): ").strip().lower()
        if again not in ("y", "yes"):
            print("Terima kasih telah bermain Tebak Angka. Sampai jumpa!")
            break
