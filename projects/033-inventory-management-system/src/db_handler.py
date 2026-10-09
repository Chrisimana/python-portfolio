import json
import os
from datetime import datetime
from barang import Barang

class DatabaseHandler:
    def __init__(self, db_file='data/data_inventory.json'):
        # Pastikan direktori data ada
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        self.db_file = db_file
        self.data = self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'barang': [], 'next_id': 1, 'transactions': []}
        return {'barang': [], 'next_id': 1, 'transactions': []}
    
    def _save_data(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def _add_transaction(self, id_barang, jenis, jumlah, keterangan):
        """Mencatat transaksi stok"""
        transaction = {
            'id': len(self.data['transactions']) + 1,
            'barang_id': id_barang,
            'jenis': jenis,  # 'masuk' atau 'keluar'
            'jumlah': jumlah,
            'keterangan': keterangan,
            'tanggal': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data['transactions'].append(transaction)
        self._save_data()
    
    def tambah_barang(self, barang_data):
        barang = Barang.from_dict(barang_data)
        barang.id = self.data['next_id']
        barang.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        barang.updated_at = barang.created_at
        
        self.data['barang'].append(barang.to_dict())
        self.data['next_id'] += 1
        
        # Catat transaksi awal
        self._add_transaction(barang.id, 'masuk', barang.stok, 'Penambahan barang baru')
        self._save_data()
        return barang.id
    
    def get_all_barang(self):
        return [Barang.from_dict(item) for item in self.data['barang']]
    
    def get_barang_by_id(self, id_barang):
        for item in self.data['barang']:
            if item['id'] == id_barang:
                return Barang.from_dict(item)
        return None
    
    def update_barang(self, id_barang, barang_data):
        for item in self.data['barang']:
            if item['id'] == id_barang:
                old_stok = item.get('stok', 0)
                item.update(barang_data)
                item['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Catat perubahan stok
                new_stok = barang_data.get('stok', old_stok)
                if new_stok != old_stok:
                    selisih = new_stok - old_stok
                    jenis = 'masuk' if selisih > 0 else 'keluar'
                    self._add_transaction(id_barang, jenis, abs(selisih), 
                                         f'Update manual stok ({old_stok} -> {new_stok})')
                
                self._save_data()
                return True
        return False
    
    def tambah_stok(self, id_barang, jumlah, keterangan="Penambahan stok"):
        """Menambah stok barang"""
        for item in self.data['barang']:
            if item['id'] == id_barang:
                item['stok'] += jumlah
                item['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._add_transaction(id_barang, 'masuk', jumlah, keterangan)
                self._save_data()
                return True
        return False
    
    def kurangi_stok(self, id_barang, jumlah, keterangan="Pengurangan stok"):
        """Mengurangi stok barang"""
        for item in self.data['barang']:
            if item['id'] == id_barang:
                if item['stok'] >= jumlah:
                    item['stok'] -= jumlah
                    item['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._add_transaction(id_barang, 'keluar', jumlah, keterangan)
                    self._save_data()
                    return True
                else:
                    return False  # Stok tidak cukup
        return False
    
    def hapus_barang(self, id_barang):
        self.data['barang'] = [item for item in self.data['barang'] if item['id'] != id_barang]
        self._save_data()
        return True
    
    def cari_barang(self, keyword):
        results = []
        for item in self.data['barang']:
            if (keyword.lower() in item['nama'].lower() or 
                keyword.lower() in item['kategori'].lower()):
                results.append(Barang.from_dict(item))
        return results
    
    def get_statistik(self):
        """Mendapatkan data statistik"""
        barang_list = self.get_all_barang()
        
        total_barang = len(barang_list)
        total_nilai = sum(b.harga * b.stok for b in barang_list)
        total_stok = sum(b.stok for b in barang_list)
        
        # Statistik per kategori
        kategori_stats = {}
        for b in barang_list:
            if b.kategori not in kategori_stats:
                kategori_stats[b.kategori] = {
                    'jumlah': 0,
                    'total_nilai': 0,
                    'total_stok': 0
                }
            kategori_stats[b.kategori]['jumlah'] += 1
            kategori_stats[b.kategori]['total_nilai'] += b.harga * b.stok
            kategori_stats[b.kategori]['total_stok'] += b.stok
        
        # Stok rendah (< 5)
        stok_rendah = [b for b in barang_list if b.stok < 5 and b.stok > 0]
        stok_habis = [b for b in barang_list if b.stok == 0]
        
        # Harga tertinggi dan terendah
        if barang_list:
            harga_tertinggi = max(barang_list, key=lambda x: x.harga)
            harga_terendah = min(barang_list, key=lambda x: x.harga)
        else:
            harga_tertinggi = harga_terendah = None
        
        return {
            'total_barang': total_barang,
            'total_nilai': total_nilai,
            'total_stok': total_stok,
            'kategori_stats': kategori_stats,
            'stok_rendah': stok_rendah,
            'stok_habis': stok_habis,
            'harga_tertinggi': harga_tertinggi,
            'harga_terendah': harga_terendah,
            'transactions': self.data['transactions'][-20:]  # 20 transaksi terakhir
        }
    
    def get_transactions(self, limit=50):
        """Mendapatkan riwayat transaksi"""
        return self.data['transactions'][-limit:]