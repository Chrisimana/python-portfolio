import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkFont
from diskon_core import DiskonCalculator
from history_manager import HistoryManager

class AplikasiDiskon:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Diskon")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f8ff')
        
        # Inisialisasi manager history
        self.history_manager = HistoryManager()
        
        # Setup font
        self.font_title = tkFont.Font(family="Arial", size=16, weight="bold")
        self.font_normal = tkFont.Font(family="Arial", size=10)
        self.font_result = tkFont.Font(family="Arial", size=12, weight="bold")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Judul
        title_label = ttk.Label(main_frame, text="KALKULATOR DISKON", 
                               font=self.font_title, foreground="#2c3e50")
        title_label.pack(pady=10)
        
        # Frame input
        input_frame = ttk.LabelFrame(main_frame, text="Input Data", padding="15")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Input harga asal
        ttk.Label(input_frame, text="Harga Asal (Rp):", font=self.font_normal).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_harga = ttk.Entry(input_frame, font=self.font_normal, width=20)
        self.entry_harga.grid(row=0, column=1, padx=10, pady=5)
        
        # Input diskon
        ttk.Label(input_frame, text="Diskon (%):", font=self.font_normal).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_diskon = ttk.Entry(input_frame, font=self.font_normal, width=20)
        self.entry_diskon.grid(row=1, column=1, padx=10, pady=5)
        
        # Frame tombol
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Tombol hitung
        self.btn_hitung = ttk.Button(button_frame, text="Hitung Diskon", 
                                   command=self.hitung_diskon)
        self.btn_hitung.pack(side=tk.LEFT, padx=5)
        
        # Tombol reset
        self.btn_reset = ttk.Button(button_frame, text="Reset", 
                                  command=self.reset_input)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        # Frame hasil
        result_frame = ttk.LabelFrame(main_frame, text="Hasil Perhitungan", padding="15")
        result_frame.pack(fill=tk.X, pady=10)
        
        # Label hasil
        self.label_hasil = ttk.Label(result_frame, text="Masukkan harga dan diskon untuk melihat hasil", 
                                   font=self.font_result, foreground="#e74c3c")
        self.label_hasil.pack(pady=10)
        
        # Detail perhitungan
        self.label_detail = ttk.Label(result_frame, text="", font=self.font_normal)
        self.label_detail.pack(pady=5)
        
        # Frame history
        history_frame = ttk.LabelFrame(main_frame, text="Riwayat Perhitungan", padding="15")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tombol history
        history_btn_frame = ttk.Frame(history_frame)
        history_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(history_btn_frame, text="Muat Ulang History", 
                  command=self.tampilkan_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(history_btn_frame, text="Hapus History", 
                  command=self.hapus_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(history_btn_frame, text="Export ke CSV", 
                  command=self.export_history).pack(side=tk.LEFT, padx=5)
        
        # Text area untuk history
        self.history_text = scrolledtext.ScrolledText(history_frame, height=10, 
                                                     font=("Consolas", 9))
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Tampilkan history saat pertama kali dibuka
        self.tampilkan_history()
        
        # Bind Enter key untuk memudahkan input
        self.entry_harga.bind('<Return>', lambda e: self.entry_diskon.focus())
        self.entry_diskon.bind('<Return>', lambda e: self.hitung_diskon())
    
    # Menghitung diskon berdasarkan input user
    def hitung_diskon(self):
        harga_str = self.entry_harga.get().strip()
        diskon_str = self.entry_diskon.get().strip()
        
        # Validasi input harga
        valid_harga, result_harga = DiskonCalculator.validasi_input_harga(harga_str)
        if not valid_harga:
            messagebox.showerror("Error Input", result_harga)
            self.entry_harga.focus()
            return
        
        # Validasi input diskon
        valid_diskon, result_diskon = DiskonCalculator.validasi_input_diskon(diskon_str)
        if not valid_diskon:
            messagebox.showerror("Error Input", result_diskon)
            self.entry_diskon.focus()
            return
        
        # Hitung diskon
        try:
            harga_asal = float(result_harga)
            diskon = float(result_diskon)
            harga_diskon = DiskonCalculator.hitung_diskon(harga_asal, diskon)
            
            # Tampilkan hasil
            self.tampilkan_hasil(harga_asal, diskon, harga_diskon)
            
            # Simpan ke history
            self.history_manager.tambah_history(harga_asal, diskon, harga_diskon)
            
            # Update history display
            self.tampilkan_history()
            
        except Exception as e:
            messagebox.showerror("Error Perhitungan", f"Terjadi kesalahan: {str(e)}")
    
    # Menampilkan hasil perhitungan
    def tampilkan_hasil(self, harga_asal, diskon, harga_diskon):
        harga_asal_fmt = f"Rp {harga_asal:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        harga_diskon_fmt = f"Rp {harga_diskon:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        selisih = harga_asal - harga_diskon
        selisih_fmt = f"Rp {selisih:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        
        self.label_hasil.config(text=f"Harga Setelah Diskon: {harga_diskon_fmt}", 
                              foreground="#27ae60")
        
        detail_text = (f"Harga Asal: {harga_asal_fmt}\n"
                      f"Diskon: {diskon}%\n"
                      f"Total Diskon: {selisih_fmt}")
        self.label_detail.config(text=detail_text)
    
    # Reset input dan hasil
    def reset_input(self):
        self.entry_harga.delete(0, tk.END)
        self.entry_diskon.delete(0, tk.END)
        self.label_hasil.config(text="Masukkan harga dan diskon untuk melihat hasil", 
                              foreground="#e74c3c")
        self.label_detail.config(text="")
        self.entry_harga.focus()
    
    # Menampilkan history di text area
    def tampilkan_history(self):
        history = self.history_manager.get_history()
        self.history_text.delete(1.0, tk.END)
        
        if not history:
            self.history_text.insert(tk.END, "Belum ada riwayat perhitungan.")
            return
        
        # Header tabel
        header = f"{'Waktu':<20} {'Harga Asal':<15} {'Diskon':<8} {'Harga Diskon':<15}\n"
        separator = "-" * 65 + "\n"
        self.history_text.insert(tk.END, header)
        self.history_text.insert(tk.END, separator)
        
        # Data history (tampilkan 10 terakhir)
        for entry in history[-10:]:
            harga_asal_fmt = f"Rp {entry['harga_asal']:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            harga_diskon_fmt = f"Rp {entry['harga_diskon']:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            row = (f"{entry['timestamp']:<20} {harga_asal_fmt:<15} "
                  f"{entry['diskon']:<8} {harga_diskon_fmt:<15}\n")
            self.history_text.insert(tk.END, row)
    
    # Menghapus semua riwayat perhitungan
    def hapus_history(self):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua riwayat?"):
            self.history_manager.hapus_history()
            self.tampilkan_history()
            messagebox.showinfo("Sukses", "Riwayat berhasil dihapus!")
    
    # Mengekspor history ke file CSV
    def export_history(self):
        if self.history_manager.export_to_csv():
            messagebox.showinfo("Sukses", "History berhasil diexport ke file 'history_diskon.csv'")
        else:
            messagebox.showerror("Error", "Gagal mengekspor history ke CSV")