import os


# Membersihkan layar terminal agar peserta berikutnya tidak bisa melihat tawaran sebelumnya
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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


# Meminta nama peserta lelang
def get_bidder_name():
    while True:
        name = input("Siapa nama Anda?: ").strip()
        if name:
            return name
        print("Nama tidak boleh kosong.")


# Meminta jumlah tawaran yang valid dari peserta
def get_bid_amount():
    while True:
        try:
            amount = float(input("Berapa tawaran Anda?: $"))
            if amount <= 0:
                print("Tawaran harus lebih besar dari 0.")
                continue
            return amount
        except ValueError:
            print("Input tidak valid. Mohon masukkan angka.")


# Mencari peserta dengan tawaran tertinggi dari dictionary tawaran yang terkumpul
def find_highest_bidder(bids):
    highest_name = None
    highest_bid = 0

    for name, bid in bids.items():
        if bid > highest_bid:
            highest_bid = bid
            highest_name = name

    return highest_name, highest_bid


# Alur utama program: mengumpulkan tawaran dari setiap peserta, lalu mengungkap pemenang
def main():
    print("=" * 40)
    print("        LELANG RAHASIA")
    print("=" * 40)
    print("Masukkan nama Anda dan tawaran rahasia Anda.")
    print("Layar akan dibersihkan setelah setiap peserta.\n")

    bids = {}
    still_bidding = True

    while still_bidding:
        name = get_bidder_name()
        amount = get_bid_amount()
        bids[name] = amount

        still_bidding = ask_yes_no("\nApakah masih ada peserta lain? (Y/N): ")
        clear_screen()

    winner, winning_bid = find_highest_bidder(bids)

    print("=" * 40)
    print("           HASIL LELANG")
    print("=" * 40)
    if winner:
        print(f"Pemenangnya adalah {winner} dengan tawaran ${winning_bid:.2f}")
    else:
        print("Tidak ada tawaran yang diajukan.")


if __name__ == "__main__":
    main()
