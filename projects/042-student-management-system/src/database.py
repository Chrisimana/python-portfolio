import json
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_file="students_data.json"):
        self.db_file = db_file
        self.ensure_database_exists()
    
    # Pastikan database ada, jika tidak ada buat yang baru
    def ensure_database_exists(self):
        if not os.path.exists(self.db_file):
            self.init_database()
    
    # Inisialisasi database kosong
    def init_database(self):
        with open(self.db_file, 'w') as file:
            json.dump([], file)
    
    # Load data dari database
    def load_data(self):
        try:
            with open(self.db_file, 'r') as file:
                return json.load(file)
        except:
            return []
    
    # Simpan data ke database
    def save_data(self, data):
        with open(self.db_file, 'w') as file:
            json.dump(data, file, indent=4)
    
    # Tambah record baru ke database
    def add_record(self, record):
        data = self.load_data()
        record['id'] = len(data) + 1
        record['created_at'] = datetime.now().isoformat()
        data.append(record)
        self.save_data(data)
        return record
    
    # Hapus record dari database berdasarkan ID
    def delete_record(self, record_id):
        data = self.load_data()
        data = [record for record in data if record['id'] != record_id]
        self.save_data(data)
        return len(data)
    
    # Cari record berdasarkan query
    def search_records(self, query):
        data = self.load_data()
        if not query:
            return data
        
        results = []
        for record in data:
            if (query.lower() in record.get('name', '').lower() or 
                query.lower() in record.get('nim', '').lower()):
                results.append(record)
        return results