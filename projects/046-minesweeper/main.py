import pygame
import random
import sys
from collections import deque

JUMLAH_KOLOM = 12
JUMLAH_BARIS = 12
JUMLAH_RANJAU = 20
UKURAN_SEL = 36
TINGGI_HEADER = 80
LEBAR_LAYAR = JUMLAH_KOLOM * UKURAN_SEL
TINGGI_LAYAR = JUMLAH_BARIS * UKURAN_SEL + TINGGI_HEADER
FPS = 30

WARNA_LATAR = (30, 33, 40)
WARNA_SEL_TERTUTUP = (96, 106, 126)
WARNA_SEL_TERBUKA = (208, 213, 223)
WARNA_SEL_MELEDAK = (220, 70, 70)
WARNA_TEKS = (240, 240, 240)
WARNA_BENDERA = (225, 60, 60)
WARNA_RANJAU = (30, 30, 30)
WARNA_MENANG = (110, 210, 130)
WARNA_KALAH = (235, 100, 100)
WARNA_ANGKA = {
    1: (30, 90, 220), 2: (30, 140, 60), 3: (210, 50, 50), 4: (20, 20, 140),
    5: (140, 30, 30), 6: (20, 140, 140), 7: (0, 0, 0), 8: (100, 100, 100),
}


# Merepresentasikan satu sel pada papan
class Sel:
    def __init__(self):
        self.ranjau = False
        self.terbuka = False
        self.bendera = False
        self.tetangga = 0 


