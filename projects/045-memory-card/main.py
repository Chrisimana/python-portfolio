import pygame
import random
import math
import json
import os
import sys

LEBAR_LAYAR = 640
TINGGI_LAYAR = 740
TINGGI_HEADER = 96
MARGIN = 24
JARAK_KARTU = 12
FPS = 60

WAKTU_TUNGGU_SALAH = 800  # milidetik kartu yang tidak cocok ditampilkan sebelum ditutup kembali
KECEPATAN_BALIK = 5.0     # kecepatan animasi pembalikan kartu per detik

FILE_SKOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skor_terbaik.json")

WARNA_LATAR = (28, 32, 44)
WARNA_BELAKANG = (70, 90, 150)
WARNA_BELAKANG_POLA = (95, 118, 185)
WARNA_DEPAN = (245, 243, 236)
WARNA_COCOK = (200, 232, 205)
WARNA_TEKS = (238, 238, 244)
WARNA_TEKS_REDUP = (150, 155, 175)
WARNA_MENANG = (120, 215, 140)

WARNA_SIMBOL = [(215, 60, 60), (50, 105, 210), (40, 160, 90)]
BENTUK_SIMBOL = ["lingkaran", "persegi", "segitiga", "belah_ketupat", "bintang", "plus"]

# Ukuran grid untuk setiap tingkat kesulitan
TINGKAT = {
    "1": ("Mudah", 4, 4),
    "2": ("Sedang", 5, 4),
    "3": ("Sulit", 6, 6),
}


