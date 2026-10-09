import csv
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
from PyQt5.QtCore import QObject, pyqtSignal

class ExportUtils(QObject):
    exportFinished = pyqtSignal(bool, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def export_to_csv(self, data, filename=None):
        try:
            if not filename:
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent(),
                    "Simpan File CSV",
                    f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "CSV Files (*.csv)"
                )
            
            if not filename:
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # Header
                writer.writerow(['ID', 'Nama Barang', 'Harga', 'Kategori', 'Stok', 'Terakhir Diupdate'])
                # Data
                for barang in data:
                    writer.writerow([
                        barang.id,
                        barang.nama,
                        barang.harga,
                        barang.kategori,
                        barang.stok,
                        barang.updated_at
                    ])
            
            self.exportFinished.emit(True, f"Data berhasil diekspor ke {filename}")
            return True
            
        except Exception as e:
            self.exportFinished.emit(False, f"Gagal mengekspor data: {str(e)}")
            return False
    
    def export_to_json(self, data, filename=None):
        try:
            if not filename:
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent(),
                    "Simpan File JSON",
                    f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "JSON Files (*.json)"
                )
            
            if not filename:
                return False
            
            data_dict = [barang.to_dict() for barang in data]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            
            self.exportFinished.emit(True, f"Data berhasil diekspor ke {filename}")
            return True
            
        except Exception as e:
            self.exportFinished.emit(False, f"Gagal mengekspor data: {str(e)}")
            return False
    
    def export_to_excel(self, data, filename=None):
        """Export to Excel (XLSX) using pandas if available"""
        try:
            import pandas as pd
            
            if not filename:
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent(),
                    "Simpan File Excel",
                    f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    "Excel Files (*.xlsx)"
                )
            
            if not filename:
                return False
            
            df = pd.DataFrame([{
                'ID': b.id,
                'Nama Barang': b.nama,
                'Harga': b.harga,
                'Kategori': b.kategori,
                'Stok': b.stok,
                'Terakhir Diupdate': b.updated_at
            } for b in data])
            
            df.to_excel(filename, index=False, engine='openpyxl')
            self.exportFinished.emit(True, f"Data berhasil diekspor ke {filename}")
            return True
            
        except ImportError:
            self.exportFinished.emit(False, "Pandas tidak terinstall. Gunakan format CSV atau JSON.")
            return False
        except Exception as e:
            self.exportFinished.emit(False, f"Gagal mengekspor data: {str(e)}")
            return False