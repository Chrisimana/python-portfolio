import random

class GameLogic:
    # Inisialisasi permainan
    def __init__(self):
        self.reset_game()
        
    # Reset permainan ke kondisi awal
    def reset_game(self):
        self.angka_rahasia = random.randint(1, 10)
        self.kesempatan = 3
        self.tebakan_sebelumnya = []
        self.status = "bermain"  # "bermain", "menang", "kalah"

    # Proses tebakan pemain    
    def tebak_angka(self, angka):
        if self.status != "bermain":
            return {"status": self.status, "pesan": "Permainan sudah selesai!"}
            
        if angka < 1 or angka > 10:
            return {"status": "error", "pesan": "Masukkan angka antara 1-10!"}
            
        self.tebakan_sebelumnya.append(angka)
        
        if angka == self.angka_rahasia:
            self.status = "menang"
            return {
                "status": "menang", 
                "pesan": f"Selamat! Tebakan Anda benar! Angka rahasia adalah {self.angka_rahasia}",
                "kesempatan": self.kesempatan
            }
        else:
            self.kesempatan -= 1
            
            if self.kesempatan == 0:
                self.status = "kalah"
                return {
                    "status": "kalah",
                    "pesan": f"Game Over! Angka rahasia adalah {self.angka_rahasia}",
                    "kesempatan": self.kesempatan
                }
            else:
                petunjuk = "lebih kecil" if angka > self.angka_rahasia else "lebih besar"
                return {
                    "status": "salah",
                    "pesan": f"Tebakan salah! Coba angka yang {petunjuk}",
                    "kesempatan": self.kesempatan
                }
    
    # Mendapatkan status permainan saat ini
    def get_game_state(self):
        return {
            "angka_rahasia": self.angka_rahasia,
            "kesempatan": self.kesempatan,
            "tebakan_sebelumnya": self.tebakan_sebelumnya.copy(),
            "status": self.status
        }