import string


ALPHABET_SIZE = 26

# Menggeser satu karakter sejumlah nilai tertentu, tetap mempertahankan huruf besar/kecil
def shift_char(char: str, shift: int) -> str:
    if char.isupper():
        base = ord("A")
        return chr((ord(char) - base + shift) % ALPHABET_SIZE + base)
    elif char.islower():
        base = ord("a")
        return chr((ord(char) - base + shift) % ALPHABET_SIZE + base)
    else:
        # Biarkan karakter non-alfabet tidak berubah
        return char

# Mengenkripsi teks menggunakan Caesar Cipher dengan nilai shift yang diberikan
def encrypt(text: str, shift: int) -> str:
    return "".join(shift_char(char, shift) for char in text)

# Mendekripsi teks dengan menggeser ke arah sebaliknya.
def decrypt(text: str, shift: int) -> str:
    return "".join(shift_char(char, -shift) for char in text)

# Menampilkan setiap kemungkinan shift untuk membantu memecahkan sandi yang tidak diketahui.
def brute_force(text: str) -> None:
    print("\nHasil brute force (semua kemungkinan shift):")
    print("-" * 40)
    for possible_shift in range(1, ALPHABET_SIZE):
        result = decrypt(text, possible_shift)
        print(f"Shift {possible_shift:2d}: {result}")
    print("-" * 40)

# Meminta pengguna memasukkan nilai shift berupa bilangan bulat yang valid.
def get_shift_value() -> int:
    while True:
        try:
            shift = int(input("Masukkan nilai shift (contoh: 3): "))
            return shift % ALPHABET_SIZE
        except ValueError:
            print("Input tidak valid. Mohon masukkan bilangan bulat.")


def print_menu() -> None:
    print("\n" + "=" * 40)
    print("           SANDI CAESAR")
    print("=" * 40)
    print("1. Enkripsi pesan")
    print("2. Dekripsi pesan")
    print("3. Brute force decrypt (shift tidak diketahui)")
    print("4. Keluar")


def main():
    while True:
        print_menu()
        choice = input("Pilih opsi (1-4): ").strip()

        if choice == "1":
            text = input("Masukkan pesan yang ingin dienkripsi: ")
            shift = get_shift_value()
            result = encrypt(text, shift)
            print(f"\nPesan terenkripsi: {result}")

        elif choice == "2":
            text = input("Masukkan pesan yang ingin didekripsi: ")
            shift = get_shift_value()
            result = decrypt(text, shift)
            print(f"\nPesan terdekripsi: {result}")

        elif choice == "3":
            text = input("Masukkan pesan terenkripsi: ")
            brute_force(text)

        elif choice == "4":
            print("\nSampai jumpa!")
            break

        else:
            print("Opsi tidak valid. Mohon pilih antara 1 dan 4.")


if __name__ == "__main__":
    main()
