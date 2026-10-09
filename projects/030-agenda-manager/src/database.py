import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path='agenda.db'):
        self.db_path = db_path
        self.init_database()
    
    # Inisialisasi database dan tabel
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table untuk agenda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agenda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                deskripsi TEXT,
                kategori TEXT,
                prioritas INTEGER,
                deadline TEXT,
                selesai BOOLEAN,
                tanggal_dibuat TEXT,
                tanggal_diupdate TEXT
            )
        ''')
        
        # Table untuk riwayat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS riwayat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aksi TEXT,
                detail TEXT,
                waktu TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Eksekusi query umum
    def execute_query(self, query: str, params: tuple = ()):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
        
        conn.close()
        return result
    
    # Log aktivitas ke riwayat
    def log_riwayat(self, aksi: str, detail: str = ""):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute_query(
            "INSERT INTO riwayat (aksi, detail, waktu) VALUES (?, ?, ?)",
            (aksi, detail, waktu)
        )