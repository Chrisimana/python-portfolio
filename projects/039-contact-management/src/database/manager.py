import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='kontak.db'):
        self.db_path = db_path
        self.init_database()
    
    # Inisialisasi database dan tabel
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabel kontak
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kontak (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                telepon TEXT,
                email TEXT,
                kategori TEXT DEFAULT 'Umum',
                tanggal_dibuat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tanggal_diubah TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aksi TEXT NOT NULL,
                detail TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel kategori
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kategori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT UNIQUE NOT NULL,
                warna TEXT DEFAULT '#3498db'
            )
        ''')
        
        # Insert kategori default
        kategori_default = ['Keluarga', 'Teman', 'Kantor', 'Darurat', 'Umum']
        for kategori in kategori_default:
            cursor.execute('INSERT OR IGNORE INTO kategori (nama) VALUES (?)', (kategori,))
        
        conn.commit()
        conn.close()
    
    # Eksekusi query umum
    def execute_query(self, query, params=()):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    
    # Ambil semua data
    def fetch_all(self, query, params=()):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    # Log history aktivitas
    def log_history(self, aksi, detail=""):
        self.execute_query(
            'INSERT INTO history (aksi, detail) VALUES (?, ?)',
            (aksi, detail)
        )