# Tata letak labirin: '#' = tembok, '.' = jalur terbuka, 'S' = start, 'E' = exit
MAZE_TEMPLATE = [
    "##############",
    "#S...#.......#",
    "#.##.#.#####.#",
    "#.#..#.#...#.#",
    "#.#.##.#.#.#.#",
    "#...#..#.#.#.#",
    "###.#.##.#.#.#",
    "#...#....#...#",
    "#.#####.###.##",
    "#.......#...E#",
    "##############",
]


# Mengubah template labirin menjadi list 2D karakter agar dapat diubah.
def build_maze(template):
    return [list(row) for row in template]


# Mencari koordinat sebuah simbol di dalam labirin.
def find_symbol(maze, symbol):
    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            if cell == symbol:
                return row_index, col_index
    return None


# Menampilkan kondisi labirin saat ini, menunjukkan posisi pemain.
def print_maze(maze, player_pos):
    row, col = player_pos
    print()
    for r, line in enumerate(maze):
        display_row = ""
        for c, cell in enumerate(line):
            if (r, c) == (row, col):
                display_row += "P"
            else:
                display_row += cell
        print(display_row)
    print()


# Mengecek apakah sebuah posisi merupakan gerakan yang valid.
def is_valid_move(maze, row, col):
    if row < 0 or row >= len(maze):
        return False
    if col < 0 or col >= len(maze[row]):
        return False
    return maze[row][col] != "#"


# Menghitung posisi baru berdasarkan arah gerakan.
def get_new_position(row, col, direction):
    if direction == "w":
        return row - 1, col
    elif direction == "s":
        return row + 1, col
    elif direction == "a":
        return row, col - 1
    elif direction == "d":
        return row, col + 1
    return row, col


# Meminta pengguna memasukkan perintah gerakan yang valid.
def get_move_input():
    valid_moves = ("w", "a", "s", "d", "q")
    while True:
        move = input("Gerakan (W=atas, A=kiri, S=bawah, D=kanan, Q=keluar): ").strip().lower()
        if move in valid_moves:
            return move
        print("Input tidak valid. Mohon masukkan W, A, S, D, atau Q.")


# Loop utama permainan yang menangani pergerakan pemain dan kondisi menang.
def main():
    maze = build_maze(MAZE_TEMPLATE)
    player_pos = find_symbol(maze, "S")
    exit_pos = find_symbol(maze, "E")

    print("=" * 40)
    print("           KABUR DARI LABIRIN")
    print("=" * 40)
    print("Bimbing P (Anda) dari S menuju E.")
    print("Hindari tembok (#) di sepanjang jalan.")

    move_count = 0

    while True:
        print_maze(maze, player_pos)

        if player_pos == exit_pos:
            print(f"Anda berhasil kabur dari labirin dalam {move_count} langkah!")
            break

        move = get_move_input()

        if move == "q":
            print("Anda menyerah. Semoga beruntung lain kali.")
            break

        new_row, new_col = get_new_position(player_pos[0], player_pos[1], move)

        if is_valid_move(maze, new_row, new_col):
            player_pos = (new_row, new_col)
            move_count += 1
        else:
            print("Anda menabrak tembok! Coba arah lain.")


if __name__ == "__main__":
    main()
