import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="history_diskon.json"):
        self.filename = filename
        self.history = []
        self.load_history()
    
    # Memuat history dari file JSON
    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.history = json.load(file)
            except (json.JSONDecodeError, Exception):
                self.history = []
    
    # Menyimpan history ke file JSON
    def save_history(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.history, file, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    # Menambahkan perhitungan ke history
    def tambah_history(self, harga_asal, diskon, harga_diskon):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "harga_asal": harga_asal,
            "diskon": diskon,
            "harga_diskon": harga_diskon
        }
        self.history.append(entry)
        self.save_history()
    
    # Mendapatkan history
    def get_history(self, limit=None):
        if limit:
            return self.history[-limit:]
        return self.history
    
    # Menghapus semua history
    def hapus_history(self):
        self.history = []
        self.save_history()
    
    # Mengekspor history ke file CSV
    def export_to_csv(self, filename="history_diskon.csv"):
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Waktu", "Harga Asal", "Diskon (%)", "Harga Diskon"])
                for entry in self.history:
                    writer.writerow([
                        entry["timestamp"],
                        entry["harga_asal"],
                        entry["diskon"],
                        entry["harga_diskon"]
                    ])
            return True
        except Exception:
            return False