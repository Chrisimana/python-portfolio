import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="data/history.json"):
        self.filename = filename
        self._ensure_directory_exists()
    
    # Memastikan direktori data exists
    def _ensure_directory_exists(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
    
    # Menyimpan record BMI ke file JSON
    def save_record(self, nama, berat, tinggi, bmi, kategori):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nama": nama,
            "berat": berat,
            "tinggi": tinggi,
            "bmi": bmi,
            "kategori": kategori
        }
        
        # Load existing data
        data = self.load_all_records()
        data.append(record)
        
        # Save back to file
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Memuat semua record dari file
    def load_all_records(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    # Menghapus semua history
    def clear_history(self):
        try:
            os.remove(self.filename)
            return True
        except FileNotFoundError:
            return False
    
    # Mendapatkan record terbaru
    def get_recent_records(self, limit=10):
        records = self.load_all_records()
        return records[-limit:] if records else []