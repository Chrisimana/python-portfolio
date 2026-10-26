import pygame
import random
import sys
import math
from collections import Counter

LEBAR_LAYAR = 480
TINGGI_LAYAR = 720
FPS = 60

PANJANG_KATA = 5
PERCOBAAN_MAKS = 6
UKURAN_KOTAK = 56
JARAK_KOTAK = 6
POSISI_Y_GRID = 84

BARIS_KEYBOARD = [list("QWERTYUIOP"), list("ASDFGHJKL"), ["ENTER"] + list("ZXCVBNM") + ["HAPUS"]]
LEBAR_TOMBOL = 40
LEBAR_TOMBOL_KHUSUS = 64
TINGGI_TOMBOL = 52
JARAK_TOMBOL = 6
POSISI_Y_KEYBOARD = 524

WARNA_LATAR = (18, 18, 20)
WARNA_KOTAK_KOSONG = (18, 18, 20)
WARNA_GARIS_KOTAK = (65, 65, 70)
WARNA_GARIS_KOTAK_AKTIF = (130, 130, 138)
WARNA_TOMBOL = (130, 131, 134)
WARNA_TEKS = (240, 240, 240)
WARNA_TEKS_REDUP = (150, 150, 158)
WARNA_STATUS = {
    "benar": (83, 141, 78),
    "ada": (181, 159, 59),
    "salah": (58, 58, 60),
}

# Urutan prioritas status untuk pewarnaan keyboard
PRIORITAS = {"salah": 1, "ada": 2, "benar": 3}

# Daftar kata jawaban (5 huruf, Bahasa Indonesia)
DAFTAR_KATA = [
    "pintu", "makan", "rumah", "kerja", "bunga", "malam", "siang", "minum", "bukit", "pasar",
    "mobil", "jalan", "hujan", "angin", "angka", "benda", "cinta", "dunia", "empat", "hitam",
    "putih", "merah", "kapal", "pulau", "sawah", "kebun", "tanah", "udara", "mulut", "betis",
    "tidur", "jatuh", "turun", "besar", "kecil", "cepat", "pelan", "mudah", "sulit", "murah",
    "mahal", "bagus", "buruk", "indah", "bodoh", "sedih", "marah", "takut", "malas", "rajin",
    "sakit", "sehat", "lapar", "murid", "dosen", "ujian", "tugas", "nilai", "kelas", "papan",
    "kursi", "kasur", "gelas", "garpu", "pisau", "dapur", "kamar", "teras", "kunci", "lampu",
    "kabel", "telur", "bebek", "udang", "sayur", "jeruk", "nanas", "salak", "garam", "kecap",
    "cabai", "beras", "bubur", "bakso", "sirup", "putra", "putri", "bapak", "kakak", "nenek",
    "kakek", "paman", "teman", "warga", "danau", "hutan", "pasir", "bulan", "surya", "petir",
    "kilat", "salju", "musim", "tahun", "pekan", "waktu", "detik", "menit", "jarum", "tiket",
    "harga", "bayar", "kirim", "surat", "kabar", "kisah", "musik", "drama", "lukis", "warna",
    "bulat", "kotak", "garis", "titik", "tujuh", "pikir", "ingat", "mimpi", "harap", "surga",
    "hukum", "benar", "salah", "jujur", "dusta", "damai", "musuh", "kawan", "bantu", "minta",
    "ambil", "tarik", "buang", "lihat", "tanya", "jawab", "tulis", "hapus", "tutup", "mulai",
    "akhir", "dekat", "depan", "kanan", "bawah", "panas", "sejuk", "basah", "licin", "kasar",
    "halus", "tajam", "keras", "lunak", "berat", "padat", "penuh", "ramai", "gelap", "silau",
    "harum", "busuk", "manis", "pahit", "pedas", "gurih", "segar", "layar", "mesin", "motor",
]


# Mengevaluasi sebuah tebakan terhadap kata target, mengembalikan daftar status per huruf
def evaluasi_tebakan(tebakan, target):
    hasil = ["salah"] * len(target)
    sisa_huruf = Counter()

    # Tahap pertama: tandai huruf yang tepat posisinya, hitung huruf target yang belum terpakai
    for i, huruf in enumerate(tebakan):
        if huruf == target[i]:
            hasil[i] = "benar"
        else:
            sisa_huruf[target[i]] += 1

    # Tahap kedua: tandai huruf yang ada di kata namun salah posisi, dibatasi jumlah huruf yang tersisa
    for i, huruf in enumerate(tebakan):
        if hasil[i] != "benar" and sisa_huruf[huruf] > 0:
            hasil[i] = "ada"
            sisa_huruf[huruf] -= 1

    return hasil


