import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTabWidget, QMessageBox,
    QStatusBar, QToolBar, QAction, QMenu, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

from db_handler import DatabaseHandler
from widgets.table_widget import CustomTableWidget
from widgets.form_widget import FormInputBarang, StockManagementDialog
from widgets.statistics_widget import StatisticsWidget
from styles import setup_app_style, get_stylesheet
from utils.export_utils import ExportUtils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseHandler()
        self.export_utils = ExportUtils(self)
        self.export_utils.exportFinished.connect(self.on_export_finished)
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        self.setWindowTitle("🚀 Inventory Management System")
        self.setGeometry(100, 100, 1300, 800)
        
        # Setup central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("📦 INVENTORY MANAGEMENT SYSTEM")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(header)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cari barang... (nama atau kategori)")
        self.search_input.textChanged.connect(self.cari_barang)
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self.load_data)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(btn_refresh)
        layout.addLayout(search_layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Tab 1: Data Barang
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        
        # Form dan tabel dalam split layout
        form_tabel_layout = QHBoxLayout()
        
        # Form input (kiri)
        self.form_widget = FormInputBarang()
        self.form_widget.dataSubmitted.connect(self.handle_data_submit)
        self.form_widget.formCleared.connect(self.load_data)
        
        # Tabel (kanan)
        self.table_widget = CustomTableWidget()
        self.table_widget.itemDeleted.connect(self.hapus_barang)
        self.table_widget.itemEdited.connect(self.edit_barang)
        self.table_widget.stockAdded.connect(self.tambah_stok)
        self.table_widget.stockReduced.connect(self.kurangi_stok)
        
        form_tabel_layout.addWidget(self.form_widget, 1)
        form_tabel_layout.addWidget(self.table_widget, 2)
        
        tab1_layout.addLayout(form_tabel_layout)
        
        # Tab 2: Statistik
        self.statistics_widget = StatisticsWidget(self.db)
        
        self.tab_widget.addTab(tab1, "📊 Kelola Barang")
        self.tab_widget.addTab(self.statistics_widget, "📈 Statistik")
        
        layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage("✅ Sistem siap digunakan - Total barang: 0")
        
        # Setup toolbar
        self.setup_toolbar()
        
    def setup_toolbar(self):
        toolbar = QToolBar("Toolbar Utama")
        self.addToolBar(toolbar)
        
        # Aksi-aksi toolbar
        act_tambah = QAction("➕ Tambah Barang", self)
        act_refresh = QAction("🔄 Refresh", self)
        act_export = QAction("📤 Export Data", self)
        act_about = QAction("ℹ️ Tentang", self)
        
        act_tambah.triggered.connect(self.form_widget.clear_form)
        act_refresh.triggered.connect(self.load_data)
        act_export.triggered.connect(self.show_export_menu)
        act_about.triggered.connect(self.show_about)
        
        toolbar.addAction(act_tambah)
        toolbar.addAction(act_refresh)
        toolbar.addAction(act_export)
        toolbar.addAction(act_about)
    
    def show_export_menu(self):
        """Menampilkan menu pilihan format export"""
        menu = QMenu(self)
        
        csv_action = QAction("Export ke CSV", self)
        json_action = QAction("Export ke JSON", self)
        excel_action = QAction("Export ke Excel", self)
        
        csv_action.triggered.connect(lambda: self.export_data('csv'))
        json_action.triggered.connect(lambda: self.export_data('json'))
        excel_action.triggered.connect(lambda: self.export_data('excel'))
        
        menu.addAction(csv_action)
        menu.addAction(json_action)
        menu.addAction(excel_action)
        
        menu.exec_(self.mapToGlobal(self.toolBar().pos()))
    
    def export_data(self, format_type):
        """Export data berdasarkan format yang dipilih"""
        data_barang = self.db.get_all_barang()
        
        if not data_barang:
            QMessageBox.warning(self, "Peringatan", "Tidak ada data untuk diekspor!")
            return
        
        if format_type == 'csv':
            self.export_utils.export_to_csv(data_barang)
        elif format_type == 'json':
            self.export_utils.export_to_json(data_barang)
        elif format_type == 'excel':
            self.export_utils.export_to_excel(data_barang)
    
    def on_export_finished(self, success, message):
        """Handler setelah export selesai"""
        if success:
            QMessageBox.information(self, "Sukses", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def handle_data_submit(self, data):
        if 'id' in data:  # Mode edit
            if self.db.update_barang(data['id'], data):
                self.load_data()
                self.form_widget.set_tambah_mode()
        else:  # Mode tambah
            self.db.tambah_barang(data)
            self.load_data()
    
    def tambah_stok(self, id_barang, jumlah=None, keterangan=""):
        """Menambah stok barang"""
        barang = self.db.get_barang_by_id(id_barang)
        if not barang:
            return
        
        if jumlah is None or jumlah == 0:
            dialog = StockManagementDialog(barang, self)
            if dialog.exec_():
                data = dialog.get_data()
                if data['operation'] == "Tambah Stok":
                    if self.db.tambah_stok(id_barang, data['jumlah'], data['keterangan']):
                        self.load_data()
                        self.tab_widget.setCurrentIndex(1)  # Buka tab statistik
                        self.statistics_widget.refresh()
                        QMessageBox.information(self, "Sukses", 
                            f"Berhasil menambah {data['jumlah']} unit stok {barang.nama}")
        else:
            if self.db.tambah_stok(id_barang, jumlah, keterangan):
                self.load_data()
    
    def kurangi_stok(self, id_barang, jumlah=None, keterangan=""):
        """Mengurangi stok barang"""
        barang = self.db.get_barang_by_id(id_barang)
        if not barang:
            return
        
        if jumlah is None or jumlah == 0:
            dialog = StockManagementDialog(barang, self)
            if dialog.exec_():
                data = dialog.get_data()
                if data['operation'] == "Kurangi Stok":
                    if self.db.kurangi_stok(id_barang, data['jumlah'], data['keterangan']):
                        self.load_data()
                        self.tab_widget.setCurrentIndex(1)
                        self.statistics_widget.refresh()
                        QMessageBox.information(self, "Sukses", 
                            f"Berhasil mengurangi {data['jumlah']} unit stok {barang.nama}")
                    else:
                        QMessageBox.warning(self, "Peringatan", 
                            f"Stok tidak mencukupi! Stok saat ini: {barang.stok} unit")
        else:
            if self.db.kurangi_stok(id_barang, jumlah, keterangan):
                self.load_data()
    
    def load_data(self):
        data_barang = self.db.get_all_barang()
        self.table_widget.update_table(data_barang)
        
        # Update status bar
        total_barang = len(data_barang)
        total_nilai = sum(barang.harga * barang.stok for barang in data_barang)
        self.statusBar().showMessage(
            f"✅ Sistem siap digunakan - Total barang: {total_barang} | "
            f"Total nilai inventory: Rp {total_nilai:,.0f}".replace(",", ".")
        )
        
        # Refresh statistik jika tab statistik aktif
        if hasattr(self, 'statistics_widget'):
            self.statistics_widget.refresh()
    
    def hapus_barang(self, id_barang):
        if self.db.hapus_barang(id_barang):
            self.load_data()
            QMessageBox.information(self, "Sukses", "Barang berhasil dihapus!")
    
    def edit_barang(self, id_barang):
        barang = self.db.get_barang_by_id(id_barang)
        if barang:
            self.form_widget.set_edit_mode(barang)
            self.tab_widget.setCurrentIndex(0)
    
    def cari_barang(self):
        keyword = self.search_input.text().strip()
        if keyword:
            results = self.db.cari_barang(keyword)
            self.table_widget.update_table(results)
        else:
            self.load_data()
    
    def show_about(self):
        QMessageBox.about(self, "Tentang Aplikasi",
                        "🚀 Inventory Management System\n\n"
                        "Fitur Utama:\n"
                        "• Manajemen barang lengkap (CRUD)\n"
                        "• Manajemen stok (tambah/kurangi stok)\n"
                        "• Pencarian real-time\n"
                        "• Statistik dan analisis inventory\n"
                        "• Riwayat transaksi stok\n"
                        "• Export data (CSV, JSON, Excel)\n"
                        "• Interface modern dan user-friendly\n\n"
                        "Dibuat dengan PyQt5\n"
                        "Versi 2.0")

def main():
    app = QApplication(sys.argv)
    
    # Setup styling
    setup_app_style(app)
    app.setStyleSheet(get_stylesheet())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()