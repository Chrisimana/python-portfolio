import pygame
import random
import sys

UKURAN_SEL = 56
MARGIN = 24
TINGGI_ATAS = 56
TINGGI_BAWAH = 110
UKURAN_GRID = UKURAN_SEL * 9
LEBAR_LAYAR = UKURAN_GRID + MARGIN * 2
TINGGI_LAYAR = TINGGI_ATAS + UKURAN_GRID + TINGGI_BAWAH
FPS = 30

WARNA_LATAR = (245, 243, 238)
WARNA_SEL = (255, 255, 255)
WARNA_SOROT = (222, 230, 245)
WARNA_ANGKA_SAMA = (196, 214, 242)
WARNA_PILIHAN = (150, 185, 240)
WARNA_BENTROK = (250, 205, 205)
WARNA_GARIS_TIPIS = (190, 190, 195)
WARNA_GARIS_TEBAL = (40, 40, 48)
WARNA_ANGKA_TETAP = (30, 30, 38)
WARNA_ANGKA_ISIAN = (35, 95, 200)
WARNA_ANGKA_SALAH = (205, 45, 45)
WARNA_TEKS = (50, 50, 60)
WARNA_TEKS_REDUP = (120, 120, 130)
WARNA_MENANG = (40, 150, 80)

# Jumlah sel kosong pada puzzle untuk setiap tingkat kesulitan
KESULITAN = {"mudah": 36, "sedang": 46, "sulit": 52}


