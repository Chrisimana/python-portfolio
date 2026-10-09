from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QScrollArea, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from models import Investasi
from database import DatabaseManager

class InputInvestasiWidget(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Kalkulator Investasi")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        
        # Input Group
        input_group = QGroupBox("Data Investasi")
        input_layout = QVBoxLayout()
        
        # Modal Input
        modal_layout = QHBoxLayout()
        self.input_modal = QLineEdit()
        self.input_modal.setPlaceholderText("Masukkan modal awal (Rp)")
        modal_layout.addWidget(QLabel("Modal Awal:"))
        modal_layout.addWidget(self.input_modal)
        
        # Bunga Input
        bunga_layout = QHBoxLayout()
        self.input_bunga = QLineEdit()
        self.input_bunga.setPlaceholderText("Bunga per tahun (%)")
        bunga_layout.addWidget(QLabel("Bunga (%):"))
        bunga_layout.addWidget(self.input_bunga)
        
        # Tahun Input
        tahun_layout = QHBoxLayout()
        self.input_tahun = QLineEdit()
        self.input_tahun.setPlaceholderText("Lama investasi (tahun)")
        tahun_layout.addWidget(QLabel("Tahun:"))
        tahun_layout.addWidget(self.input_tahun)
        
        input_layout.addLayout(modal_layout)
        input_layout.addLayout(bunga_layout)
        input_layout.addLayout(tahun_layout)
        input_group.setLayout(input_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_hitung = QPushButton("🚀 Hitung Investasi")
        self.btn_hitung.setObjectName("secondary")
        self.btn_clear = QPushButton("🗑️ Bersihkan")
        self.btn_clear.setObjectName("danger")
        
        button_layout.addWidget(self.btn_hitung)
        button_layout.addWidget(self.btn_clear)
        
        # Result
        self.label_hasil = QLabel("Hasil akan ditampilkan di sini...")
        self.label_hasil.setObjectName("result")
        self.label_hasil.setAlignment(Qt.AlignCenter)
        self.label_hasil.setMinimumHeight(80)
        
        # Connections
        self.btn_hitung.clicked.connect(self.hitung_investasi)
        self.btn_clear.clicked.connect(self.clear_inputs)
        
        # Add to main layout
        layout.addWidget(title)
        layout.addWidget(input_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.label_hasil)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def hitung_investasi(self):
        try:
            modal = float(self.input_modal.text().replace(',', ''))
            bunga = float(self.input_bunga.text()) / 100
            tahun = int(self.input_tahun.text())
            
            if modal <= 0 or bunga <= 0 or tahun <= 0:
                raise ValueError("Nilai harus positif")
            
            # Rumus bunga majemuk: A = P * (1 + r)^t
            hasil = modal * ((1 + bunga) ** tahun)
            
            # Format hasil dengan separator ribuan
            hasil_formatted = f"Rp {hasil:,.2f}"
            
            self.label_hasil.setText(
                f"💰 Hasil Investasi setelah {tahun} tahun:\n"
                f"{hasil_formatted}"
            )
            
            # Simpan ke database
            investasi = Investasi(modal, bunga * 100, tahun, hasil)
            self.db_manager.save_investasi(investasi)
            
            # Refresh history di parent
            if self.parent:
                self.parent.refresh_history()
                
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", 
                              "Harap masukkan angka yang valid!\n" + str(e))
    
    def clear_inputs(self):
        self.input_modal.clear()
        self.input_bunga.clear()
        self.input_tahun.clear()
        self.label_hasil.setText("Hasil akan ditampilkan di sini...")

class HistoryWidget(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Riwayat Perhitungan")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Tanggal", "Modal Awal", "Bunga (%)", "Tahun", "Hasil Akhir"
        ])
        
        # Header styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Clear button
        self.btn_clear_history = QPushButton("🗑️ Hapus Semua Riwayat")
        self.btn_clear_history.setObjectName("danger")
        self.btn_clear_history.clicked.connect(self.clear_history)
        
        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addWidget(self.btn_clear_history)
        
        self.setLayout(layout)
        self.load_data()
    
    def load_data(self):
        history = self.db_manager.get_all_history()
        self.table.setRowCount(len(history))
        
        for row, investasi in enumerate(history):
            self.table.setItem(row, 0, QTableWidgetItem(
                investasi.tanggal.strftime("%d/%m/%Y %H:%M")
            ))
            self.table.setItem(row, 1, QTableWidgetItem(
                f"Rp {investasi.modal_awal:,.2f}"
            ))
            self.table.setItem(row, 2, QTableWidgetItem(
                f"{investasi.bunga:.2f}%"
            ))
            self.table.setItem(row, 3, QTableWidgetItem(
                str(investasi.tahun)
            ))
            self.table.setItem(row, 4, QTableWidgetItem(
                f"Rp {investasi.hasil:,.2f}"
            ))
    
    def clear_history(self):
        reply = QMessageBox.question(
            self, 'Konfirmasi',
            'Apakah Anda yakin ingin menghapus semua riwayat?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db_manager.clear_history()
            self.table.setRowCount(0)
            QMessageBox.information(self, "Sukses", "Riwayat berhasil dihapus!")

class MainTabWidget(QTabWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        
        # Create tabs
        self.input_widget = InputInvestasiWidget(db_manager, self)
        self.history_widget = HistoryWidget(db_manager)
        
        self.addTab(self.input_widget, "🧮 Kalkulator")
        self.addTab(self.history_widget, "📊 Riwayat")
    
    def refresh_history(self):
        self.history_widget.load_data()