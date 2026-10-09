class FibonacciCalculator:
    @staticmethod
    def hitung_fibonacci(n):
        
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        
        deret = [0, 1]
        for i in range(2, n):
            suku_berikutnya = deret[i-1] + deret[i-2]
            deret.append(suku_berikutnya)
        
        return deret
    
    @staticmethod
    def hitung_statistik(deret):
        
        if not deret:
            return {}
        
        n = len(deret)
        total = sum(deret)
        rata_rata = total / n if n > 0 else 0
        
        # Hitung suku genap dan ganjil
        suku_genap = [x for x in deret if x % 2 == 0]
        suku_ganjil = [x for x in deret if x % 2 != 0]
        
        # Hitung rasio golden ratio
        rasio_terakhir = 0
        if n >= 2 and deret[-2] != 0:
            rasio_terakhir = deret[-1] / deret[-2]
        
        statistik = {
            'jumlah_suku': n,
            'total': total,
            'rata_rata': rata_rata,
            'suku_terbesar': max(deret) if n > 0 else 0,
            'suku_terkecil': min(deret) if n > 0 else 0,
            'jumlah_genap': len(suku_genap),
            'jumlah_ganjil': len(suku_ganjil),
            'rasio_terakhir': rasio_terakhir,
            'golden_ratio': 1.61803398875,
            'selisih_rasio': abs(rasio_terakhir - 1.61803398875)
        }
        
        return statistik
    
    @staticmethod
    def format_deret(deret):
        
        if not deret:
            return "Deret kosong"
        
        # Format dengan indeks
        format_dengan_indeks = []
        for i, suku in enumerate(deret):
            format_dengan_indeks.append(f"F({i}) = {suku}")
        
        # Bagi menjadi dua kolom untuk tampilan yang lebih baik
        tengah = len(format_dengan_indeks) // 2
        if len(format_dengan_indeks) % 2 != 0:
            tengah += 1
            
        kolom_kiri = format_dengan_indeks[:tengah]
        kolom_kanan = format_dengan_indeks[tengah:]
        
        # Cari panjang maksimum untuk perataan
        panjang_maks = max(len(item) for item in format_dengan_indeks) + 4
        
        # Gabungkan dalam dua kolom
        hasil_format = ""
        for i in range(max(len(kolom_kiri), len(kolom_kanan))):
            kiri = kolom_kiri[i] if i < len(kolom_kiri) else ""
            kanan = kolom_kanan[i] if i < len(kolom_kanan) else ""
            
            kiri_rapi = kiri.ljust(panjang_maks)
            hasil_format += f"{kiri_rapi}{kanan}\n"
        
        # Tambahkan bentuk kompak
        bentuk_kompak = ", ".join(map(str, deret))
        hasil_format += f"\nBentuk kompak: {bentuk_kompak}"
        
        return hasil_format