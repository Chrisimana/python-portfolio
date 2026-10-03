MILE_TO_KM = 1.60934


# Mengonversi jarak dari mil ke kilometer
def miles_to_km(miles: float) -> float:
    return miles * MILE_TO_KM


# Mengonversi jarak dari kilometer ke mil
def km_to_miles(km: float) -> float:
    return km / MILE_TO_KM


# Meminta pengguna memasukkan angka yang valid
def get_distance(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Mohon masukkan jarak yang bernilai 0 atau lebih besar.")
                continue
            return value
        except ValueError:
            print("Input tidak valid. Mohon masukkan angka.")


# Menampilkan menu pilihan arah konversi
def print_menu():
    print("\n" + "=" * 35)
    print("     MILE TO KM CONVERTER")
    print("=" * 35)
    print("1. Mil ke Kilometer")
    print("2. Kilometer ke Mil")
    print("3. Keluar")


# Alur utama program
def main():
    while True:
        print_menu()
        choice = input("Pilih opsi (1-3): ").strip()

        if choice == "1":
            miles = get_distance("Masukkan jarak dalam mil: ")
            result = miles_to_km(miles)
            print(f"\n{miles} mil = {result:.2f} km")

        elif choice == "2":
            km = get_distance("Masukkan jarak dalam kilometer: ")
            result = km_to_miles(km)
            print(f"\n{km} km = {result:.2f} mil")

        elif choice == "3":
            print("\nSampai jumpa!")
            break

        else:
            print("Opsi tidak valid. Mohon pilih antara 1 dan 3.")


if __name__ == "__main__":
    main()