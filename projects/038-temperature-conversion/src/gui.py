import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from konversi_suhu import KonversiSuhu
from history_manager import HistoryManager

class AplikasiKonversiSuhu:
    def __init__(self, root):
        self.root = root
        self.root.title("Konversi Suhu")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Inisialisasi history manager
        self.history_manager = HistoryManager()
        
        # Buat style untuk tampilan yang lebih modern
        self.setup_style()
        
        # Buat notebook (tab)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Frame untuk konversi
        self.frame_konversi = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_konversi, text='Konversi Suhu')
        
        # Frame untuk history
        self.frame_history = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_history, text='Riwayat Konversi')
        
        # Setup komponen untuk konversi
        self.setup_konversi_frame()
        
        # Setup komponen untuk history
        self.setup_history_frame()
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))
    
    def setup_konversi_frame(self):
        # Judul
        label_judul = ttk.Label(self.frame_konversi, text="KONVERSI SUHU", 
                               font=('Arial', 16, 'bold'))
        label_judul.pack(pady=10)
        
        # Frame input
        frame_input = ttk.Frame(self.frame_konversi)
        frame_input.pack(pady=10, padx=20, fill='x')
        
        # Input nilai
        ttk.Label(frame_input, text="Nilai Suhu:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nilai = ttk.Entry(frame_input, font=('Arial', 12), width=15)
        self.entry_nilai.grid(row=0, column=1, padx=5, pady=5)
        
        # Satuan asal
        ttk.Label(frame_input, text="Dari Satuan:").grid(row=1, column=0, sticky='w', pady=5)
        self.combo_dari = ttk.Combobox(frame_input, values=['C', 'F', 'R', 'K'], 
                                      state='readonly', width=12)
        self.combo_dari.set('C')
        self.combo_dari.grid(row=1, column=1, padx=5, pady=5)
        
        # Satuan tujuan
        ttk.Label(frame_input, text="Ke Satuan:").grid(row=2, column=0, sticky='w', pady=5)
        self.combo_ke = ttk.Combobox(frame_input, values=['C', 'F', 'R', 'K'], 
                                    state='readonly', width=12)
        self.combo_ke.set('F')
        self.combo_ke.grid(row=2, column=1, padx=5, pady=5)
        
        # Tombol konversi
        btn_konversi = ttk.Button(frame_input, text="Konversi", command=self.konversi_suhu)
        btn_konversi.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame hasil
        frame_hasil = ttk.LabelFrame(self.frame_konversi, text="Hasil Konversi")
        frame_hasil.pack(pady=10, padx=20, fill='x')
        
        self.label_hasil = ttk.Label(frame_hasil, text="", font=('Arial', 14, 'bold'),
                                   foreground='blue')
        self.label_hasil.pack(pady=10)
        
        # Frame konversi cepat
        self.setup_konversi_cepat()
    
    def setup_konversi_cepat(self):
        frame_cepat = ttk.LabelFrame(self.frame_konversi, text="Konversi Cepat dari Celsius")
        frame_cepat.pack(pady=10, padx=20, fill='x')
        
        # Tombol konversi cepat
        btn_frame = ttk.Frame(frame_cepat)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="C → F", 
                  command=lambda: self.konversi_cepat('C', 'F')).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="C → R", 
                  command=lambda: self.konversi_cepat('C', 'R')).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="C → K", 
                  command=lambda: self.konversi_cepat('C', 'K')).grid(row=0, column=2, padx=5)
        
        ttk.Button(btn_frame, text="F → C", 
                  command=lambda: self.konversi_cepat('F', 'C')).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="R → C", 
                  command=lambda: self.konversi_cepat('R', 'C')).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="K → C", 
                  command=lambda: self.konversi_cepat('K', 'C')).grid(row=1, column=2, padx=5, pady=5)
    
    def setup_history_frame(self):
        # Judul
        label_judul = ttk.Label(self.frame_history, text="RIWAYAT KONVERSI", 
                               font=('Arial', 16, 'bold'))
        label_judul.pack(pady=10)
        
        # Tombol refresh dan clear
        frame_tombol = ttk.Frame(self.frame_history)
        frame_tombol.pack(pady=5)
        
        ttk.Button(frame_tombol, text="Refresh", command=self.tampilkan_history).pack(side='left', padx=5)
        ttk.Button(frame_tombol, text="Hapus Riwayat", command=self.hapus_history).pack(side='left', padx=5)
        
        # Area teks untuk menampilkan history
        self.text_history = scrolledtext.ScrolledText(self.frame_history, width=70, height=20,
                                                     font=('Arial', 10))
        self.text_history.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Tampilkan history saat pertama kali
        self.tampilkan_history()
    
    def konversi_suhu(self):
        try:
            nilai = float(self.entry_nilai.get())
            dari = self.combo_dari.get()
            ke = self.combo_ke.get()
            
            hasil = KonversiSuhu.konversi_suhu(nilai, dari, ke)
            
            # Format hasil dengan 2 angka desimal
            hasil_format = f"{hasil:.2f}"
            
            # Tampilkan hasil
            self.label_hasil.config(text=f"{nilai}°{dari} = {hasil_format}°{ke}")
            
            # Simpan ke history
            self.history_manager.add_entry(nilai, dari, float(hasil_format), ke)
            
        except ValueError as e:
            messagebox.showerror("Error", "Masukkan nilai yang valid!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def konversi_cepat(self, dari, ke):
        try:
            nilai = float(self.entry_nilai.get())
            hasil = KonversiSuhu.konversi_suhu(nilai, dari, ke)
            hasil_format = f"{hasil:.2f}"
            
            self.label_hasil.config(text=f"{nilai}°{dari} = {hasil_format}°{ke}")
            
            # Simpan ke history
            self.history_manager.add_entry(nilai, dari, float(hasil_format), ke)
            
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai yang valid terlebih dahulu!")
    
    def tampilkan_history(self):
        history = self.history_manager.get_history()
        self.text_history.delete(1.0, tk.END)
        
        if not history:
            self.text_history.insert(tk.END, "Belum ada riwayat konversi.")
            return
        
        for i, entry in enumerate(reversed(history), 1):
            self.text_history.insert(tk.END, 
                                   f"{i}. {entry['timestamp']}\n"
                                   f"   {entry['nilai_awal']}°{entry['satuan_awal']} → "
                                   f"{entry['nilai_hasil']}°{entry['satuan_hasil']}\n\n")
    
    def hapus_history(self):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua riwayat?"):
            self.history_manager.clear_history()
            self.tampilkan_history()