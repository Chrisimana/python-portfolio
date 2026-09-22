import random

# Setiap item memiliki nama dan jumlah followers (dalam juta) untuk perbandingan
ITEMS = [
    {"name": "Instagram", "followers": 2500},
    {"name": "YouTube", "followers": 2200},
    {"name": "TikTok", "followers": 1500},
    {"name": "Facebook", "followers": 2900},
    {"name": "Twitter (X)", "followers": 550},
    {"name": "LinkedIn", "followers": 900},
    {"name": "Pinterest", "followers": 450},
    {"name": "Snapchat", "followers": 750},
    {"name": "Reddit", "followers": 500},
    {"name": "Netflix", "followers": 260},
]


# Memilih item secara acak dari daftar, opsional mengecualikan item tertentu
def get_random_item(exclude=None):
    choices = [item for item in ITEMS if item != exclude]
    return random.choice(choices)


# Menampilkan kedua item tanpa membocorkan jumlah followers-nya
def print_items(item_a, item_b):
    print(f"\nBandingkan A: {item_a['name']}")
    print("melawan")
    print(f"Bandingkan B: {item_b['name']}")


# Meminta pemain menebak item mana yang memiliki followers lebih banyak, A atau B
def get_guess():
    while True:
        guess = input("Siapa yang memiliki followers lebih banyak? Ketik 'A' atau 'B': ").strip().lower()
        if guess in ("a", "b"):
            return guess
        print("Input tidak valid. Mohon ketik 'A' atau 'B'.")


# Mengecek apakah tebakan pemain benar
def check_guess(guess, item_a, item_b):
    if guess == "a":
        return item_a["followers"] >= item_b["followers"]
    else:
        return item_b["followers"] >= item_a["followers"]


# Loop utama permainan yang berlanjut hingga pemain menebak salah
def main():
    print("=" * 40)
    print("      TEBAK LEBIH TINGGI/RENDAH")
    print("=" * 40)
    print("Tebak akun mana yang memiliki followers lebih banyak!")

    score = 0
    item_a = get_random_item()
    item_b = get_random_item(exclude=item_a)

    while True:
        print_items(item_a, item_b)
        guess = get_guess()

        correct = check_guess(guess, item_a, item_b)

        if not correct:
            print(f"\nSalah! {item_a['name']} memiliki {item_a['followers']}Jt followers, "
                  f"{item_b['name']} memiliki {item_b['followers']}Jt followers.")
            break

        score += 1
        print(f"\nBenar! Skor Anda sekarang {score}.")

        # Pemenang ronde sebelumnya menjadi item A untuk ronde berikutnya
        winner = item_a if item_a["followers"] >= item_b["followers"] else item_b
        item_a = winner
        item_b = get_random_item(exclude=item_a)

    print(f"\nSkor akhir: {score}")


if __name__ == "__main__":
    while True:
        main()
        again = input("\nApakah Anda ingin bermain lagi? (Y/N): ").strip().lower()
        if again not in ("y", "yes"):
            print("Terima kasih telah bermain Tebak Lebih Tinggi/Rendah. Sampai jumpa!")
            break
