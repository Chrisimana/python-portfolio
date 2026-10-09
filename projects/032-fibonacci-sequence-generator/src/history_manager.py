import json
import os
import datetime
from typing import List, Dict

class ManajerRiwayat:
    def __init__(self, nama_file="fibonacci_history.json"):
        self.nama_file = nama_file
        self.riwayat = self.muat_riwayat()
    
    def muat_riwayat(self) -> List[Dict]: 

        # Memuat riwayat dari file JSON
        if os.path.exists(self.nama_file):
            try:
                with open(self.nama_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error memuat riwayat: {e}")
                return []
        return []
    
    def simpan_riwayat(self):
        
        # Menyimpan riwayat ke file JSON
        try:
            with open(self.nama_file, 'w', encoding='utf-8') as file:
                json.dump(self.riwayat, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error menyimpan riwayat: {e}")
    
    def tambah_riwayat(self, n: int, deret: List[int]):

        # Menambahkan entri baru ke riwayat
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entri = {
            "timestamp": timestamp,
            "n": n,
            "deret": deret,
            "suku_terakhir": deret[-1] if deret else 0
        }
        
        self.riwayat.append(entri)
        self.simpan_riwayat()
    
    def dapatkan_riwayat_terbaru(self, jumlah: int = 20) -> List[Dict]: 

        # Mendapatkan entri riwayat terbaru
        return self.riwayat[-jumlah:]
    
    def bersihkan_riwayat(self):

        # Membersihkan seluruh riwayat
        self.riwayat = []
        self.simpan_riwayat()
    
    def ekspor_riwayat_ke_file(self, nama_file=None):

        # Mengekspor riwayat ke file teks
        if not nama_file:
            nama_file = f"fibonacci_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(nama_file, 'w', encoding='utf-8') as file:
                file.write("RIWAYAT PERHITUNGAN DERET FIBONACCI\n")
                file.write("=" * 50 + "\n\n")
                
                for entri in self.riwayat:
                    file.write(f"Waktu: {entri['timestamp']}\n")
                    file.write(f"Jumlah suku (N): {entri['n']}\n")
                    file.write(f"Suku terakhir: {entri['suku_terakhir']}\n")
                    file.write(f"Deret: {', '.join(map(str, entri['deret']))}\n")
                    file.write("-" * 40 + "\n")
            
            return nama_file
        except Exception as e:
            raise Exception(f"Gagal mengekspor riwayat: {e}")
    
    def dapatkan_entri_dari_index(self, index: int) -> Dict:

        # Mendapatkan entri riwayat berdasarkan indeks
        if 0 <= index < len(self.riwayat):
            return self.riwayat[index]
        return None