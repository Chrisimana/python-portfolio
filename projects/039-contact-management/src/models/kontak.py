
from database.manager import DatabaseManager
from datetime import datetime

class Kontak:
    def __init__(self):
        self.db = DatabaseManager()
        self.kategori_list = self.ambil_semua_kategori()
    
    # Ambil semua kontak, bisa difilter berdasarkan kategori
    def ambil_semua_kontak(self, kategori=None):
        if kategori:
            query = 'SELECT * FROM kontak WHERE kategori = ? ORDER BY nama'
            return self.db.fetch_all(query, (kategori,))
        else:
            query = 'SELECT * FROM kontak ORDER BY nama'
            return self.db.fetch_all(query)
    
    # Ambil kontak berdasarkan ID
    def ambil_kontak_by_id(self, id_kontak):
        query = 'SELECT * FROM kontak WHERE id = ?'
        result = self.db.fetch_all(query, (id_kontak,))
        return result[0] if result else None
    
    def tambah_kontak(self, nama, telepon, email, kategori="Umum"):
        """Tambah kontak baru"""
        query = '''
            INSERT INTO kontak (nama, telepon, email, kategori, tanggal_dibuat, tanggal_diubah)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute_query(query, (nama, telepon, email, kategori, timestamp, timestamp))
        
        # Log history
        self.db.log_history("TAMBAH", f"Kontak {nama} ditambahkan")
    
    def edit_kontak(self, id_kontak, nama, telepon, email, kategori):
        """Edit kontak yang sudah ada"""
        query = '''
            UPDATE kontak 
            SET nama = ?, telepon = ?, email = ?, kategori = ?, tanggal_diubah = ?
            WHERE id = ?
        '''
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute_query(query, (nama, telepon, email, kategori, timestamp, id_kontak))
        
        # Log history
        self.db.log_history("EDIT", f"Kontak {nama} diubah")
    
    # Hapus kontak
    def hapus_kontak(self, id_kontak):
        kontak = self.ambil_kontak_by_id(id_kontak)
        if kontak:
            query = 'DELETE FROM kontak WHERE id = ?'
            self.db.execute_query(query, (id_kontak,))
            
            # Log history
            self.db.log_history("HAPUS", f"Kontak {kontak[1]} dihapus")
    
    def cari_kontak(self, keyword):
        """Cari kontak berdasarkan nama atau telepon"""
        query = '''
            SELECT * FROM kontak 
            WHERE nama LIKE ? OR telepon LIKE ? OR email LIKE ?
            ORDER BY nama
        '''
        search_term = f'%{keyword}%'
        return self.db.fetch_all(query, (search_term, search_term, search_term))
    
    # Ambil semua kategori
    def ambil_semua_kategori(self):
        query = 'SELECT nama FROM kategori ORDER BY nama'
        results = self.db.fetch_all(query)
        return [result[0] for result in results]
    
    # Ambil history aktivitas
    def ambil_history(self, limit=50):
        query = 'SELECT * FROM history ORDER BY timestamp DESC LIMIT ?'
        return self.db.fetch_all(query, (limit,))
    
    def statistik_kontak(self):
        """Ambil statistik kontak per kategori"""
        query = '''
            SELECT kategori, COUNT(*) as jumlah 
            FROM kontak 
            GROUP BY kategori 
            ORDER BY jumlah DESC
        '''
        return self.db.fetch_all(query)