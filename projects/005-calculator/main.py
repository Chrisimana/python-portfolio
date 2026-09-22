import math

# Melakukan penjumlahan dua angka
def add(a, b):
    return a + b

# Melakukan pengurangan dua angka
def subtract(a, b):
    return a - b

# Melakukan perkalian dua angka
def multiply(a, b):
    return a * b

# Melakukan pembagian dua angka, memunculkan error jika dibagi dengan nol
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Tidak dapat membagi dengan nol.")
    return a / b

# Melakukan pemangkatan
def power(a, b):
    return math.pow(a, b)

# Melakukan operasi modulus
def modulus(a, b):
    if b == 0:
        raise ZeroDivisionError("Tidak dapat melakukan modulus dengan nol.")
    return a % b

# Meminta pengguna memasukkan angka yang valid, terus bertanya sampai valid
def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Input tidak valid. Mohon masukkan angka yang valid.")

# Menampilkan menu utama operasi
def print_menu():
    print("\n" + "=" * 35)
    print("            KALKULATOR")
    print("=" * 35)
    print("1. Penjumlahan     (+)")
    print("2. Pengurangan     (-)")
    print("3. Perkalian       (*)")
    print("4. Pembagian       (/)")
    print("5. Pemangkatan     (^)")
    print("6. Modulus         (%)")
    print("7. Keluar")

# Loop utama program yang menangani pemilihan menu dan perhitungan
def main():
    operations = {
        "1": ("Penjumlahan", add),
        "2": ("Pengurangan", subtract),
        "3": ("Perkalian", multiply),
        "4": ("Pembagian", divide),
        "5": ("Pemangkatan", power),
        "6": ("Modulus", modulus),
    }

    while True:
        print_menu()
        choice = input("Pilih opsi (1-7): ").strip()

        if choice == "7":
            print("\nSampai jumpa!")
            break

        if choice not in operations:
            print("Opsi tidak valid. Mohon pilih antara 1 dan 7.")
            continue

        name, operation = operations[choice]
        num1 = get_number("Masukkan angka pertama: ")
        num2 = get_number("Masukkan angka kedua: ")

        try:
            result = operation(num1, num2)
            print(f"\nHasil {name}: {num1} dan {num2} -> {result}")
        except ZeroDivisionError as error:
            print(f"\nError: {error}")


# Titik masuk program
if __name__ == "__main__":
    main()
