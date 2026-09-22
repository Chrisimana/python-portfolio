import random
import string

# Membangun kumpulan karakter untuk dipilih berdasarkan preferensi pengguna
def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    pool = ""

    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    return pool

# Menghasilkan password acak dengan panjang tertentu dari kumpulan karakter
def generate_password(length, pool):
    return "".join(random.choice(pool) for _ in range(length))

# Menanyakan pertanyaan ya/tidak dan mengembalikan True atau False
def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            print("Mohon jawab dengan Y atau N.")

# Meminta pengguna memasukkan panjang password yang valid
def get_password_length():
    while True:
        try:
            length = int(input("Masukkan panjang password (minimal 4): "))
            if length < 4:
                print("Panjang password minimal harus 4.")
                continue
            return length
        except ValueError:
            print("Input tidak valid. Mohon masukkan bilangan bulat.")

# Menilai kekuatan password berdasarkan panjang dan variasi karakter
def rate_strength(length, use_upper, use_lower, use_digits, use_symbols):
    variety = sum([use_upper, use_lower, use_digits, use_symbols])

    if length >= 12 and variety >= 3:
        return "Kuat"
    elif length >= 8 and variety >= 2:
        return "Sedang"
    else:
        return "Lemah"

# Alur utama program
def main():
    print("=" * 40)
    print("          PEMBUAT PASSWORD")
    print("=" * 40)

    length = get_password_length()
    use_upper = ask_yes_no("Sertakan huruf besar? (Y/N): ")
    use_lower = ask_yes_no("Sertakan huruf kecil? (Y/N): ")
    use_digits = ask_yes_no("Sertakan angka? (Y/N): ")
    use_symbols = ask_yes_no("Sertakan simbol? (Y/N): ")

    pool = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

    if not pool:
        print("\nAnda harus memilih setidaknya satu jenis karakter. Menggunakan huruf kecil sebagai default.")
        pool = string.ascii_lowercase
        use_lower = True

    password = generate_password(length, pool)
    strength = rate_strength(length, use_upper, use_lower, use_digits, use_symbols)

    print("\n" + "-" * 40)
    print(f"Password yang dihasilkan: {password}")
    print(f"Kekuatan password       : {strength}")
    print("-" * 40)


if __name__ == "__main__":
    while True:
        main()
        again = input("\nBuat password lain? (Y/N): ").strip().lower()
        if again not in ("y", "yes"):
            print("Sampai jumpa!")
            break
