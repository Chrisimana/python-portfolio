from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from model import ModelAgenda, AgendaItem
from gui import MainWindow

class ControllerAgenda(QObject):
    def __init__(self):
        super().__init__()
        self.model = ModelAgenda()
        self.view = MainWindow()
        
        # Koneksi sinyal-sinyal
        self.setup_koneksi()
        
        # Muat data awal
        self.muat_data_awal()
    
    # Setup koneksi antara view dan controller
    def setup_koneksi(self):
        # Tombol-tombol
        self.view.btn_tambah.clicked.connect(self.proses_tambah_agenda)
        self.view.btn_hapus.clicked.connect(self.proses_hapus_agenda)
        self.view.btn_edit.clicked.connect(self.proses_edit_agenda)
        self.view.btn_tandai.clicked.connect(self.proses_tandai_selesai)
        
        # Filter
        self.view.combo_filter_kategori.currentTextChanged.connect(self.filter_berdasarkan_kategori)
    
    # Memuat data awal saat aplikasi dimulai
    def muat_data_awal(self):
        agenda_items = self.model.dapatkan_semua_agenda()
        self.tampilkan_agenda_di_list(agenda_items)
        
        statistik = self.model.dapatkan_statistik()
        self.view.tampilkan_statistik(statistik)
    
    # Menampilkan agenda di list widget
    def tampilkan_agenda_di_list(self, agenda_items):
        self.view.list_agenda.clear()
        
        for item in agenda_items:
            # Format tampilan agenda
            status = "✅" if item.selesai else "⏳"
            prioritas_icon = "🚨" if item.prioritas == 1 else "⚠️" if item.prioritas == 2 else "📌"
            
            display_text = f"{status} {prioritas_icon} {item.judul}"
            if item.deadline:
                display_text += f" | ⏰ {item.deadline}"
            if item.deskripsi:
                display_text += f" | 📝 {item.deskripsi[:30]}..."
            
            list_item = QListWidgetItem(display_text)
            list_item.setData(1, item.id)  # Qt.UserRole = 1
            
            # Styling berdasarkan status dan prioritas
            if item.selesai:
                list_item.setForeground(self.view.palette().color(self.view.foregroundRole()).lighter(150))
            elif item.prioritas == 1:
                list_item.setBackground(self.view.palette().highlight())
            
            self.view.list_agenda.addItem(list_item)
    
    # Proses penambahan agenda baru
    def proses_tambah_agenda(self):
        data = self.view.dapatkan_input_agenda()
        
        if not data['judul']:
            self.view.tampilkan_pesan("Peringatan", "Judul agenda tidak boleh kosong!", "warning")
            return
        
        # Buat agenda item baru
        agenda_item = AgendaItem(
            judul=data['judul'],
            deskripsi=data['deskripsi'],
            kategori=data['kategori'],
            prioritas=data['prioritas'],
            deadline=data['deadline'],
            selesai=data['selesai']
        )
        
        # Tambah ke model
        if self.model.tambah_agenda(agenda_item):
            self.view.tampilkan_pesan("Sukses", "Agenda berhasil ditambahkan!", "info")
            self.view.kosongkan_form()
            
            # Update tampilan
            self.muat_data_awal()
        else:
            self.view.tampilkan_pesan("Error", "Gagal menambahkan agenda!", "error")
    
    # Proses penghapusan agenda
    def proses_hapus_agenda(self):
        selected_item = self.view.list_agenda.currentItem()
        if not selected_item:
            self.view.tampilkan_pesan("Peringatan", "Pilih agenda yang akan dihapus!", "warning")
            return
        
        agenda_id = selected_item.data(1)  # Qt.UserRole
        
        # Konfirmasi hapus
        reply = QMessageBox.question(
            self.view, "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus agenda ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.model.hapus_agenda(agenda_id):
                self.view.tampilkan_pesan("Sukses", "Agenda berhasil dihapus!", "info")
                self.muat_data_awal()
    
    # Proses pengeditan agenda
    def proses_edit_agenda(self):
        selected_item = self.view.list_agenda.currentItem()
        if not selected_item:
            self.view.tampilkan_pesan("Peringatan", "Pilih agenda yang akan diedit!", "warning")
            return
        
        agenda_id = selected_item.data(1)  # Qt.UserRole
        agenda_item = self.model.dapatkan_agenda_by_id(agenda_id)
        
        if agenda_item:
            # Isi form dengan data existing
            self.view.input_judul.setText(agenda_item.judul)
            self.view.input_deskripsi.setPlainText(agenda_item.deskripsi)
            
            # Set kategori
            index = self.view.combo_kategori.findText(agenda_item.kategori)
            if index >= 0:
                self.view.combo_kategori.setCurrentIndex(index)
            
            # Set prioritas (1-based to 0-based)
            self.view.combo_prioritas.setCurrentIndex(agenda_item.prioritas - 1)
            self.view.input_deadline.setText(agenda_item.deadline)
            self.view.check_selesai.setChecked(agenda_item.selesai)
            
            # Ubah tombol tambah menjadi update
            self.view.btn_tambah.setText("🔄 Update Agenda")
            self.view.btn_tambah.disconnect()
            self.view.btn_tambah.clicked.connect(lambda: self.proses_update_agenda(agenda_id))
    
    # Proses update agenda
    def proses_update_agenda(self, agenda_id: int):
        data = self.view.dapatkan_input_agenda()
        
        if not data['judul']:
            self.view.tampilkan_pesan("Peringatan", "Judul agenda tidak boleh kosong!", "warning")
            return
        
        if self.model.update_agenda(agenda_id, **data):
            self.view.tampilkan_pesan("Sukses", "Agenda berhasil diupdate!", "info")
            self.view.kosongkan_form()
            
            # Kembalikan tombol ke mode tambah
            self.view.btn_tambah.setText("➕ Tambah Agenda")
            self.view.btn_tambah.disconnect()
            self.view.btn_tambah.clicked.connect(self.proses_tambah_agenda)
            
            self.muat_data_awal()
    
    # Proses menandai agenda sebagai selesai
    def proses_tandai_selesai(self):
        selected_item = self.view.list_agenda.currentItem()
        if not selected_item:
            self.view.tampilkan_pesan("Peringatan", "Pilih agenda yang akan ditandai selesai!", "warning")
            return
        
        agenda_id = selected_item.data(1)  # Qt.UserRole
        
        if self.model.update_agenda(agenda_id, selesai=True):
            self.view.tampilkan_pesan("Sukses", "Agenda ditandai sebagai selesai!", "info")
            self.muat_data_awal()
    
    # Filter agenda berdasarkan kategori
    def filter_berdasarkan_kategori(self, kategori: str):
        if kategori == "Semua":
            agenda_items = self.model.dapatkan_semua_agenda()
        else:
            agenda_items = self.model.dapatkan_agenda_by_kategori(kategori)
        
        self.view.list_agenda_kategori.clear()
        for item in agenda_items:
            display_text = f"{'✅' if item.selesai else '⏳'} {item.judul}"
            if item.deadline:
                display_text += f" | ⏰ {item.deadline}"
            
            list_item = QListWidgetItem(display_text)
            self.view.list_agenda_kategori.addItem(list_item)
    
    # Menjalankan aplikasi
    def jalankan(self):
        self.view.show()