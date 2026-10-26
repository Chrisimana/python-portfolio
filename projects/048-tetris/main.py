import pygame
import random
import sys

KOLOM = 10
BARIS = 20
UKURAN = 30
LEBAR_PANEL = 200
LEBAR_PAPAN = KOLOM * UKURAN
LEBAR_LAYAR = LEBAR_PAPAN + LEBAR_PANEL
TINGGI_LAYAR = BARIS * UKURAN
FPS = 60

WARNA_LATAR = (18, 20, 28)
WARNA_PAPAN = (26, 29, 40)
WARNA_GARIS = (40, 44, 58)
WARNA_TEKS = (235, 235, 240)
WARNA_TEKS_REDUP = (150, 155, 170)

# Bentuk setiap balok dalam bentuk matriks, angka 1 menandakan sel terisi
BENTUK = {
    "I": [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    "S": [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    "Z": [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
    "J": [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    "L": [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
}

WARNA_BALOK = {
    "I": (0, 200, 220),
    "O": (235, 200, 40),
    "T": (170, 80, 200),
    "S": (80, 200, 90),
    "Z": (220, 70, 70),
    "J": (70, 100, 220),
    "L": (235, 140, 40),
}

POIN_BARIS = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}

# Pergeseran yang dicoba saat rotasi terhalang dinding atau balok lain (wall kick sederhana)
GESER_ROTASI = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]


# Merepresentasikan satu balok yang sedang jatuh
class Balok:
    def __init__(self, nama):
        self.nama = nama
        self.matriks = [baris[:] for baris in BENTUK[nama]]
        self.x = (KOLOM - len(self.matriks[0])) // 2
        self.y = 0

    # Menghasilkan koordinat setiap sel terisi pada papan
    def sel_terisi(self, matriks=None, x=None, y=None):
        matriks = self.matriks if matriks is None else matriks
        x = self.x if x is None else x
        y = self.y if y is None else y
        for r, baris in enumerate(matriks):
            for c, nilai in enumerate(baris):
                if nilai:
                    yield x + c, y + r

    # Mengembalikan matriks hasil rotasi 90 derajat searah jarum jam
    def matriks_rotasi(self):
        return [list(baris) for baris in zip(*self.matriks[::-1])]


# Mengelola grid papan dan seluruh aturan tumbukan
class Papan:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [[None] * KOLOM for _ in range(BARIS)]

    # Mengecek apakah posisi balok valid (di dalam papan dan tidak menimpa sel lain)
    def valid(self, balok, matriks=None, x=None, y=None):
        for sx, sy in balok.sel_terisi(matriks, x, y):
            if sx < 0 or sx >= KOLOM or sy >= BARIS:
                return False
            if sy >= 0 and self.grid[sy][sx] is not None:
                return False
        return True

    # Mengunci balok ke dalam grid
    def kunci(self, balok):
        for sx, sy in balok.sel_terisi():
            if 0 <= sy < BARIS:
                self.grid[sy][sx] = balok.nama

    # Menghapus baris yang penuh dan mengembalikan jumlahnya
    def hapus_baris_penuh(self):
        baris_tersisa = [baris for baris in self.grid if any(sel is None for sel in baris)]
        jumlah_hapus = BARIS - len(baris_tersisa)
        for _ in range(jumlah_hapus):
            baris_tersisa.insert(0, [None] * KOLOM)
        self.grid = baris_tersisa
        return jumlah_hapus


# Mengatur seluruh alur permainan Tetris, termasuk tampilan dan input
class GameTetris:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
        self.jam = pygame.time.Clock()
        self.font_besar = pygame.font.Font(None, 44)
        self.font_sedang = pygame.font.Font(None, 30)
        self.font_kecil = pygame.font.Font(None, 22)

        pygame.key.set_repeat(170, 55)
        self.skor_tertinggi = 0
        self.papan = Papan()
        self.mulai_baru()

    # Menyiapkan permainan baru
    def mulai_baru(self):
        self.papan.reset()
        self.kantong = []
        self.skor = 0
        self.baris_total = 0
        self.level = 1
        self.status = "main"  # main, jeda, selesai
        self.waktu_jatuh = 0
        self.tombol_aktif = set()
        self.berikutnya = self._ambil_nama_berikutnya()
        self.munculkan_balok()

    # Mengambil nama balok berikutnya memakai sistem kantong 7 balok agar distribusi merata
    def _ambil_nama_berikutnya(self):
        if not self.kantong:
            self.kantong = list(BENTUK.keys())
            random.shuffle(self.kantong)
        return self.kantong.pop()

    # Memunculkan balok baru di bagian atas papan
    def munculkan_balok(self):
        self.balok = Balok(self.berikutnya)
        self.berikutnya = self._ambil_nama_berikutnya()

        if not self.papan.valid(self.balok):
            self.status = "selesai"
            self.skor_tertinggi = max(self.skor_tertinggi, self.skor)

    # Interval jatuh otomatis dalam milidetik, semakin cepat seiring naiknya level
    def interval_jatuh(self):
        return max(80, 800 - (self.level - 1) * 70)

    # Menggeser balok, mengembalikan True jika berhasil
    def geser(self, dx, dy):
        if self.papan.valid(self.balok, x=self.balok.x + dx, y=self.balok.y + dy):
            self.balok.x += dx
            self.balok.y += dy
            return True
        return False

    # Memutar balok dengan mencoba beberapa pergeseran jika terhalang
    def rotasi(self):
        if self.balok.nama == "O":
            return

        matriks_baru = self.balok.matriks_rotasi()
        for dx, dy in GESER_ROTASI:
            if self.papan.valid(self.balok, matriks_baru, self.balok.x + dx, self.balok.y + dy):
                self.balok.matriks = matriks_baru
                self.balok.x += dx
                self.balok.y += dy
                return

    # Mengunci balok, menghapus baris penuh, menambah skor, lalu memunculkan balok baru
    def kunci_balok(self):
        self.papan.kunci(self.balok)
        jumlah = self.papan.hapus_baris_penuh()

        self.skor += POIN_BARIS[jumlah] * self.level
        self.baris_total += jumlah
        self.level = 1 + self.baris_total // 10
        self.munculkan_balok()

    # Menjatuhkan balok satu baris, atau mengunci jika sudah menyentuh dasar
    def langkah_jatuh(self, dari_pemain=False):
        if self.geser(0, 1):
            if dari_pemain:
                self.skor += 1
        else:
            self.kunci_balok()

    # Menjatuhkan balok langsung ke posisi terbawah
    def jatuh_langsung(self):
        jarak = 0
        while self.geser(0, 1):
            jarak += 1
        self.skor += jarak * 2
        self.kunci_balok()

    # Menghitung posisi y bayangan (ghost) tempat balok akan mendarat
    def posisi_bayangan(self):
        y = self.balok.y
        while self.papan.valid(self.balok, y=y + 1):
            y += 1
        return y

    # Menangani seluruh event keyboard dan jendela
    def tangani_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYUP:
            self.tombol_aktif.discard(event.key)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.mulai_baru()
                return True
            if event.key == pygame.K_p and self.status in ("main", "jeda"):
                self.status = "jeda" if self.status == "main" else "main"
                return True

            if self.status != "main":
                return True

            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.geser(-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.geser(1, 0)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.langkah_jatuh(dari_pemain=True)
            elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                # Rotasi dan jatuh langsung hanya diproses sekali per penekanan, bukan saat tombol ditahan
                if event.key not in self.tombol_aktif:
                    if event.key == pygame.K_SPACE:
                        self.jatuh_langsung()
                    else:
                        self.rotasi()

            self.tombol_aktif.add(event.key)

        return True

    # Memperbarui logika jatuh otomatis berdasarkan waktu yang berlalu
    def perbarui(self, dt):
        if self.status != "main":
            return

        self.waktu_jatuh += dt
        while self.waktu_jatuh >= self.interval_jatuh() and self.status == "main":
            self.waktu_jatuh -= self.interval_jatuh()
            self.langkah_jatuh()

    # Menggambar satu kotak balok pada koordinat piksel tertentu
    def _gambar_kotak(self, x, y, warna, ukuran=UKURAN, transparan=False):
        rect = pygame.Rect(x, y, ukuran, ukuran).inflate(-2, -2)
        if transparan:
            pygame.draw.rect(self.layar, warna, rect, 2, border_radius=4)
            return

        pygame.draw.rect(self.layar, warna, rect, border_radius=4)
        terang = tuple(min(255, nilai + 45) for nilai in warna)
        pygame.draw.line(self.layar, terang, rect.topleft, rect.topright, 2)
        pygame.draw.line(self.layar, terang, rect.topleft, rect.bottomleft, 2)

    # Menggambar papan, balok terkunci, bayangan, dan balok aktif
    def _gambar_papan(self):
        pygame.draw.rect(self.layar, WARNA_PAPAN, (0, 0, LEBAR_PAPAN, TINGGI_LAYAR))
        for c in range(KOLOM + 1):
            pygame.draw.line(self.layar, WARNA_GARIS, (c * UKURAN, 0), (c * UKURAN, TINGGI_LAYAR))
        for r in range(BARIS + 1):
            pygame.draw.line(self.layar, WARNA_GARIS, (0, r * UKURAN), (LEBAR_PAPAN, r * UKURAN))

        for r in range(BARIS):
            for c in range(KOLOM):
                nama = self.papan.grid[r][c]
                if nama:
                    self._gambar_kotak(c * UKURAN, r * UKURAN, WARNA_BALOK[nama])

        if self.status == "selesai":
            return

        y_bayangan = self.posisi_bayangan()
        for sx, sy in self.balok.sel_terisi(y=y_bayangan):
            if sy >= 0:
                self._gambar_kotak(sx * UKURAN, sy * UKURAN, WARNA_BALOK[self.balok.nama], transparan=True)

        for sx, sy in self.balok.sel_terisi():
            if sy >= 0:
                self._gambar_kotak(sx * UKURAN, sy * UKURAN, WARNA_BALOK[self.balok.nama])

    # Menggambar teks berlabel pada panel samping
    def _gambar_info(self, label, nilai, y):
        teks_label = self.font_kecil.render(label, True, WARNA_TEKS_REDUP)
        teks_nilai = self.font_sedang.render(str(nilai), True, WARNA_TEKS)
        self.layar.blit(teks_label, (LEBAR_PAPAN + 20, y))
        self.layar.blit(teks_nilai, (LEBAR_PAPAN + 20, y + 20))

    # Menggambar panel samping berisi skor, level, balok berikutnya, dan petunjuk kontrol
    def _gambar_panel(self):
        pygame.draw.rect(self.layar, WARNA_LATAR, (LEBAR_PAPAN, 0, LEBAR_PANEL, TINGGI_LAYAR))

        self._gambar_info("SKOR", self.skor, 20)
        self._gambar_info("REKOR", self.skor_tertinggi, 80)
        self._gambar_info("LEVEL", self.level, 140)
        self._gambar_info("BARIS", self.baris_total, 200)

        teks_next = self.font_kecil.render("BERIKUTNYA", True, WARNA_TEKS_REDUP)
        self.layar.blit(teks_next, (LEBAR_PAPAN + 20, 265))

        kotak = pygame.Rect(LEBAR_PAPAN + 20, 290, 150, 90)
        pygame.draw.rect(self.layar, WARNA_PAPAN, kotak, border_radius=6)
        matriks = BENTUK[self.berikutnya]
        ukuran_kecil = 24
        lebar_bentuk = len(matriks[0]) * ukuran_kecil
        tinggi_bentuk = len(matriks) * ukuran_kecil
        awal_x = kotak.centerx - lebar_bentuk // 2
        awal_y = kotak.centery - tinggi_bentuk // 2
        for r, baris in enumerate(matriks):
            for c, nilai in enumerate(baris):
                if nilai:
                    self._gambar_kotak(
                        awal_x + c * ukuran_kecil, awal_y + r * ukuran_kecil,
                        WARNA_BALOK[self.berikutnya], ukuran_kecil,
                    )

        petunjuk = [
            "Panah kiri/kanan: geser",
            "Panah atas: putar",
            "Panah bawah: turun",
            "Spasi: jatuh langsung",
            "P: jeda   R: ulang",
        ]
        for i, baris in enumerate(petunjuk):
            teks = self.font_kecil.render(baris, True, WARNA_TEKS_REDUP)
            self.layar.blit(teks, (LEBAR_PAPAN + 14, 420 + i * 24))

    # Menggambar lapisan pesan untuk kondisi jeda dan game over
    def _gambar_overlay(self):
        if self.status == "main":
            return

        lapisan = pygame.Surface((LEBAR_PAPAN, TINGGI_LAYAR), pygame.SRCALPHA)
        lapisan.fill((0, 0, 0, 160))
        self.layar.blit(lapisan, (0, 0))

        judul = "JEDA" if self.status == "jeda" else "GAME OVER"
        sub = "Tekan P untuk lanjut" if self.status == "jeda" else "Tekan R untuk main lagi"

        teks_judul = self.font_besar.render(judul, True, WARNA_TEKS)
        teks_sub = self.font_kecil.render(sub, True, WARNA_TEKS_REDUP)
        self.layar.blit(teks_judul, teks_judul.get_rect(center=(LEBAR_PAPAN // 2, TINGGI_LAYAR // 2 - 15)))
        self.layar.blit(teks_sub, teks_sub.get_rect(center=(LEBAR_PAPAN // 2, TINGGI_LAYAR // 2 + 20)))

    # Menggambar seluruh elemen ke layar
    def gambar(self):
        self.layar.fill(WARNA_LATAR)
        self._gambar_papan()
        self._gambar_panel()
        self._gambar_overlay()
        pygame.display.flip()

    # Menjalankan game loop utama
    def jalankan(self):
        berjalan = True
        while berjalan:
            dt = self.jam.tick(FPS)

            for event in pygame.event.get():
                if not self.tangani_event(event):
                    berjalan = False

            self.perbarui(dt)
            self.gambar()

        pygame.quit()
        sys.exit()


def main():
    game = GameTetris()
    game.jalankan()


if __name__ == "__main__":
    main()
