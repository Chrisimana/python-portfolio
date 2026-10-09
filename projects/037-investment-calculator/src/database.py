import json
import os
from models import Investasi, HistoryManager
from datetime import datetime

class DatabaseManager:
    def __init__(self, filename="history_investasi.json"):
        self.filename = filename
        self.history_manager = HistoryManager()
        self.load_data()
    
    def save_investasi(self, investasi: Investasi):
        self.history_manager.tambah_investasi(investasi)
        self.save_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        investasi = Investasi(
                            modal_awal=item['modal_awal'],
                            bunga=item['bunga'],
                            tahun=item['tahun'],
                            hasil=item['hasil'],
                            tanggal=datetime.fromisoformat(item['tanggal'])
                        )
                        self.history_manager.tambah_investasi(investasi)
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def save_data(self):
        data = []
        for investasi in self.history_manager.get_history():
            data.append({
                'modal_awal': investasi.modal_awal,
                'bunga': investasi.bunga,
                'tahun': investasi.tahun,
                'hasil': investasi.hasil,
                'tanggal': investasi.tanggal.isoformat()
            })
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_all_history(self):
        return self.history_manager.get_history()
    
    def clear_history(self):
        self.history_manager.clear_history()
        if os.path.exists(self.filename):
            os.remove(self.filename)