# Menggambar simbol kartu di dalam sebuah area
def gambar_simbol(layar, bentuk, warna, rect):
    pusat = rect.center
    r = int(min(rect.width, rect.height) * 0.30)

    if bentuk == "lingkaran":
        pygame.draw.circle(layar, warna, pusat, r)
    elif bentuk == "persegi":
        pygame.draw.rect(layar, warna, pygame.Rect(0, 0, r * 2, r * 2).move(pusat[0] - r, pusat[1] - r), border_radius=4)
    elif bentuk == "segitiga":
        titik = [(pusat[0], pusat[1] - r), (pusat[0] - r, pusat[1] + r * 0.8), (pusat[0] + r, pusat[1] + r * 0.8)]
        pygame.draw.polygon(layar, warna, titik)
    elif bentuk == "belah_ketupat":
        titik = [(pusat[0], pusat[1] - r), (pusat[0] + r, pusat[1]), (pusat[0], pusat[1] + r), (pusat[0] - r, pusat[1])]
        pygame.draw.polygon(layar, warna, titik)
    elif bentuk == "bintang":
        titik = []
        for i in range(10):
            sudut = -math.pi / 2 + i * math.pi / 5
            jari = r * 1.15 if i % 2 == 0 else r * 0.5
            titik.append((pusat[0] + jari * math.cos(sudut), pusat[1] + jari * math.sin(sudut)))
        pygame.draw.polygon(layar, warna, titik)
    elif bentuk == "plus":
        tebal = max(4, r // 2)
        pygame.draw.rect(layar, warna, pygame.Rect(pusat[0] - tebal, pusat[1] - r, tebal * 2, r * 2))
        pygame.draw.rect(layar, warna, pygame.Rect(pusat[0] - r, pusat[1] - tebal, r * 2, tebal * 2))


# Merepresentasikan satu kartu beserta status dan animasi pembaliknya
class Kartu:
    def __init__(self, id_pasangan, bentuk, warna, rect):
        self.id_pasangan = id_pasangan
        self.bentuk = bentuk
        self.warna = warna
        self.rect = rect
        self.terbuka = False
        self.cocok = False
        self.animasi = 0.0

    # Memperbarui progres animasi pembalikan menuju status terbuka atau tertutup
    def perbarui(self, dt):
        target = 1.0 if (self.terbuka or self.cocok) else 0.0
        if self.animasi < target:
            self.animasi = min(target, self.animasi + dt * KECEPATAN_BALIK)
        elif self.animasi > target:
            self.animasi = max(target, self.animasi - dt * KECEPATAN_BALIK)


# Mengelola penyimpanan skor terbaik per tingkat kesulitan
class PenyimpanSkor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._muat()

    def _muat(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _simpan(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=2)
        except OSError:
            pass

    # Mengambil skor terbaik untuk tingkat tertentu, None jika belum ada
    def ambil(self, tingkat):
        return self.data.get(tingkat)

    # Menyimpan skor baru jika lebih baik, mengembalikan True jika rekor baru
    def perbarui(self, tingkat, langkah, waktu):
        lama = self.data.get(tingkat)
        if lama is None or (langkah, waktu) < (lama["langkah"], lama["waktu"]):
            self.data[tingkat] = {"langkah": langkah, "waktu": waktu}
            self._simpan()
            return True
        return False


# Mengatur tampilan, input, dan alur permainan Memory Card
class GameMemory:
    def __init__(self, file_skor=FILE_SKOR):
        pygame.init()
        pygame.display.set_caption("Memory Card")
        self.layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
        self.jam = pygame.time.Clock()
        self.font_besar = pygame.font.Font(None, 56)
        self.font_sedang = pygame.font.Font(None, 30)
        self.font_kecil = pygame.font.Font(None, 22)

        self.penyimpan = PenyimpanSkor(file_skor)
        self.kunci_tingkat = "1"
        self.mulai_baru()

    # Menyusun kartu sesuai tingkat kesulitan dan mengacaknya
    def mulai_baru(self, kunci_tingkat=None):
        if kunci_tingkat:
            self.kunci_tingkat = kunci_tingkat

        _, kolom, baris = TINGKAT[self.kunci_tingkat]
        jumlah_pasangan = kolom * baris // 2

        kombinasi = [(b, w) for b in BENTUK_SIMBOL for w in WARNA_SIMBOL]
        random.shuffle(kombinasi)
        terpilih = kombinasi[:jumlah_pasangan]

        daftar = []
        for id_pasangan, (bentuk, warna) in enumerate(terpilih):
            daftar.append((id_pasangan, bentuk, warna))
            daftar.append((id_pasangan, bentuk, warna))
        random.shuffle(daftar)

        lebar_area = LEBAR_LAYAR - MARGIN * 2
        tinggi_area = TINGGI_LAYAR - TINGGI_HEADER - MARGIN
        ukuran = min(
            (lebar_area - JARAK_KARTU * (kolom - 1)) // kolom,
            (tinggi_area - JARAK_KARTU * (baris - 1)) // baris,
        )
        total_lebar = ukuran * kolom + JARAK_KARTU * (kolom - 1)
        total_tinggi = ukuran * baris + JARAK_KARTU * (baris - 1)
        awal_x = (LEBAR_LAYAR - total_lebar) // 2
        awal_y = TINGGI_HEADER + (tinggi_area - total_tinggi) // 2

        self.kartu = []
        for indeks, (id_pasangan, bentuk, warna) in enumerate(daftar):
            r, c = divmod(indeks, kolom)
            rect = pygame.Rect(
                awal_x + c * (ukuran + JARAK_KARTU),
                awal_y + r * (ukuran + JARAK_KARTU),
                ukuran, ukuran,
            )
            self.kartu.append(Kartu(id_pasangan, bentuk, warna, rect))

        self.terpilih = []
        self.langkah = 0
        self.jumlah_cocok = 0
        self.tutup_pada = None
        self.waktu_mulai = None
        self.waktu_akhir = None
        self.rekor_baru = False

    # Menghitung waktu bermain dalam detik, dimulai saat kartu pertama dibuka
    def waktu_berjalan(self):
        if self.waktu_mulai is None:
            return 0
        akhir = self.waktu_akhir if self.waktu_akhir is not None else pygame.time.get_ticks()
        return (akhir - self.waktu_mulai) // 1000

    # Mengecek apakah seluruh pasangan sudah ditemukan
    def selesai(self):
        return self.jumlah_cocok == len(self.kartu) // 2

    # Memproses klik pada sebuah kartu
    def tangani_klik(self, posisi):
        if self.tutup_pada is not None or self.selesai():
            return

        for kartu in self.kartu:
            if kartu.rect.collidepoint(posisi) and not kartu.terbuka and not kartu.cocok:
                if self.waktu_mulai is None:
                    self.waktu_mulai = pygame.time.get_ticks()

                kartu.terbuka = True
                self.terpilih.append(kartu)

                if len(self.terpilih) == 2:
                    self.langkah += 1
                    self._periksa_pasangan()
                break

    # Membandingkan dua kartu yang terbuka
    def _periksa_pasangan(self):
        pertama, kedua = self.terpilih
        if pertama.id_pasangan == kedua.id_pasangan:
            pertama.cocok = kedua.cocok = True
            pertama.terbuka = kedua.terbuka = False
            self.terpilih = []
            self.jumlah_cocok += 1

            if self.selesai():
                self.waktu_akhir = pygame.time.get_ticks()
                self.rekor_baru = self.penyimpan.perbarui(
                    self.kunci_tingkat, self.langkah, self.waktu_berjalan()
                )
        else:
            self.tutup_pada = pygame.time.get_ticks() + WAKTU_TUNGGU_SALAH

    # Menangani seluruh event Pygame
    def tangani_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.tangani_klik(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.mulai_baru()
            elif event.unicode in TINGKAT:
                self.mulai_baru(event.unicode)
        return True

    # Memperbarui animasi kartu dan menutup kembali kartu yang tidak cocok setelah jeda
    def perbarui(self, dt):
        if self.tutup_pada is not None and pygame.time.get_ticks() >= self.tutup_pada:
            for kartu in self.terpilih:
                kartu.terbuka = False
            self.terpilih = []
            self.tutup_pada = None

        for kartu in self.kartu:
            kartu.perbarui(dt)

    # Menggambar satu kartu dengan efek pembalikan
    def _gambar_kartu(self, kartu):
        if kartu.animasi < 0.5:
            skala = 1 - kartu.animasi * 2
            tampil_depan = False
        else:
            skala = (kartu.animasi - 0.5) * 2
            tampil_depan = True

        lebar = max(2, int(kartu.rect.width * skala))
        rect = pygame.Rect(0, 0, lebar, kartu.rect.height)
        rect.center = kartu.rect.center

        if tampil_depan:
            warna = WARNA_COCOK if kartu.cocok else WARNA_DEPAN
            pygame.draw.rect(self.layar, warna, rect, border_radius=10)
            if skala > 0.6:
                gambar_simbol(self.layar, kartu.bentuk, kartu.warna, kartu.rect)
        else:
            pygame.draw.rect(self.layar, WARNA_BELAKANG, rect, border_radius=10)
            if skala > 0.6:
                dalam = kartu.rect.inflate(-kartu.rect.width * 0.35, -kartu.rect.height * 0.35)
                pygame.draw.rect(self.layar, WARNA_BELAKANG_POLA, dalam, 3, border_radius=6)

    # Menggambar bagian atas layar berisi judul, statistik, dan skor terbaik
    def _gambar_header(self):
        nama, kolom, baris = TINGKAT[self.kunci_tingkat]
        judul = self.font_sedang.render(f"MEMORY CARD - {nama} ({kolom}x{baris})", True, WARNA_TEKS)
        self.layar.blit(judul, (MARGIN, 18))

        info = self.font_sedang.render(
            f"Langkah: {self.langkah}    Waktu: {self.waktu_berjalan()}s", True, WARNA_TEKS
        )
        self.layar.blit(info, (MARGIN, 52))

        terbaik = self.penyimpan.ambil(self.kunci_tingkat)
        teks_terbaik = "Terbaik: -" if terbaik is None else f"Terbaik: {terbaik['langkah']} langkah, {terbaik['waktu']}s"
        gambar_terbaik = self.font_kecil.render(teks_terbaik, True, WARNA_TEKS_REDUP)
        self.layar.blit(gambar_terbaik, gambar_terbaik.get_rect(topright=(LEBAR_LAYAR - MARGIN, 22)))

        petunjuk = self.font_kecil.render("1/2/3: tingkat | R: ulang", True, WARNA_TEKS_REDUP)
        self.layar.blit(petunjuk, petunjuk.get_rect(topright=(LEBAR_LAYAR - MARGIN, 56)))

    # Menggambar lapisan kemenangan di atas papan
    def _gambar_menang(self):
        if not self.selesai():
            return

        lapisan = pygame.Surface((LEBAR_LAYAR, TINGGI_LAYAR), pygame.SRCALPHA)
        lapisan.fill((10, 12, 20, 190))
        self.layar.blit(lapisan, (0, 0))

        judul = self.font_besar.render("SELESAI!", True, WARNA_MENANG)
        hasil = self.font_sedang.render(
            f"{self.langkah} langkah dalam {self.waktu_berjalan()} detik", True, WARNA_TEKS
        )
        self.layar.blit(judul, judul.get_rect(center=(LEBAR_LAYAR // 2, TINGGI_LAYAR // 2 - 40)))
        self.layar.blit(hasil, hasil.get_rect(center=(LEBAR_LAYAR // 2, TINGGI_LAYAR // 2 + 8)))

        if self.rekor_baru:
            rekor = self.font_sedang.render("Rekor baru!", True, (240, 200, 80))
            self.layar.blit(rekor, rekor.get_rect(center=(LEBAR_LAYAR // 2, TINGGI_LAYAR // 2 + 44)))

        ulang = self.font_kecil.render("Tekan R untuk main lagi", True, WARNA_TEKS_REDUP)
        self.layar.blit(ulang, ulang.get_rect(center=(LEBAR_LAYAR // 2, TINGGI_LAYAR // 2 + 84)))

    # Menggambar seluruh elemen ke layar
    def gambar(self):
        self.layar.fill(WARNA_LATAR)
        self._gambar_header()
        for kartu in self.kartu:
            self._gambar_kartu(kartu)
        self._gambar_menang()
        pygame.display.flip()

    # Menjalankan game loop utama
    def jalankan(self):
        berjalan = True
        while berjalan:
            dt = self.jam.tick(FPS) / 1000

            for event in pygame.event.get():
                if not self.tangani_event(event):
                    berjalan = False

            self.perbarui(dt)
            self.gambar()

        pygame.quit()
        sys.exit()


def main():
    game = GameMemory()
    game.jalankan()


if __name__ == "__main__":
    main()
