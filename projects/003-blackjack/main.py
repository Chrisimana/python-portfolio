import random


SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = [
    "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "Jack", "Queen", "King", "Ace"
]

RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10,
    "Ace": 11,  # Ace ditangani secara khusus di calculate_hand_value
}

# Membuat dan mengacak satu set kartu standar berisi 52 kartu
def create_deck() -> list:
    deck = [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

# Mengambil bagian rank dari string kartu seperti 10 of Hearts
def card_rank(card: str) -> str:
    return card.split(" of ")[0]

# Menghitung nilai terbaik dari sebuah tangan Blackjack, memperlakukan Ace sebagai 11 kecuali itu akan membuat tangan bust, dalam hal ini Ace dihitung sebagai 1.
def calculate_hand_value(hand: list) -> int:
    value = sum(RANK_VALUES[card_rank(card)] for card in hand)
    num_aces = sum(1 for card in hand if card_rank(card) == "Ace")

    while value > 21 and num_aces > 0:
        value -= 10  # hitung satu Ace sebagai 1, bukan 11
        num_aces -= 1

    return value

# Mengambil satu kartu dari bagian atas deck
def deal_card(deck: list) -> str:
    return deck.pop()

# Menampilkan tangan kartu. Jika hide_first True, kartu pertama disembunyikan (untuk dealer).
def show_hand(name: str, hand: list, hide_first: bool = False) -> None:
    if hide_first:
        visible = ["Kartu Tersembunyi"] + hand[1:]
        print(f"Tangan {name}: {', '.join(visible)}")
    else:
        value = calculate_hand_value(hand)
        print(f"Tangan {name}: {', '.join(hand)} (nilai: {value})")

# Meminta pemain untuk memilih Hit atau Stand, mengembalikan True jika pemain bust, False jika tidak.
def player_turn(deck: list, player_hand: list) -> bool:
    while True:
        choice = input("Anda ingin (H)it atau (S)tand? ").strip().lower()

        if choice in ("h", "hit"):
            player_hand.append(deal_card(deck))
            show_hand("Pemain", player_hand)

            if calculate_hand_value(player_hand) > 21:
                print("\nAnda bust! Nilai tangan Anda melebihi 21.")
                return True

        elif choice in ("s", "stand"):
            print("Anda memilih untuk stand.")
            return False

        else:
            print("Pilihan tidak valid. Ketik 'H' untuk Hit atau 'S' untuk Stand.")

# Memainkan giliran dealer, dealer harus hit hingga mencapai nilai minimal 17.
def dealer_turn(deck: list, dealer_hand: list) -> None:
    print("\nDealer membuka tangan:")
    show_hand("Dealer", dealer_hand)

    while calculate_hand_value(dealer_hand) < 17:
        print("Dealer hit...")
        dealer_hand.append(deal_card(deck))
        show_hand("Dealer", dealer_hand)

# Menentukan pemenang berdasarkan nilai akhir tangan pemain dan dealer.
def determine_winner(player_value: int, dealer_value: int) -> str:
    if player_value > 21:
        return "Dealer menang! Pemain bust."
    if dealer_value > 21:
        return "Pemain menang! Dealer bust."
    if player_value > dealer_value:
        return "Pemain menang!"
    if dealer_value > player_value:
        return "Dealer menang!"
    return "Seri (push)!"

# Memainkan satu ronde Blackjack.
def play_round() -> None:
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print("\n" + "=" * 40)
    print("Ronde baru dimulai!")
    print("=" * 40)

    show_hand("Pemain", player_hand)
    show_hand("Dealer", dealer_hand, hide_first=True)

    # Cek apakah pemain langsung mendapat Blackjack alami
    if calculate_hand_value(player_hand) == 21:
        print("\nBlackjack! Anda menang dengan 21 alami.")
        return

    busted = player_turn(deck, player_hand)

    if not busted:
        dealer_turn(deck, dealer_hand)

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    print("\n" + "-" * 40)
    print(f"Nilai akhir pemain: {player_value}")
    print(f"Nilai akhir dealer: {dealer_value}")
    print(determine_winner(player_value, dealer_value))
    print("-" * 40)


def main():
    print("=" * 40)
    print("           PERMAINAN BLACKJACK")
    print("=" * 40)
    print("Aturan: Usahakan nilai kartu Anda sedekat mungkin dengan 21")
    print("tanpa melebihinya. Kartu bergambar bernilai 10,")
    print("Ace bernilai 11 atau 1, mana yang lebih menguntungkan Anda.")

    while True:
        play_round()

        again = input("\nApakah Anda ingin bermain ronde lagi? (Y/N): ").strip().lower()
        if again not in ("y", "yes"):
            print("\nTerima kasih telah bermain Blackjack. Sampai jumpa!")
            break


if __name__ == "__main__":
    main()
