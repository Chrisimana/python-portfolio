def get_positive_float(prompt: str) -> float:
    # Meminta pengguna memasukkan angka desimal positif.
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Mohon masukkan nilai 0 atau lebih besar.")
                continue
            return value
        except ValueError:
            print("Input tidak valid. Mohon masukkan angka.")


def get_positive_int(prompt: str) -> int:
    # Meminta pengguna memasukkan bilangan bulat positif.
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Mohon masukkan jumlah orang lebih besar dari 0.")
                continue
            return value
        except ValueError:
            print("Input tidak valid. Mohon masukkan bilangan bulat.")


def calculate_tip(bill: float, tip_percent: float, people: int) -> dict:
    # Menghitung jumlah tip, total tagihan, dan jumlah per orang.
    tip_amount = bill * (tip_percent / 100)
    total_amount = bill + tip_amount
    amount_per_person = total_amount / people

    return {
        "bill": bill,
        "tip_percent": tip_percent,
        "tip_amount": tip_amount,
        "total_amount": total_amount,
        "people": people,
        "amount_per_person": amount_per_person,
    }


def print_receipt(result: dict) -> None:
    # Menampilkan ringkasan hasil perhitungan tip dengan format yang rapi.
    print("\n" + "=" * 35)
    print("           RINGKASAN TIP")
    print("=" * 35)
    print(f"Jumlah tagihan     : {result['bill']:.2f}")
    print(f"Persentase tip     : {result['tip_percent']:.1f}%")
    print(f"Jumlah tip         : {result['tip_amount']:.2f}")
    print(f"Total tagihan      : {result['total_amount']:.2f}")
    print(f"Jumlah orang       : {result['people']}")
    print("-" * 35)
    print(f"Jumlah per orang   : {result['amount_per_person']:.2f}")
    print("=" * 35)


def main():
    print("=" * 35)
    print("        KALKULATOR TIP")
    print("=" * 35)

    bill = get_positive_float("\nMasukkan jumlah tagihan: ")
    tip_percent = get_positive_float("Masukkan persentase tip (contoh: 10, 15, 20): ")
    people = get_positive_int("Masukkan jumlah orang yang membagi tagihan: ")

    result = calculate_tip(bill, tip_percent, people)
    print_receipt(result)

    print("\nTerima kasih telah menggunakan Kalkulator Tip!")


if __name__ == "__main__":
    main()
