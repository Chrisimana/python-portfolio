from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QAction,
    QMessageBox, QAbstractItemView, QPushButton, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QBrush

class CustomTableWidget(QTableWidget):
    itemDeleted = pyqtSignal(int)
    itemEdited = pyqtSignal(int)
    stockAdded = pyqtSignal(int, int, str)  # id, jumlah, keterangan
    stockReduced = pyqtSignal(int, int, str)  # id, jumlah, keterangan
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_context_menu()
    
    def setup_ui(self):
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            "ID", "Nama Barang", "Harga", "Kategori", "Stok", "Aksi", "Terakhir Diupdate"
        ])
        
        # Styling table
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        self.setColumnWidth(5, 120)
        
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Set font
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
    
    def setup_context_menu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        menu = QMenu(self)
        
        edit_action = QAction("✏️ Edit Barang", self)
        tambah_stok_action = QAction("➕ Tambah Stok", self)
        kurangi_stok_action = QAction("➖ Kurangi Stok", self)
        delete_action = QAction("🗑️ Hapus Barang", self)
        
        edit_action.triggered.connect(self.edit_selected_item)
        tambah_stok_action.triggered.connect(self.tambah_stok_selected)
        kurangi_stok_action.triggered.connect(self.kurangi_stok_selected)
        delete_action.triggered.connect(self.delete_selected_item)
        
        menu.addAction(edit_action)
        menu.addAction(tambah_stok_action)
        menu.addAction(kurangi_stok_action)
        menu.addSeparator()
        menu.addAction(delete_action)
        
        menu.exec_(self.viewport().mapToGlobal(position))
    
    def edit_selected_item(self):
        current_row = self.currentRow()
        if current_row >= 0:
            item_id = int(self.item(current_row, 0).text())
            self.itemEdited.emit(item_id)
    
    def tambah_stok_selected(self):
        current_row = self.currentRow()
        if current_row >= 0:
            item_id = int(self.item(current_row, 0).text())
            item_name = self.item(current_row, 1).text()
            from widgets.form_widget import StockManagementDialog
            # Need to get barang object - will be handled in main window
            self.stockAdded.emit(item_id, 0, "")  # Signal will be handled in main
    
    def kurangi_stok_selected(self):
        current_row = self.currentRow()
        if current_row >= 0:
            item_id = int(self.item(current_row, 0).text())
            self.stockReduced.emit(item_id, 0, "")
    
    def delete_selected_item(self):
        current_row = self.currentRow()
        if current_row >= 0:
            item_id = int(self.item(current_row, 0).text())
            item_name = self.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, 'Konfirmasi Hapus',
                f'Apakah Anda yakin ingin menghapus "{item_name}"?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.itemDeleted.emit(item_id)
    
    def update_table(self, data_barang):
        self.setRowCount(0)
        
        for barang in data_barang:
            row = self.rowCount()
            self.insertRow(row)
            
            # Format harga dengan separator ribuan
            harga_text = f"Rp {barang.harga:,.0f}".replace(",", ".")
            
            # Warna stok
            stok_item = QTableWidgetItem(str(barang.stok))
            if barang.stok == 0:
                stok_item.setBackground(QBrush(QColor(255, 200, 200)))  # Merah untuk stok 0
                stok_item.setForeground(QBrush(QColor(255, 0, 0)))
            elif barang.stok < 5:
                stok_item.setBackground(QBrush(QColor(255, 255, 200)))  # Kuning untuk stok rendah
            
            # Tombol aksi
            widget_aksi = QWidget()
            layout_aksi = QHBoxLayout(widget_aksi)
            layout_aksi.setContentsMargins(5, 2, 5, 2)
            
            btn_tambah = QPushButton("➕")
            btn_tambah.setFixedSize(30, 25)
            btn_tambah.setToolTip("Tambah Stok")
            btn_tambah.clicked.connect(lambda checked, x=barang.id: self.stockAdded.emit(x, 0, ""))
            
            btn_kurang = QPushButton("➖")
            btn_kurang.setFixedSize(30, 25)
            btn_kurang.setToolTip("Kurangi Stok")
            btn_kurang.clicked.connect(lambda checked, x=barang.id: self.stockReduced.emit(x, 0, ""))
            
            layout_aksi.addWidget(btn_tambah)
            layout_aksi.addWidget(btn_kurang)
            layout_aksi.addStretch()
            
            items = [
                QTableWidgetItem(str(barang.id)),
                QTableWidgetItem(barang.nama),
                QTableWidgetItem(harga_text),
                QTableWidgetItem(barang.kategori),
                stok_item,
                QTableWidgetItem(""),  # Placeholder for action column
                QTableWidgetItem(barang.updated_at)
            ]
            
            for col, item in enumerate(items):
                if col != 5:  # Skip action column for item
                    item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(row, col, item)
            
            self.setCellWidget(row, 5, widget_aksi)