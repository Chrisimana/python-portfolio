from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QListWidget, QLineEdit, QPushButton, QMessageBox,
    QTabWidget, QTextEdit, QComboBox, QCheckBox,
    QGroupBox, QListWidgetItem, QProgressBar, QSplitter
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ AGENDA MANAGER ✨")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_ui()
    
    # Setup UI components
    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter untuk responsive layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Input dan kontrol
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Title
        title_label = QLabel("AGENDA MANAGER")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; padding: 20px;")
        
        # Form input
        form_group = QGroupBox("Tambah Agenda Baru")
        form_layout = QGridLayout(form_group)
        
        self.input_judul = QLineEdit()
        self.input_judul.setPlaceholderText("Judul agenda...")
        
        self.input_deskripsi = QTextEdit()
        self.input_deskripsi.setMaximumHeight(80)
        self.input_deskripsi.setPlaceholderText("Deskripsi agenda...")
        
        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems(["Pekerjaan", "Pribadi", "Belajar", "Kesehatan", "Keuangan", "Lainnya"])
        
        self.combo_prioritas = QComboBox()
        self.combo_prioritas.addItems(["Tinggi", "Sedang", "Rendah"])
        
        self.input_deadline = QLineEdit()
        self.input_deadline.setPlaceholderText("YYYY-MM-DD")
        
        self.check_selesai = QCheckBox("Tandai sebagai selesai")
        
        form_layout.addWidget(QLabel("Judul*:"), 0, 0)
        form_layout.addWidget(self.input_judul, 0, 1)
        form_layout.addWidget(QLabel("Kategori:"), 1, 0)
        form_layout.addWidget(self.combo_kategori, 1, 1)
        form_layout.addWidget(QLabel("Prioritas:"), 2, 0)
        form_layout.addWidget(self.combo_prioritas, 2, 1)
        form_layout.addWidget(QLabel("Deadline:"), 3, 0)
        form_layout.addWidget(self.input_deadline, 3, 1)
        form_layout.addWidget(QLabel("Deskripsi:"), 4, 0)
        form_layout.addWidget(self.input_deskripsi, 4, 1)
        form_layout.addWidget(self.check_selesai, 5, 1)
        
        # Tombol aksi
        button_layout = QHBoxLayout()
        self.btn_tambah = QPushButton("➕ Tambah Agenda")
        self.btn_hapus = QPushButton("🗑️ Hapus")
        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_tandai = QPushButton("✅ Tandai Selesai")
        
        button_layout.addWidget(self.btn_tambah)
        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_tandai)
        button_layout.addWidget(self.btn_hapus)
        
        # Statistik
        stats_group = QGroupBox("Statistik")
        stats_layout = QGridLayout(stats_group)
        
        self.label_total = QLabel("Total: 0")
        self.label_selesai = QLabel("Selesai: 0")
        self.label_belum_selesai = QLabel("Belum Selesai: 0")
        self.label_prioritas_tinggi = QLabel("Prioritas Tinggi: 0")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        
        stats_layout.addWidget(self.label_total, 0, 0)
        stats_layout.addWidget(self.label_selesai, 0, 1)
        stats_layout.addWidget(self.label_belum_selesai, 1, 0)
        stats_layout.addWidget(self.label_prioritas_tinggi, 1, 1)
        stats_layout.addWidget(self.progress_bar, 2, 0, 1, 2)
        
        # Assemble left panel
        left_layout.addWidget(title_label)
        left_layout.addWidget(form_group)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(stats_group)
        left_layout.addStretch()
        
        # Right panel - Tampilan agenda
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Tab semua agenda
        self.tab_semua = QWidget()
        layout_semua = QVBoxLayout(self.tab_semua)
        
        self.list_agenda = QListWidget()
        layout_semua.addWidget(self.list_agenda)
        
        # Tab berdasarkan kategori
        self.tab_kategori = QWidget()
        layout_kategori = QVBoxLayout(self.tab_kategori)
        
        self.combo_filter_kategori = QComboBox()
        self.combo_filter_kategori.addItems(["Semua", "Pekerjaan", "Pribadi", "Belajar", "Kesehatan", "Keuangan", "Lainnya"])
        self.list_agenda_kategori = QListWidget()
        
        layout_kategori.addWidget(QLabel("Filter Kategori:"))
        layout_kategori.addWidget(self.combo_filter_kategori)
        layout_kategori.addWidget(self.list_agenda_kategori)
        
        # Tab prioritas tinggi
        self.tab_prioritas = QWidget()
        layout_prioritas = QVBoxLayout(self.tab_prioritas)
        
        self.list_agenda_prioritas = QListWidget()
        layout_prioritas.addWidget(self.list_agenda_prioritas)
        
        # Add tabs
        self.tab_widget.addTab(self.tab_semua, "📋 Semua Agenda")
        self.tab_widget.addTab(self.tab_kategori, "📂 Berdasarkan Kategori")
        self.tab_widget.addTab(self.tab_prioritas, "🚨 Prioritas Tinggi")
        
        right_layout.addWidget(self.tab_widget)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
    
    # Mendapatkan data input dari form
    def dapatkan_input_agenda(self):
        return {
            'judul': self.input_judul.text().strip(),
            'deskripsi': self.input_deskripsi.toPlainText().strip(),
            'kategori': self.combo_kategori.currentText(),
            'prioritas': self.combo_prioritas.currentIndex() + 1,  # 1,2,3
            'deadline': self.input_deadline.text().strip(),
            'selesai': self.check_selesai.isChecked()
        }
    
    # Mengosongkan form input
    def kosongkan_form(self):
        self.input_judul.clear()
        self.input_deskripsi.clear()
        self.combo_kategori.setCurrentIndex(0)
        self.combo_prioritas.setCurrentIndex(1)  # Sedang
        self.input_deadline.clear()
        self.check_selesai.setChecked(False)
    
    # Menampilkan statistik
    def tampilkan_statistik(self, statistik):
        self.label_total.setText(f"Total: {statistik['total']}")
        self.label_selesai.setText(f"Selesai: {statistik['selesai']}")
        self.label_belum_selesai.setText(f"Belum Selesai: {statistik['belum_selesai']}")
        self.label_prioritas_tinggi.setText(f"Prioritas Tinggi: {statistik['prioritas_tinggi']}")
        
        # Progress bar
        if statistik['total'] > 0:
            progress = int((statistik['selesai'] / statistik['total']) * 100)
            self.progress_bar.setValue(progress)
            self.progress_bar.setFormat(f"{progress}% Selesai")
        else:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("0% Selesai")
    
    # Menampilkan pesan dialog
    def tampilkan_pesan(self, judul: str, pesan: str, tipe: str = "info"):
        if tipe == "info":
            QMessageBox.information(self, judul, pesan)
        elif tipe == "warning":
            QMessageBox.warning(self, judul, pesan)
        elif tipe == "error":
            QMessageBox.critical(self, judul, pesan)