# Mengelola seluruh logika papan: pemasangan ranjau, pembukaan sel, dan kondisi menang
class Papan:
    def __init__(self, kolom, baris, jumlah_ranjau):
        self.kolom = kolom
        self.baris = baris
        self.jumlah_ranjau = jumlah_ranjau
        self.reset()

    # Mengosongkan papan dan mengembalikan seluruh status ke kondisi awal
    def reset(self):
        self.grid = [[Sel() for _ in range(self.kolom)] for _ in range(self.baris)]
        self.ranjau_terpasang = False
        self.jumlah_terbuka = 0
        self.jumlah_bendera = 0

    # Menghasilkan koordinat seluruh tetangga yang valid dari sebuah sel
    def _tetangga(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.baris and 0 <= nc < self.kolom:
                    yield nr, nc

    # Memasang ranjau secara acak setelah klik pertama, sel yang diklik beserta tetangganya dijaga aman
    def _pasang_ranjau(self, aman_r, aman_c):
        zona_aman = {(aman_r, aman_c)} | set(self._tetangga(aman_r, aman_c))
        kandidat = [
            (r, c)
            for r in range(self.baris)
            for c in range(self.kolom)
            if (r, c) not in zona_aman
        ]

        for r, c in random.sample(kandidat, self.jumlah_ranjau):
            self.grid[r][c].ranjau = True

        for r in range(self.baris):
            for c in range(self.kolom):
                self.grid[r][c].tetangga = sum(
                    1 for nr, nc in self._tetangga(r, c) if self.grid[nr][nc].ranjau
                )

        self.ranjau_terpasang = True

    # Membuka sebuah sel, mengembalikan "ranjau", "ok", atau "abaikan"
    def buka(self, r, c):
        sel = self.grid[r][c]
        if sel.terbuka or sel.bendera:
            return "abaikan"

        if not self.ranjau_terpasang:
            self._pasang_ranjau(r, c)

        if sel.ranjau:
            sel.terbuka = True
            return "ranjau"

        # Membuka area kosong secara berantai menggunakan antrean (flood fill)
        antrean = deque([(r, c)])
        while antrean:
            cr, cc = antrean.popleft()
            sel_sekarang = self.grid[cr][cc]
            if sel_sekarang.terbuka or sel_sekarang.bendera:
                continue

            sel_sekarang.terbuka = True
            self.jumlah_terbuka += 1

            if sel_sekarang.tetangga == 0:
                for nr, nc in self._tetangga(cr, cc):
                    tetangga = self.grid[nr][nc]
                    if not tetangga.terbuka and not tetangga.bendera and not tetangga.ranjau:
                        antrean.append((nr, nc))

        return "ok"

    # Membuka seluruh tetangga sebuah angka jika jumlah bendera di sekitarnya sudah sesuai
    def buka_sekitar(self, r, c):
        sel = self.grid[r][c]
        if not sel.terbuka or sel.tetangga == 0:
            return "abaikan"

        daftar_tetangga = list(self._tetangga(r, c))
        jumlah_bendera = sum(1 for nr, nc in daftar_tetangga if self.grid[nr][nc].bendera)
        if jumlah_bendera != sel.tetangga:
            return "abaikan"

        hasil = "ok"
        for nr, nc in daftar_tetangga:
            tetangga = self.grid[nr][nc]
            if not tetangga.bendera and not tetangga.terbuka:
                if self.buka(nr, nc) == "ranjau":
                    hasil = "ranjau"
        return hasil

    # Memasang atau mencabut bendera pada sel yang belum terbuka
    def toggle_bendera(self, r, c):
        sel = self.grid[r][c]
        if sel.terbuka:
            return

        sel.bendera = not sel.bendera
        self.jumlah_bendera += 1 if sel.bendera else -1

    # Menandai seluruh ranjau dengan bendera saat pemain menang
    def tandai_semua_ranjau(self):
        for baris in self.grid:
            for sel in baris:
                if sel.ranjau and not sel.bendera:
                    sel.bendera = True
                    self.jumlah_bendera += 1

    # Mengecek apakah seluruh sel aman sudah terbuka
    def menang(self):
        return self.jumlah_terbuka == self.kolom * self.baris - self.jumlah_ranjau


# Mengatur tampilan, input, dan alur permainan Minesweeper
class GameMinesweeper:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
        self.jam = pygame.time.Clock()
        self.font_besar = pygame.font.Font(None, 40)
        self.font_sedang = pygame.font.Font(None, 30)
        self.font_kecil = pygame.font.Font(None, 22)
        self.font_angka = pygame.font.Font(None, 30)

        self.papan = Papan(JUMLAH_KOLOM, JUMLAH_BARIS, JUMLAH_RANJAU)
        self.mulai_baru()

    # Menyiapkan permainan baru
    def mulai_baru(self):
        self.papan.reset()
        self.status = "siap"  # siap, main, menang, kalah
        self.waktu_mulai = 0
        self.waktu_akhir = 0

    # Menghitung waktu bermain dalam detik
    def waktu_berjalan(self):
        if self.status == "siap":
            return 0
        if self.status == "main":
            return (pygame.time.get_ticks() - self.waktu_mulai) // 1000
        return self.waktu_akhir

    # Memproses hasil pembukaan sel dan memperbarui status permainan
    def _proses_hasil(self, hasil):
        if hasil == "ranjau":
            self.status = "kalah"
            self.waktu_akhir = (pygame.time.get_ticks() - self.waktu_mulai) // 1000
        elif self.papan.menang():
            self.status = "menang"
            self.waktu_akhir = (pygame.time.get_ticks() - self.waktu_mulai) // 1000
            self.papan.tandai_semua_ranjau()

    # Menangani klik mouse pada papan
    def tangani_klik(self, posisi, tombol):
        x, y = posisi
        if y < TINGGI_HEADER or self.status in ("menang", "kalah"):
            return

        c = x // UKURAN_SEL
        r = (y - TINGGI_HEADER) // UKURAN_SEL
        if not (0 <= r < JUMLAH_BARIS and 0 <= c < JUMLAH_KOLOM):
            return

        if tombol == 1:
            if self.status == "siap":
                self.status = "main"
                self.waktu_mulai = pygame.time.get_ticks()

            if self.papan.grid[r][c].terbuka:
                hasil = self.papan.buka_sekitar(r, c)
            else:
                hasil = self.papan.buka(r, c)
            self._proses_hasil(hasil)

        elif tombol == 3:
            self.papan.toggle_bendera(r, c)

    # Menangani seluruh event Pygame
    def tangani_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.mulai_baru()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.tangani_klik(event.pos, event.button)
        return True

    # Menggambar bendera di dalam sebuah area
    def _gambar_bendera(self, rect):
        tiang_x = rect.centerx
        pygame.draw.line(self.layar, WARNA_RANJAU, (tiang_x, rect.top + 7), (tiang_x, rect.bottom - 8), 3)
        segitiga = [(tiang_x, rect.top + 7), (tiang_x - 11, rect.top + 13), (tiang_x, rect.top + 19)]
        pygame.draw.polygon(self.layar, WARNA_BENDERA, segitiga)
        pygame.draw.line(self.layar, WARNA_RANJAU, (rect.centerx - 8, rect.bottom - 7), (rect.centerx + 8, rect.bottom - 7), 3)

    # Menggambar ranjau di dalam sebuah area
    def _gambar_ranjau(self, rect):
        pusat = rect.center
        for dx, dy in [(-9, 0), (9, 0), (0, -9), (0, 9), (-6, -6), (6, 6), (-6, 6), (6, -6)]:
            pygame.draw.line(self.layar, WARNA_RANJAU, pusat, (pusat[0] + dx, pusat[1] + dy), 2)
        pygame.draw.circle(self.layar, WARNA_RANJAU, pusat, 7)
        pygame.draw.circle(self.layar, (240, 240, 240), (pusat[0] - 2, pusat[1] - 2), 2)

    # Menggambar satu sel sesuai kondisinya
    def _gambar_sel(self, r, c):
        sel = self.papan.grid[r][c]
        rect = pygame.Rect(c * UKURAN_SEL, TINGGI_HEADER + r * UKURAN_SEL, UKURAN_SEL, UKURAN_SEL)
        rect_dalam = rect.inflate(-2, -2)
        permainan_selesai = self.status in ("menang", "kalah")

        if sel.terbuka:
            warna = WARNA_SEL_MELEDAK if sel.ranjau else WARNA_SEL_TERBUKA
            pygame.draw.rect(self.layar, warna, rect_dalam)
            if sel.ranjau:
                self._gambar_ranjau(rect)
            elif sel.tetangga > 0:
                teks = self.font_angka.render(str(sel.tetangga), True, WARNA_ANGKA[sel.tetangga])
                self.layar.blit(teks, teks.get_rect(center=rect.center))
            return

        if permainan_selesai and sel.ranjau and not sel.bendera:
            pygame.draw.rect(self.layar, WARNA_SEL_TERBUKA, rect_dalam)
            self._gambar_ranjau(rect)
            return

        pygame.draw.rect(self.layar, WARNA_SEL_TERTUTUP, rect_dalam)
        pygame.draw.line(self.layar, (130, 140, 160), rect_dalam.topleft, rect_dalam.topright, 2)
        pygame.draw.line(self.layar, (130, 140, 160), rect_dalam.topleft, rect_dalam.bottomleft, 2)

        if sel.bendera:
            self._gambar_bendera(rect)
            if self.status == "kalah" and not sel.ranjau:
                pygame.draw.line(self.layar, (255, 255, 0), rect.topleft, rect.bottomright, 3)
                pygame.draw.line(self.layar, (255, 255, 0), rect.topright, rect.bottomleft, 3)

    # Menggambar bagian atas layar berisi sisa ranjau, waktu, dan status
    def _gambar_header(self):
        sisa = JUMLAH_RANJAU - self.papan.jumlah_bendera
        teks_ranjau = self.font_sedang.render(f"RANJAU: {sisa}", True, WARNA_TEKS)
        teks_waktu = self.font_sedang.render(f"WAKTU: {self.waktu_berjalan()}", True, WARNA_TEKS)
        self.layar.blit(teks_ranjau, (14, 14))
        self.layar.blit(teks_waktu, teks_waktu.get_rect(topright=(LEBAR_LAYAR - 14, 14)))

        if self.status == "menang":
            pesan, warna = "KAMU MENANG! Tekan R untuk main lagi", WARNA_MENANG
        elif self.status == "kalah":
            pesan, warna = "KAMU KALAH! Tekan R untuk mengulang", WARNA_KALAH
        else:
            pesan, warna = "Klik kiri: buka | Klik kanan: bendera | R: ulang", (170, 175, 190)
        teks_status = self.font_kecil.render(pesan, True, warna)
        self.layar.blit(teks_status, teks_status.get_rect(center=(LEBAR_LAYAR // 2, 56)))

    # Menggambar seluruh elemen ke layar
    def gambar(self):
        self.layar.fill(WARNA_LATAR)
        self._gambar_header()
        for r in range(JUMLAH_BARIS):
            for c in range(JUMLAH_KOLOM):
                self._gambar_sel(r, c)
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
    game = GameMinesweeper()
    game.jalankan()


if __name__ == "__main__":
    main()
