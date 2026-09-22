import time


# Menampilkan teks dengan jeda singkat antar baris untuk kesan lebih dramatis
def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


# Menanyakan pertanyaan kepada pemain dan memvalidasi jawaban terhadap pilihan yang diperbolehkan
def ask_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Pilihan tidak valid. Mohon pilih salah satu dari: {', '.join(valid_choices)}.")


# Akhir cerita ketika pemain dimakan oleh troll
def ending_trolls():
    slow_print("\nAnda memasuki gua dan tertangkap oleh troll.")
    slow_print("PERMAINAN BERAKHIR.")


# Akhir cerita ketika pemain tenggelam di lautan
def ending_drown():
    slow_print("\nAnda melompat ke laut dan dimakan oleh ikan trout yang marah.")
    slow_print("PERMAINAN BERAKHIR.")


# Akhir cerita ketika pemain terbakar karena pintu jebakan api
def ending_fire():
    slow_print("\nAnda memilih pintu yang salah. Anda jatuh ke lubang api.")
    slow_print("PERMAINAN BERAKHIR.")


# Akhir cerita ketika pemain menemukan harta karun dan memenangkan permainan
def ending_treasure():
    slow_print("\nAnda membuka pintu dan menemukan peti harta karun!")
    slow_print("Selamat, Anda menemukan harta karun! ANDA MENANG!")


# Alur cerita utama, memandu pemain melalui serangkaian keputusan
def main():
    slow_print("=" * 40)
    slow_print("           PULAU HARTA KARUN")
    slow_print("=" * 40)
    slow_print("Selamat datang petualang di Pulau Harta Karun.")
    slow_print("Misi Anda adalah menemukan harta karun.\n")

    path = ask_choice(
        "Anda berada di persimpangan jalan. Ke arah mana? Ketik 'left' atau 'right': ",
        ("left", "right"),
    )

    if path == "right":
        ending_drown()
        return

    slow_print("\nAnda berjalan menyusuri jalur kiri dan tiba di sebuah sungai.")
    crossing = ask_choice(
        "Ada perahu dan jembatan. Ketik 'wait' untuk menunggu perahu atau 'swim' untuk menyeberangi sungai: ",
        ("wait", "swim"),
    )

    if crossing == "swim":
        ending_trolls()
        return

    slow_print("\nAnda berhasil menyeberangi sungai dengan selamat menggunakan perahu.")
    slow_print("Anda tiba di sebuah rumah dengan tiga pintu: merah, kuning, dan biru.")
    door = ask_choice(
        "Pintu mana yang Anda pilih? Ketik 'red', 'yellow', atau 'blue': ",
        ("red", "yellow", "blue"),
    )

    if door == "red":
        ending_fire()
    elif door == "yellow":
        ending_trolls()
    else:
        ending_treasure()


if __name__ == "__main__":
    while True:
        main()
        again = input("\nApakah Anda ingin bermain lagi? (Y/N): ").strip().lower()
        if again not in ("y", "yes"):
            print("Terima kasih telah bermain Pulau Harta Karun. Sampai jumpa!")
            break