# Mengelola state dan aturan permainan Wordle
class PermainanWordle:
    def __init__(self):
        self.dimainkan = 0
        self.menang = 0
        self.streak = 0
        self.mulai_baru()

    # Menyiapkan permainan baru dengan kata target acak
    def mulai_baru(self):
        self.target = random.choice(DAFTAR_KATA).upper()
        self.tebakan = []
        self.hasil = []
        self.saat_ini = ""
        self.status = "main"  # main, menang, kalah
        self.status_huruf = {}

    # Menambahkan satu huruf ke tebakan yang sedang diketik
    def ketik(self, huruf):
        if self.status == "main" and len(self.saat_ini) < PANJANG_KATA and huruf.isalpha():
            self.saat_ini += huruf.upper()

    # Menghapus huruf terakhir pada tebakan yang sedang diketik
    def hapus(self):
        if self.status == "main":
            self.saat_ini = self.saat_ini[:-1]

    # Mengirim tebakan, mengembalikan None jika berhasil atau pesan error jika gagal
    def kirim(self):
        if self.status != "main":
            return None
        if len(self.saat_ini) < PANJANG_KATA:
            return "Huruf kurang"

        hasil = evaluasi_tebakan(self.saat_ini, self.target)
        self.tebakan.append(self.saat_ini)
        self.hasil.append(hasil)

        for huruf, nilai in zip(self.saat_ini, hasil):
            lama = self.status_huruf.get(huruf)
            if lama is None or PRIORITAS[nilai] > PRIORITAS[lama]:
                self.status_huruf[huruf] = nilai

        if self.saat_ini == self.target:
            self.status = "menang"
            self.dimainkan += 1
            self.menang += 1
            self.streak += 1
        elif len(self.tebakan) >= PERCOBAAN_MAKS:
            self.status = "kalah"
            self.dimainkan += 1
            self.streak = 0

        self.saat_ini = ""
        return None


