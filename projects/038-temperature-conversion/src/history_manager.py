import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="history_konversi.json"):
        self.filename = filename
        self.history = []
        self.load_history()
    
    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.history = json.load(file)
            except (json.JSONDecodeError, IOError):
                self.history = []
    
    def save_history(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.history, file, indent=2)
        except IOError:
            print("Gagal menyimpan history")
    
    def add_entry(self, nilai_awal, satuan_awal, nilai_hasil, satuan_hasil):
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'nilai_awal': nilai_awal,
            'satuan_awal': satuan_awal,
            'nilai_hasil': nilai_hasil,
            'satuan_hasil': satuan_hasil
        }
        self.history.append(entry)
        self.save_history()
    
    def get_history(self, limit=None):
        if limit is None:
            return self.history
        return self.history[-limit:]
    
    def clear_history(self):
        self.history = []
        self.save_history()