import random

CHOICES = ["rock", "paper", "scissors"]

# Menentukan pilihan mana yang mengalahkan pilihan mana: key mengalahkan value
WINNING_RULES = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


# Memilih pilihan komputer secara acak
def get_computer_choice():
    return random.choice(CHOICES)


# Meminta pemain memasukkan pilihan yang valid (rock, paper, atau scissors)
def get_player_choice():
    while True:
        choice = input("Pilih rock, paper, atau scissors: ").strip().lower()
        if choice in CHOICES:
            return choice
        print("Pilihan tidak valid. Mohon ketik 'rock', 'paper', atau 'scissors'.")


# Menentukan pemenang ronde, mengembalikan 'player', 'computer', atau 'tie'
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "tie"
    elif WINNING_RULES[player_choice] == computer_choice:
        return "player"
    else:
        return "computer"


# Menampilkan hasil ronde berdasarkan siapa yang menang
def print_round_result(player_choice, computer_choice, result):
    print(f"\nAnda memilih     : {player_choice}")
    print(f"Komputer memilih : {computer_choice}")

    if result == "tie":
        print("Seri!")
    elif result == "player":
        print("Anda menang ronde ini!")
    else:
        print("Komputer menang ronde ini!")


# Menampilkan skor pertandingan saat ini
def print_score(player_score, computer_score, ties):
    print(f"\nSkor -> Anda: {player_score} | Komputer: {computer_score} | Seri: {ties}")


# Loop utama permainan yang menjalankan beberapa ronde hingga pemain berhenti
def main():
    print("=" * 40)
    print("        BATU GUNTING KERTAS")
    print("=" * 40)
    print("Ketik 'rock', 'paper', atau 'scissors' untuk bermain.")
    print("Ketik 'quit' kapan saja untuk berhenti bermain.\n")

    player_score = 0
    computer_score = 0
    ties = 0

    while True:
        choice_input = input("Pilih rock, paper, scissors (atau 'quit'): ").strip().lower()

        if choice_input == "quit":
            break

        if choice_input not in CHOICES:
            print("Pilihan tidak valid. Mohon ketik 'rock', 'paper', 'scissors', atau 'quit'.")
            continue

        computer_choice = get_computer_choice()
        result = determine_winner(choice_input, computer_choice)

        print_round_result(choice_input, computer_choice, result)

        if result == "player":
            player_score += 1
        elif result == "computer":
            computer_score += 1
        else:
            ties += 1

        print_score(player_score, computer_score, ties)
        print("-" * 40)

    print("\n" + "=" * 40)
    print("             SKOR AKHIR")
    print("=" * 40)
    print_score(player_score, computer_score, ties)

    if player_score > computer_score:
        print("\nSelamat, Anda memenangkan pertandingan!")
    elif computer_score > player_score:
        print("\nKomputer memenangkan pertandingan. Semoga beruntung lain kali!")
    else:
        print("\nPertandingan berakhir seri!")

    print("\nTerima kasih telah bermain!")


if __name__ == "__main__":
    main()
