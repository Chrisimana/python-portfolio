from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush

class StatisticsWidget(QWidget):
    def __init__(self, db_handler):
        super().__init__()
        self.db = db_handler
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Scroll area untuk konten
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # Header
        header = QLabel("📊 Statistik Inventory")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(header)
        
        # Grid untuk kartu statistik
        stats_grid = QGridLayout()
        self.stats_cards = {}
        
        card_titles = {
            'total_barang': ('Total Barang', '📦'),
            'total_stok': ('Total Stok', '📊'),
            'total_nilai': ('Total Nilai Inventory', '💰')
        }
        
        for i, (key, (title, icon)) in enumerate(card_titles.items()):
            card = self.create_stat_card(icon, title, "0")
            stats_grid.addWidget(card, i // 2, i % 2)
            self.stats_cards[key] = card
        
        content_layout.addLayout(stats_grid)
        
        # Statistik per kategori
        kategori_group = QGroupBox("Statistik per Kategori")
        kategori_layout = QVBoxLayout()
        self.kategori_table = QTableWidget()
        self.kategori_table.setColumnCount(4)
        self.kategori_table.setHorizontalHeaderLabels(["Kategori", "Jumlah Item", "Total Stok", "Total Nilai"])
        self.kategori_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        kategori_layout.addWidget(self.kategori_table)
        kategori_group.setLayout(kategori_layout)
        content_layout.addWidget(kategori_group)
        
        # Peringatan stok
        warning_group = QGroupBox("⚠️ Peringatan Stok")
        warning_group.setStyleSheet("QGroupBox { color: orange; }")
        warning_layout = QHBoxLayout()
        
        self.stok_rendah_label = QLabel()
        self.stok_rendah_label.setWordWrap(True)
        self.stok_habis_label = QLabel()
        self.stok_habis_label.setWordWrap(True)
        
        warning_layout.addWidget(self.stok_rendah_label)
        warning_layout.addWidget(self.stok_habis_label)
        warning_group.setLayout(warning_layout)
        content_layout.addWidget(warning_group)
        
        # Info harga
        harga_group = QGroupBox("🏷️ Informasi Harga")
        harga_layout = QGridLayout()
        self.harga_tertinggi_label = QLabel()
        self.harga_terendah_label = QLabel()
        
        harga_layout.addWidget(QLabel("Harga Tertinggi:"), 0, 0)
        harga_layout.addWidget(self.harga_tertinggi_label, 0, 1)
        harga_layout.addWidget(QLabel("Harga Terendah:"), 1, 0)
        harga_layout.addWidget(self.harga_terendah_label, 1, 1)
        harga_group.setLayout(harga_layout)
        content_layout.addWidget(harga_group)
        
        # Riwayat transaksi terbaru
        transaksi_group = QGroupBox("📜 Riwayat Transaksi Terbaru")
        transaksi_layout = QVBoxLayout()
        self.transaksi_table = QTableWidget()
        self.transaksi_table.setColumnCount(5)
        self.transaksi_table.setHorizontalHeaderLabels(["ID", "ID Barang", "Jenis", "Jumlah", "Tanggal"])
        self.transaksi_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        transaksi_layout.addWidget(self.transaksi_table)
        transaksi_group.setLayout(transaksi_layout)
        content_layout.addWidget(transaksi_group)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.setLayout(layout)
    
    def create_stat_card(self, icon, title, value):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        icon_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 18, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: #4CAF50;")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        
        return card
    
    def refresh(self):
        stats = self.db.get_statistik()
        
        # Update stat cards
        self.stats_cards['total_barang'].findChildren(QLabel)[2].setText(str(stats['total_barang']))
        self.stats_cards['total_stok'].findChildren(QLabel)[2].setText(str(stats['total_stok']))
        nilai_text = f"Rp {stats['total_nilai']:,.0f}".replace(",", ".")
        self.stats_cards['total_nilai'].findChildren(QLabel)[2].setText(nilai_text)
        
        # Update kategori table
        self.kategori_table.setRowCount(0)
        for kategori, data in stats['kategori_stats'].items():
            row = self.kategori_table.rowCount()
            self.kategori_table.insertRow(row)
            self.kategori_table.setItem(row, 0, QTableWidgetItem(kategori))
            self.kategori_table.setItem(row, 1, QTableWidgetItem(str(data['jumlah'])))
            self.kategori_table.setItem(row, 2, QTableWidgetItem(str(data['total_stok'])))
            nilai = f"Rp {data['total_nilai']:,.0f}".replace(",", ".")
            self.kategori_table.setItem(row, 3, QTableWidgetItem(nilai))
        
        # Update stok warnings
        stok_rendah_text = "⚠️ Stok Rendah (<5):\n"
        if stats['stok_rendah']:
            for b in stats['stok_rendah'][:5]:
                stok_rendah_text += f"• {b.nama}: {b.stok} unit\n"
        else:
            stok_rendah_text += "Tidak ada stok rendah\n"
        
        stok_habis_text = "❌ Stok Habis:\n"
        if stats['stok_habis']:
            for b in stats['stok_habis'][:5]:
                stok_habis_text += f"• {b.nama}\n"
        else:
            stok_habis_text += "Tidak ada stok habis\n"
        
        self.stok_rendah_label.setText(stok_rendah_text)
        self.stok_habis_label.setText(stok_habis_text)
        
        # Update harga info
        if stats['harga_tertinggi']:
            harga_tertinggi = f"{stats['harga_tertinggi'].nama} - Rp {stats['harga_tertinggi'].harga:,.0f}".replace(",", ".")
            harga_terendah = f"{stats['harga_terendah'].nama} - Rp {stats['harga_terendah'].harga:,.0f}".replace(",", ".")
            self.harga_tertinggi_label.setText(harga_tertinggi)
            self.harga_terendah_label.setText(harga_terendah)
        
        # Update transaksi table
        self.transaksi_table.setRowCount(0)
        for trans in stats['transactions']:
            row = self.transaksi_table.rowCount()
            self.transaksi_table.insertRow(row)
            self.transaksi_table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
            self.transaksi_table.setItem(row, 1, QTableWidgetItem(str(trans['barang_id'])))
            
            jenis_item = QTableWidgetItem(trans['jenis'])
            if trans['jenis'] == 'masuk':
                jenis_item.setForeground(QBrush(QColor(76, 175, 80)))
            else:
                jenis_item.setForeground(QBrush(QColor(244, 67, 54)))
            self.transaksi_table.setItem(row, 2, jenis_item)
            
            self.transaksi_table.setItem(row, 3, QTableWidgetItem(str(trans['jumlah'])))
            self.transaksi_table.setItem(row, 4, QTableWidgetItem(trans['tanggal']))