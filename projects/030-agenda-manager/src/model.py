from datetime import datetime
import json
import os
from pathlib import Path
from typing import List, Dict, Optional

class AgendaItem:
    def __init__(self, judul: str, deskripsi: str = "", kategori: str = "Umum", 
                 prioritas: int = 3, deadline: str = "", selesai: bool = False):
        self.id = int(datetime.now().timestamp() * 1000)
        self.judul = judul
        self.deskripsi = deskripsi
        self.kategori = kategori
        self.prioritas = prioritas  # 1: Tinggi, 2: Sedang, 3: Rendah
        self.deadline = deadline
        self.selesai = selesai
        self.tanggal_dibuat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tanggal_diupdate = self.tanggal_dibuat
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'judul': self.judul,
            'deskripsi': self.deskripsi,
            'kategori': self.kategori,
            'prioritas': self.prioritas,
            'deadline': self.deadline,
            'selesai': self.selesai,
            'tanggal_dibuat': self.tanggal_dibuat,
            'tanggal_diupdate': self.tanggal_diupdate
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AgendaItem':
        item = cls(
            judul=data['judul'],
            deskripsi=data['deskripsi'],
            kategori=data['kategori'],
            prioritas=data['prioritas'],
            deadline=data['deadline'],
            selesai=data['selesai']
        )
        item.id = data['id']
        item.tanggal_dibuat = data['tanggal_dibuat']
        item.tanggal_diupdate = data['tanggal_diupdate']
        return item

class ModelAgenda:
    def __init__(self):
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        self.file_path = self.data_dir / 'data_agenda.json'
        self.agenda_items: List[AgendaItem] = []
        self.muat_data()
    
    # Memuat data agenda dari file JSON
    def muat_data(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.agenda_items = [AgendaItem.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading data: {e}")
            self.agenda_items = []
    
    # Menyimpan data agenda ke file JSON
    def simpan_data(self):
        try:
            data = [item.to_dict() for item in self.agenda_items]
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    # Menambah agenda baru
    def tambah_agenda(self, agenda_item: AgendaItem) -> bool:
        self.agenda_items.append(agenda_item)
        self.simpan_data()
        return True
    
    # Menghapus agenda berdasarkan ID
    def hapus_agenda(self, agenda_id: int) -> bool:
        self.agenda_items = [item for item in self.agenda_items if item.id != agenda_id]
        self.simpan_data()
        return True
    
    # Update agenda berdasarkan ID
    def update_agenda(self, agenda_id: int, **kwargs) -> bool:
        for item in self.agenda_items:
            if item.id == agenda_id:
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                item.tanggal_diupdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.simpan_data()
                return True
        return False
    
    # Mendapatkan agenda berdasarkan ID
    def dapatkan_agenda_by_id(self, agenda_id: int) -> Optional[AgendaItem]:
        for item in self.agenda_items:
            if item.id == agenda_id:
                return item
        return None
    
    # Mendapatkan semua agenda
    def dapatkan_semua_agenda(self) -> List[AgendaItem]:
        return self.agenda_items
    
    # Mendapatkan agenda berdasarkan kategori
    def dapatkan_agenda_by_kategori(self, kategori: str) -> List[AgendaItem]:
        return [item for item in self.agenda_items if item.kategori == kategori]
    
    # Mendapatkan agenda dengan prioritas tinggi
    def dapatkan_agenda_prioritas_tinggi(self) -> List[AgendaItem]:
        return [item for item in self.agenda_items if item.prioritas == 1 and not item.selesai]
    
    # Mendapatkan statistik agenda
    def dapatkan_statistik(self) -> Dict:
        total = len(self.agenda_items)
        selesai = len([item for item in self.agenda_items if item.selesai])
        belum_selesai = total - selesai
        prioritas_tinggi = len([item for item in self.agenda_items if item.prioritas == 1])
        
        return {
            'total': total,
            'selesai': selesai,
            'belum_selesai': belum_selesai,
            'prioritas_tinggi': prioritas_tinggi
        }