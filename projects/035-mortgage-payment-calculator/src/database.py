import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.db_path = "history/history_cicilan.db"
        self._create_database()
    
    def _create_database(self):
        """Membuat database dan tabel jika belum ada"""
        os.makedirs("history", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perhitungan_cicilan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                nama_proyek TEXT,
                harga_asal REAL,
                harga_jual REAL,
                lama_cicilan INTEGER,
                cicilan_per_tahun REAL,
                total_selisih REAL,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Menyimpan data perhitungan ke database
    def simpan_perhitungan(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO perhitungan_cicilan 
            (nama_proyek, harga_asal, harga_jual, lama_cicilan, cicilan_per_tahun, total_selisih, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nama_proyek'],
            data['harga_asal'],
            data['harga_jual'],
            data['lama_cicilan'],
            data['cicilan_per_tahun'],
            data['total_selisih'],
            json.dumps(data.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
    
    # Mengambil history perhitungan
    def ambil_history(self, limit=50):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM perhitungan_cicilan 
            ORDER BY tanggal DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    # Menghapus data history berdasarkan ID
    def hapus_history(self, id_perhitungan):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM perhitungan_cicilan WHERE id = ?', (id_perhitungan,))
        
        conn.commit()
        conn.close()
    
    # Menghapus semua data history
    def hapus_semua_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM perhitungan_cicilan')
        
        conn.commit()
        conn.close()