# Penyelesai Sudoku berbasis bitmask dengan heuristik memilih sel yang paling sedikit kandidatnya
class Penyelesai:
    def __init__(self, papan):
        self.papan = [baris[:] for baris in papan]
        self.baris = [0] * 9
        self.kolom = [0] * 9
        self.kotak = [0] * 9

        for r in range(9):
            for c in range(9):
                nilai = self.papan[r][c]
                if nilai:
                    self._pasang(r, c, nilai)

    @staticmethod
    def _indeks_kotak(r, c):
        return 3 * (r // 3) + c // 3

    def _pasang(self, r, c, nilai):
        bit = 1 << nilai
        self.baris[r] |= bit
        self.kolom[c] |= bit
        self.kotak[self._indeks_kotak(r, c)] |= bit
        self.papan[r][c] = nilai

    def _lepas(self, r, c, nilai):
        bit = 1 << nilai
        self.baris[r] &= ~bit
        self.kolom[c] &= ~bit
        self.kotak[self._indeks_kotak(r, c)] &= ~bit
        self.papan[r][c] = 0

    # Mencari sel kosong dengan kandidat paling sedikit, mengembalikan (r, c, mask) atau None jika penuh
    def _pilih_sel(self):
        terbaik = None
        jumlah_terkecil = 10

        for r in range(9):
            for c in range(9):
                if self.papan[r][c] != 0:
                    continue

                mask = ~(self.baris[r] | self.kolom[c] | self.kotak[self._indeks_kotak(r, c)]) & 0x3FE
                jumlah = bin(mask).count("1")
                if jumlah < jumlah_terkecil:
                    jumlah_terkecil = jumlah
                    terbaik = (r, c, mask)
                    if jumlah <= 1:
                        return terbaik

        return terbaik

    @staticmethod
    def _daftar_angka(mask):
        return [n for n in range(1, 10) if mask & (1 << n)]

    # Menyelesaikan papan dengan backtracking, opsi acak untuk menghasilkan solusi yang bervariasi
    def selesaikan(self, acak=False):
        pilihan = self._pilih_sel()
        if pilihan is None:
            return True

        r, c, mask = pilihan
        angka = self._daftar_angka(mask)
        if acak:
            random.shuffle(angka)

        for nilai in angka:
            self._pasang(r, c, nilai)
            if self.selesaikan(acak):
                return True
            self._lepas(r, c, nilai)

        return False

    # Menghitung jumlah solusi yang mungkin, berhenti begitu mencapai batas
    def hitung_solusi(self, batas=2):
        pilihan = self._pilih_sel()
        if pilihan is None:
            return 1

        r, c, mask = pilihan
        total = 0
        for nilai in self._daftar_angka(mask):
            self._pasang(r, c, nilai)
            total += self.hitung_solusi(batas - total)
            self._lepas(r, c, nilai)
            if total >= batas:
                break

        return total


# Membuat puzzle Sudoku baru dengan satu solusi unik
class GeneratorPuzzle:
    # Menghasilkan solusi lengkap secara acak
    @staticmethod
    def buat_solusi():
        penyelesai = Penyelesai([[0] * 9 for _ in range(9)])
        penyelesai.selesaikan(acak=True)
        return penyelesai.papan

    # Mengosongkan sel satu per satu selama puzzle tetap memiliki tepat satu solusi
    @staticmethod
    def buat_puzzle(solusi, jumlah_kosong):
        puzzle = [baris[:] for baris in solusi]
        posisi = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(posisi)

        dikosongkan = 0
        for r, c in posisi:
            if dikosongkan >= jumlah_kosong:
                break

            nilai_asli = puzzle[r][c]
            puzzle[r][c] = 0
            if Penyelesai(puzzle).hitung_solusi(2) == 1:
                dikosongkan += 1
            else:
                puzzle[r][c] = nilai_asli

        return puzzle


# Mengelola state papan Sudoku: sel tetap, isian pemain, dan pengecekan bentrokan
class PapanSudoku:
    def __init__(self, tingkat):
        self.tingkat = tingkat
        self.solusi = GeneratorPuzzle.buat_solusi()
        self.puzzle = GeneratorPuzzle.buat_puzzle(self.solusi, KESULITAN[tingkat])
        self.isian = [baris[:] for baris in self.puzzle]

    # Mengecek apakah sel merupakan angka bawaan puzzle
    def sel_tetap(self, r, c):
        return self.puzzle[r][c] != 0

    # Mengisi sel dengan angka (0 untuk menghapus), sel bawaan tidak dapat diubah
    def isi(self, r, c, nilai):
        if not self.sel_tetap(r, c):
            self.isian[r][c] = nilai

    # Mengisi sel dengan jawaban yang benar sebagai petunjuk
    def beri_petunjuk(self, r, c):
        if self.sel_tetap(r, c) or self.isian[r][c] == self.solusi[r][c]:
            return False
        self.isian[r][c] = self.solusi[r][c]
        return True

    # Mengecek apakah angka pada sel bentrok dengan angka lain di baris, kolom, atau kotak
    def bentrok(self, r, c):
        nilai = self.isian[r][c]
        if nilai == 0:
            return False

        for i in range(9):
            if i != c and self.isian[r][i] == nilai:
                return True
            if i != r and self.isian[i][c] == nilai:
                return True

        br, bc = 3 * (r // 3), 3 * (c // 3)
        for rr in range(br, br + 3):
            for cc in range(bc, bc + 3):
                if (rr, cc) != (r, c) and self.isian[rr][cc] == nilai:
                    return True

        return False

    # Mengecek apakah puzzle sudah terisi penuh dan tanpa bentrokan
    def selesai(self):
        for r in range(9):
            for c in range(9):
                if self.isian[r][c] == 0 or self.bentrok(r, c):
                    return False
        return True


# Mengatur tampilan, input, dan alur permainan Sudoku
class GameSudoku:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku")
        self.layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
        self.jam = pygame.time.Clock()
        self.font_angka = pygame.font.Font(None, 46)
        self.font_judul = pygame.font.Font(None, 34)
        self.font_kecil = pygame.font.Font(None, 22)
        self.font_besar = pygame.font.Font(None, 56)

        self.tingkat = "mudah"
        self.mulai_baru()

    # Membuat puzzle baru sesuai tingkat kesulitan saat ini
    def mulai_baru(self, tingkat=None):
        if tingkat:
            self.tingkat = tingkat

        self.papan = PapanSudoku(self.tingkat)
        self.pilihan = (4, 4)
        self.jumlah_petunjuk = 0
        self.waktu_mulai = pygame.time.get_ticks()
        self.waktu_akhir = None
        self.pesan = ""

    # Menghitung waktu bermain dalam detik
    def waktu_berjalan(self):
        akhir = self.waktu_akhir if self.waktu_akhir is not None else pygame.time.get_ticks()
        return (akhir - self.waktu_mulai) // 1000

    # Menandai permainan selesai jika seluruh sel benar
    def _periksa_selesai(self):
        if self.waktu_akhir is None and self.papan.selesai():
            self.waktu_akhir = pygame.time.get_ticks()

    # Mengubah sel yang dipilih berdasarkan klik mouse
    def tangani_klik(self, posisi):
        x, y = posisi
        c = (x - MARGIN) // UKURAN_SEL
        r = (y - TINGGI_ATAS) // UKURAN_SEL
        if 0 <= r < 9 and 0 <= c < 9 and x >= MARGIN and y >= TINGGI_ATAS:
            self.pilihan = (r, c)

    # Menangani input keyboard
    def tangani_tombol(self, tombol):
        r, c = self.pilihan
        selesai = self.waktu_akhir is not None

        if tombol == pygame.K_n:
            self.mulai_baru()
            return
        if tombol == pygame.K_e:
            self.mulai_baru("mudah")
            return
        if tombol == pygame.K_m:
            self.mulai_baru("sedang")
            return
        if tombol == pygame.K_s:
            self.mulai_baru("sulit")
            return

        if tombol == pygame.K_UP:
            self.pilihan = (max(0, r - 1), c)
        elif tombol == pygame.K_DOWN:
            self.pilihan = (min(8, r + 1), c)
        elif tombol == pygame.K_LEFT:
            self.pilihan = (r, max(0, c - 1))
        elif tombol == pygame.K_RIGHT:
            self.pilihan = (r, min(8, c + 1))

        if selesai:
            return

        angka_tombol = {
            **{getattr(pygame, f"K_{n}"): n for n in range(1, 10)},
            **{getattr(pygame, f"K_KP{n}"): n for n in range(1, 10)},
        }

        if tombol in angka_tombol:
            self.papan.isi(r, c, angka_tombol[tombol])
        elif tombol in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0, pygame.K_KP0):
            self.papan.isi(r, c, 0)
        elif tombol == pygame.K_h:
            if self.papan.beri_petunjuk(r, c):
                self.jumlah_petunjuk += 1

        self._periksa_selesai()

    # Menangani seluruh event Pygame
    def tangani_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.tangani_klik(event.pos)
        if event.type == pygame.KEYDOWN:
            self.tangani_tombol(event.key)
        return True

    # Menentukan warna latar sebuah sel berdasarkan pilihan, sorotan, dan bentrokan
    def _warna_sel(self, r, c):
        pr, pc = self.pilihan
        nilai_pilihan = self.papan.isian[pr][pc]

        if (r, c) == self.pilihan:
            return WARNA_PILIHAN
        if self.papan.bentrok(r, c):
            return WARNA_BENTROK
        if nilai_pilihan != 0 and self.papan.isian[r][c] == nilai_pilihan:
            return WARNA_ANGKA_SAMA
        if r == pr or c == pc or (r // 3 == pr // 3 and c // 3 == pc // 3):
            return WARNA_SOROT
        return WARNA_SEL

    # Menggambar papan 9x9 beserta seluruh angkanya
    def _gambar_grid(self):
        for r in range(9):
            for c in range(9):
                rect = pygame.Rect(MARGIN + c * UKURAN_SEL, TINGGI_ATAS + r * UKURAN_SEL, UKURAN_SEL, UKURAN_SEL)
                pygame.draw.rect(self.layar, self._warna_sel(r, c), rect)

                nilai = self.papan.isian[r][c]
                if nilai:
                    if self.papan.sel_tetap(r, c):
                        warna = WARNA_ANGKA_TETAP
                    elif self.papan.bentrok(r, c):
                        warna = WARNA_ANGKA_SALAH
                    else:
                        warna = WARNA_ANGKA_ISIAN
                    teks = self.font_angka.render(str(nilai), True, warna)
                    self.layar.blit(teks, teks.get_rect(center=rect.center))

        for i in range(10):
            tebal = 3 if i % 3 == 0 else 1
            warna = WARNA_GARIS_TEBAL if i % 3 == 0 else WARNA_GARIS_TIPIS
            posisi = i * UKURAN_SEL
            pygame.draw.line(
                self.layar, warna,
                (MARGIN, TINGGI_ATAS + posisi), (MARGIN + UKURAN_GRID, TINGGI_ATAS + posisi), tebal,
            )
            pygame.draw.line(
                self.layar, warna,
                (MARGIN + posisi, TINGGI_ATAS), (MARGIN + posisi, TINGGI_ATAS + UKURAN_GRID), tebal,
            )

    # Menggambar bagian atas (judul, kesulitan, waktu) dan bagian bawah (petunjuk kontrol)
    def _gambar_info(self):
        teks_judul = self.font_judul.render(f"SUDOKU - {self.tingkat.upper()}", True, WARNA_TEKS)
        self.layar.blit(teks_judul, (MARGIN, 16))

        menit, detik = divmod(self.waktu_berjalan(), 60)
        teks_waktu = self.font_judul.render(f"{menit:02d}:{detik:02d}", True, WARNA_TEKS)
        self.layar.blit(teks_waktu, teks_waktu.get_rect(topright=(LEBAR_LAYAR - MARGIN, 16)))

        y = TINGGI_ATAS + UKURAN_GRID + 14
        baris_petunjuk = [
            "Klik/panah: pilih sel | 1-9: isi | Backspace: hapus",
            f"H: petunjuk (dipakai {self.jumlah_petunjuk}x) | N: puzzle baru",
            "E: mudah | M: sedang | S: sulit (memulai puzzle baru)",
        ]
        for i, baris in enumerate(baris_petunjuk):
            teks = self.font_kecil.render(baris, True, WARNA_TEKS_REDUP)
            self.layar.blit(teks, (MARGIN, y + i * 24))

    # Menggambar pesan kemenangan di atas papan
    def _gambar_menang(self):
        if self.waktu_akhir is None:
            return

        lapisan = pygame.Surface((UKURAN_GRID, 120), pygame.SRCALPHA)
        lapisan.fill((255, 255, 255, 225))
        posisi = (MARGIN, TINGGI_ATAS + UKURAN_GRID // 2 - 60)
        self.layar.blit(lapisan, posisi)

        teks = self.font_besar.render("SELESAI!", True, WARNA_MENANG)
        sub = self.font_kecil.render("Tekan N untuk puzzle baru", True, WARNA_TEKS)
        self.layar.blit(teks, teks.get_rect(center=(LEBAR_LAYAR // 2, posisi[1] + 42)))
        self.layar.blit(sub, sub.get_rect(center=(LEBAR_LAYAR // 2, posisi[1] + 88)))

    # Menggambar seluruh elemen ke layar
    def gambar(self):
        self.layar.fill(WARNA_LATAR)
        self._gambar_info()
        self._gambar_grid()
        self._gambar_menang()
        pygame.display.flip()

    # Menjalankan game loop utama
    def jalankan(self):
        berjalan = True
        while berjalan:
            for event in pygame.event.get():
                if not self.tangani_event(event):
                    berjalan = False

            self.gambar()
            self.jam.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    game = GameSudoku()
    game.jalankan()


if __name__ == "__main__":
    main()