# Mengatur tampilan dan input permainan Wordle
class GameWordle:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Wordle Clone")
        self.layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
        self.jam = pygame.time.Clock()
        self.font_judul = pygame.font.Font(None, 54)
        self.font_kotak = pygame.font.Font(None, 48)
        self.font_tombol = pygame.font.Font(None, 26)
        self.font_kecil = pygame.font.Font(None, 24)

        self.permainan = PermainanWordle()
        self.pesan = ""
        self.pesan_hingga = 0
        self.getar_hingga = 0
        self.tombol_keyboard = self._susun_keyboard()

    # Menghitung posisi seluruh tombol keyboard di layar
    def _susun_keyboard(self):
        daftar = []
        for indeks_baris, baris in enumerate(BARIS_KEYBOARD):
            lebar_tombol = [LEBAR_TOMBOL_KHUSUS if len(k) > 1 else LEBAR_TOMBOL for k in baris]
            total = sum(lebar_tombol) + JARAK_TOMBOL * (len(baris) - 1)
            x = (LEBAR_LAYAR - total) // 2
            y = POSISI_Y_KEYBOARD + indeks_baris * (TINGGI_TOMBOL + JARAK_TOMBOL)

            for kunci, lebar in zip(baris, lebar_tombol):
                daftar.append((kunci, pygame.Rect(x, y, lebar, TINGGI_TOMBOL)))
                x += lebar + JARAK_TOMBOL
        return daftar

    # Menampilkan pesan singkat di layar selama beberapa detik
    def tampilkan_pesan(self, teks, durasi=1800):
        self.pesan = teks
        self.pesan_hingga = pygame.time.get_ticks() + durasi

    # Memproses penekanan tombol (dari keyboard fisik maupun keyboard di layar)
    def proses_kunci(self, kunci):
        if kunci == "ENTER":
            if self.permainan.status != "main":
                self.permainan.mulai_baru()
                return
            kesalahan = self.permainan.kirim()
            if kesalahan:
                self.tampilkan_pesan(kesalahan)
                self.getar_hingga = pygame.time.get_ticks() + 400
        elif kunci == "HAPUS":
            self.permainan.hapus()
        else:
            self.permainan.ketik(kunci)

    # Menangani seluruh event Pygame
    def tangani_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.proses_kunci("ENTER")
            elif event.key == pygame.K_BACKSPACE:
                self.proses_kunci("HAPUS")
            elif event.unicode and event.unicode.isalpha() and len(event.unicode) == 1:
                self.proses_kunci(event.unicode.upper())

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for kunci, rect in self.tombol_keyboard:
                if rect.collidepoint(event.pos):
                    self.proses_kunci(kunci)
                    break

        return True

    # Menggambar judul dan statistik singkat
    def _gambar_header(self):
        judul = self.font_judul.render("WORDLE", True, WARNA_TEKS)
        self.layar.blit(judul, judul.get_rect(center=(LEBAR_LAYAR // 2, 40)))
        pygame.draw.line(self.layar, WARNA_GARIS_KOTAK, (20, 70), (LEBAR_LAYAR - 20, 70), 1)

    # Menggambar satu kotak huruf
    def _gambar_kotak(self, rect, huruf, status):
        if status:
            pygame.draw.rect(self.layar, WARNA_STATUS[status], rect, border_radius=4)
        else:
            warna_garis = WARNA_GARIS_KOTAK_AKTIF if huruf else WARNA_GARIS_KOTAK
            pygame.draw.rect(self.layar, WARNA_KOTAK_KOSONG, rect)
            pygame.draw.rect(self.layar, warna_garis, rect, 2)

        if huruf:
            teks = self.font_kotak.render(huruf, True, WARNA_TEKS)
            self.layar.blit(teks, teks.get_rect(center=rect.center))

    # Menggambar seluruh grid 6x5 tebakan
    def _gambar_grid(self):
        total_lebar = PANJANG_KATA * UKURAN_KOTAK + (PANJANG_KATA - 1) * JARAK_KOTAK
        awal_x = (LEBAR_LAYAR - total_lebar) // 2
        sekarang = pygame.time.get_ticks()
        indeks_aktif = len(self.permainan.tebakan)

        for baris in range(PERCOBAAN_MAKS):
            geser = 0
            if baris == indeks_aktif and sekarang < self.getar_hingga:
                geser = int(math.sin(sekarang / 18) * 6)

            for kolom in range(PANJANG_KATA):
                rect = pygame.Rect(
                    awal_x + kolom * (UKURAN_KOTAK + JARAK_KOTAK) + geser,
                    POSISI_Y_GRID + baris * (UKURAN_KOTAK + JARAK_KOTAK),
                    UKURAN_KOTAK, UKURAN_KOTAK,
                )

                huruf, status = "", None
                if baris < len(self.permainan.tebakan):
                    huruf = self.permainan.tebakan[baris][kolom]
                    status = self.permainan.hasil[baris][kolom]
                elif baris == indeks_aktif and kolom < len(self.permainan.saat_ini):
                    huruf = self.permainan.saat_ini[kolom]

                self._gambar_kotak(rect, huruf, status)

    # Menggambar keyboard di layar beserta warna status setiap huruf
    def _gambar_keyboard(self):
        for kunci, rect in self.tombol_keyboard:
            status = self.permainan.status_huruf.get(kunci)
            warna = WARNA_STATUS[status] if status else WARNA_TOMBOL
            pygame.draw.rect(self.layar, warna, rect, border_radius=6)

            teks = self.font_tombol.render(kunci, True, WARNA_TEKS)
            self.layar.blit(teks, teks.get_rect(center=rect.center))

    # Menggambar pesan sementara dan hasil akhir permainan
    def _gambar_pesan(self):
        sekarang = pygame.time.get_ticks()
        y_pesan = POSISI_Y_GRID + PERCOBAAN_MAKS * (UKURAN_KOTAK + JARAK_KOTAK) + 6

        if self.permainan.status == "menang":
            teks = "Hebat! Kamu berhasil menebak."
            warna = WARNA_STATUS["benar"]
        elif self.permainan.status == "kalah":
            teks = f"Kata yang benar: {self.permainan.target}"
            warna = (230, 110, 110)
        elif sekarang < self.pesan_hingga:
            teks, warna = self.pesan, WARNA_TEKS
        else:
            teks, warna = "Ketik 5 huruf lalu tekan Enter", WARNA_TEKS_REDUP

        gambar_teks = self.font_kecil.render(teks, True, warna)
        self.layar.blit(gambar_teks, gambar_teks.get_rect(center=(LEBAR_LAYAR // 2, y_pesan + 12)))

        if self.permainan.status != "main":
            petunjuk = self.font_kecil.render("Tekan Enter untuk main lagi", True, WARNA_TEKS_REDUP)
            self.layar.blit(petunjuk, petunjuk.get_rect(center=(LEBAR_LAYAR // 2, y_pesan + 38)))

    # Menggambar statistik sesi di bagian bawah
    def _gambar_statistik(self):
        p = self.permainan
        teks = f"Menang {p.menang} dari {p.dimainkan} | Streak {p.streak}"
        gambar_teks = self.font_kecil.render(teks, True, WARNA_TEKS_REDUP)
        self.layar.blit(gambar_teks, gambar_teks.get_rect(center=(LEBAR_LAYAR // 2, TINGGI_LAYAR - 14)))

    # Menggambar seluruh elemen ke layar
    def gambar(self):
        self.layar.fill(WARNA_LATAR)
        self._gambar_header()
        self._gambar_grid()
        self._gambar_pesan()
        self._gambar_keyboard()
        self._gambar_statistik()
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
    game = GameWordle()
    game.jalankan()


if __name__ == "__main__":
    main()
