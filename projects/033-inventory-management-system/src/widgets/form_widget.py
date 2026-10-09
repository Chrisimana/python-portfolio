from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QMessageBox, QDialog, QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator

class FormInputBarang(QWidget):
    dataSubmitted = pyqtSignal(dict)
    formCleared = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.mode_tambah = True
        self.current_id = None
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Group box untuk form
        group_box = QGroupBox("Form Input Barang")
        group_box.setFont(QFont("Arial", 10, QFont.Bold))
        
        form_layout = QGridLayout()
        
        # Input fields
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Masukkan nama barang...")
        
        self.harga_input = QLineEdit()
        self.harga_input.setPlaceholderText("0")
        self.harga_input.setValidator(QDoubleValidator(0, 999999999, 2))
        
        self.kategori_combo = QComboBox()
        self.kategori_combo.addItems(["Elektronik", "Pakaian", "Makanan", "Minuman", "Alat Tulis", "Olahraga", "Kesehatan", "Umum"])
        
        self.stok_spin = QSpinBox()
        self.stok_spin.setRange(0, 9999)
        self.stok_spin.setValue(1)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_submit = QPushButton("➕ Tambah Barang")
        self.btn_clear = QPushButton("🗑️ Bersihkan")
        
        self.btn_submit.clicked.connect(self.submit_data)
        self.btn_clear.clicked.connect(self.clear_form)
        
        button_layout.addWidget(self.btn_submit)
        button_layout.addWidget(self.btn_clear)
        
        # Add to form layout
        form_layout.addWidget(QLabel("Nama Barang:"), 0, 0)
        form_layout.addWidget(self.nama_input, 0, 1)
        form_layout.addWidget(QLabel("Harga (Rp):"), 1, 0)
        form_layout.addWidget(self.harga_input, 1, 1)
        form_layout.addWidget(QLabel("Kategori:"), 2, 0)
        form_layout.addWidget(self.kategori_combo, 2, 1)
        form_layout.addWidget(QLabel("Stok:"), 3, 0)
        form_layout.addWidget(self.stok_spin, 3, 1)
        
        group_box.setLayout(form_layout)
        layout.addWidget(group_box)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def submit_data(self):
        nama = self.nama_input.text().strip()
        harga_text = self.harga_input.text().strip()
        
        if not nama:
            QMessageBox.warning(self, "Peringatan", "Nama barang harus diisi!")
            self.nama_input.setFocus()
            return
        
        if not harga_text:
            QMessageBox.warning(self, "Peringatan", "Harga barang harus diisi!")
            self.harga_input.setFocus()
            return
        
        try:
            harga = float(harga_text)
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Format harga tidak valid!")
            self.harga_input.setFocus()
            return
        
        data = {
            'nama': nama,
            'harga': harga,
            'kategori': self.kategori_combo.currentText(),
            'stok': self.stok_spin.value()
        }
        
        if self.mode_tambah:
            self.dataSubmitted.emit(data)
            self.clear_form()
            QMessageBox.information(self, "Sukses", "Barang berhasil ditambahkan!")
        else:
            data['id'] = self.current_id
            self.dataSubmitted.emit(data)
            QMessageBox.information(self, "Sukses", "Barang berhasil diupdate!")
    
    def clear_form(self):
        self.nama_input.clear()
        self.harga_input.clear()
        self.kategori_combo.setCurrentIndex(0)
        self.stok_spin.setValue(1)
        self.set_tambah_mode()
        self.formCleared.emit()
    
    def set_tambah_mode(self):
        self.mode_tambah = True
        self.current_id = None
        self.btn_submit.setText("➕ Tambah Barang")
    
    def set_edit_mode(self, barang):
        self.mode_tambah = False
        self.current_id = barang.id
        self.nama_input.setText(barang.nama)
        self.harga_input.setText(str(int(barang.harga)))
        self.kategori_combo.setCurrentText(barang.kategori)
        self.stok_spin.setValue(barang.stok)
        self.btn_submit.setText("💾 Update Barang")


class StockManagementDialog(QDialog):
    """Dialog untuk manajemen stok (tambah/kurangi)"""
    def __init__(self, barang, parent=None):
        super().__init__(parent)
        self.barang = barang
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle(f"Manajemen Stok - {self.barang.nama}")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Info barang
        info_group = QGroupBox("Informasi Barang")
        info_layout = QFormLayout()
        info_layout.addRow("Nama Barang:", QLabel(self.barang.nama))
        info_layout.addRow("Kategori:", QLabel(self.barang.kategori))
        info_layout.addRow("Harga:", QLabel(f"Rp {self.barang.harga:,.0f}".replace(",", ".")))
        info_layout.addRow("Stok Saat Ini:", QLabel(f"{self.barang.stok} unit"))
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Pilihan operasi
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Tambah Stok", "Kurangi Stok"])
        self.operation_combo.currentTextChanged.connect(self.on_operation_changed)
        layout.addWidget(QLabel("Jenis Operasi:"))
        layout.addWidget(self.operation_combo)
        
        # Jumlah
        layout.addWidget(QLabel("Jumlah:"))
        self.jumlah_spin = QSpinBox()
        self.jumlah_spin.setRange(1, 9999)
        self.jumlah_spin.setValue(1)
        layout.addWidget(self.jumlah_spin)
        
        # Keterangan
        layout.addWidget(QLabel("Keterangan:"))
        self.keterangan_input = QLineEdit()
        self.keterangan_input.setPlaceholderText("Opsional...")
        layout.addWidget(self.keterangan_input)
        
        # Warning label
        self.warning_label = QLabel()
        self.warning_label.setStyleSheet("color: red;")
        layout.addWidget(self.warning_label)
        
        # Buttons
        button_box = QDialogButtonBox()
        self.btn_ok = button_box.addButton("Proses", QDialogButtonBox.AcceptRole)
        self.btn_cancel = button_box.addButton("Batal", QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def on_operation_changed(self, text):
        if text == "Kurangi Stok":
            self.warning_label.setText(f"Peringatan: Stok saat ini {self.barang.stok} unit")
        else:
            self.warning_label.setText("")
    
    def get_data(self):
        return {
            'operation': self.operation_combo.currentText(),
            'jumlah': self.jumlah_spin.value(),
            'keterangan': self.keterangan_input.text().strip() or 
                         (f"{self.operation_combo.currentText()} stok")
        }