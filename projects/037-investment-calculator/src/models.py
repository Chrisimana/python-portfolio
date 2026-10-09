from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Investasi:
    modal_awal: float
    bunga: float
    tahun: int
    hasil: float
    tanggal: datetime = None
    
    def __post_init__(self):
        if self.tanggal is None:
            self.tanggal = datetime.now()

class HistoryManager:
    def __init__(self):
        self.history: List[Investasi] = []
    
    def tambah_investasi(self, investasi: Investasi):
        self.history.append(investasi)
    
    def get_history(self) -> List[Investasi]:
        return sorted(self.history, key=lambda x: x.tanggal, reverse=True)
    
    def clear_history(self):
        self.history.clear()