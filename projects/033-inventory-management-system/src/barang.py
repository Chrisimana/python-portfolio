from dataclasses import dataclass
from datetime import datetime

@dataclass
class Barang:
    id: int
    nama: str
    harga: float
    kategori: str
    stok: int
    created_at: str
    updated_at: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'harga': self.harga,
            'kategori': self.kategori,
            'stok': self.stok,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id', 0),
            nama=data.get('nama', ''),
            harga=data.get('harga', 0),
            kategori=data.get('kategori', 'Umum'),
            stok=data.get('stok', 0),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', '')
        )