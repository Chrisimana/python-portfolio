import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fibonacci_calculator import FibonacciCalculator
from history_manager import ManajerRiwayat

class AntarmukaFibonacci:
    def __init__(self, root):
        self.root = root
        self.root.title("Generator Deret Fibonacci")
        self.root.geometry("1000x750")
        self.root.configure(bg='#f0f0f0')
        
        # Inisialisasi komponen
        self.kalkulator = FibonacciCalculator()
        self.manajer_riwayat = ManajerRiwayat()
        
        # Setup GUI
        self._setup_gui()
        
    def _setup_gui(self):
        # Header
        frame_header = tk.Frame(self.root, bg='#2c3e50', height=100)
        frame_header.pack(fill=tk.X, padx=10, pady=10)
        frame_header.pack_propagate(False)
        
        label_judul = tk.Label(frame_header, text="Generator Deret Fibonacci", 
                              font=('Arial', 22, 'bold'), fg='white', bg='#2c3e50')
        label_judul.pack(expand=True)
        
        label_subjudul = tk.Label(frame_header, 
                                 text="Hasilkan, Visualisasikan & Analisis Deret Fibonacci", 
                                 font=('Arial', 11), fg='#ecf0f1', bg='#2c3e50')
        label_subjudul.pack(expand=True)
        
        # Frame utama
        frame_utama = tk.Frame(self.root, bg='#f0f0f0')
        frame_utama.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame input
        self._buat_frame_input(frame_utama)
        
        # Frame hasil
        self._buat_frame_hasil(frame_utama)
        
        # Frame riwayat
        self._buat_frame_riwayat(frame_utama)
        
        # Status bar
        self._buat_status_bar()
        
        # Muat riwayat awal
        self._perbarui_riwayat()
    
    def _buat_frame_input(self, parent):

        # Membuat frame untuk input parameter
        frame_input = tk.LabelFrame(parent, text="Parameter Input", 
                                   font=('Arial', 12, 'bold'),
                                   bg='#f0f0f0', fg='#2c3e50', padx=15, pady=15)
        frame_input.pack(fill=tk.X, pady=(0, 10))
        
        # Input N
        tk.Label(frame_input, text="Masukkan N (jumlah suku Fibonacci):", 
                font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, sticky=tk.W, pady=8)
        
        self.entry_n = tk.Entry(frame_input, font=('Arial', 12), width=12, justify=tk.CENTER)
        self.entry_n.grid(row=0, column=1, padx=10, pady=8)
        self.entry_n.bind('<Return>', lambda event: self._generate_fibonacci())
        
        # Tombol aksi
        self.tombol_generate = tk.Button(frame_input, text="Hasilkan Deret", 
                                        font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                                        command=self._generate_fibonacci, width=15)
        self.tombol_generate.grid(row=0, column=2, padx=10, pady=8)
        
        self.tombol_clear = tk.Button(frame_input, text="Bersihkan", 
                                     font=('Arial', 10), bg='#e74c3c', fg='white',
                                     command=self._bersihkan_semua, width=10)
        self.tombol_clear.grid(row=0, column=3, padx=10, pady=8)
        
        # Opsi tambahan
        frame_opsi = tk.Frame(frame_input, bg='#f0f0f0')
        frame_opsi.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=8)
        
        self.var_tampil_grafik = tk.BooleanVar(value=True)
        self.var_tampil_statistik = tk.BooleanVar(value=True)
        
        tk.Checkbutton(frame_opsi, text="Tampilkan Grafik", 
                      variable=self.var_tampil_grafik,
                      bg='#f0f0f0', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 20))
        tk.Checkbutton(frame_opsi, text="Tampilkan Statistik", 
                      variable=self.var_tampil_statistik,
                      bg='#f0f0f0', font=('Arial', 9)).pack(side=tk.LEFT)
    
    def _buat_frame_hasil(self, parent):

        # Membuat frame untuk menampilkan hasil
        frame_hasil = tk.LabelFrame(parent, text="Hasil", font=('Arial', 12, 'bold'),
                                   bg='#f0f0f0', fg='#2c3e50', padx=15, pady=15)
        frame_hasil.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Notebook untuk tab
        self.notebook = ttk.Notebook(frame_hasil)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab deret
        self._buat_tab_deret()
        
        # Tab grafik
        self._buat_tab_grafik()
        
        # Tab statistik
        self._buat_tab_statistik()
    
    def _buat_tab_deret(self):

        # Membuat tab untuk menampilkan deret Fibonacci
        frame_tab_deret = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame_tab_deret, text="Deret Fibonacci")
        
        self.text_deret = scrolledtext.ScrolledText(frame_tab_deret, wrap=tk.WORD, 
                                                   font=('Consolas', 10), height=10)
        self.text_deret.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _buat_tab_grafik(self):

        # Membuat tab untuk menampilkan grafik
        self.frame_tab_grafik = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.frame_tab_grafik, text="Visualisasi Grafik")
    
    def _buat_tab_statistik(self):

        # Membuat tab untuk menampilkan statistik
        frame_tab_statistik = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame_tab_statistik, text="Analisis Statistik")
        
        self.text_statistik = scrolledtext.ScrolledText(frame_tab_statistik, wrap=tk.WORD, 
                                                       font=('Consolas', 10), height=10)
        self.text_statistik.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _buat_frame_riwayat(self, parent):

        # Membuat frame untuk menampilkan riwayat perhitungan
        frame_riwayat = tk.LabelFrame(parent, text="Riwayat Perhitungan", 
                                     font=('Arial', 12, 'bold'),
                                     bg='#f0f0f0', fg='#2c3e50', padx=15, pady=15)
        frame_riwayat.pack(fill=tk.BOTH, expand=True)
        
        # Kontrol riwayat
        frame_kontrol_riwayat = tk.Frame(frame_riwayat, bg='#f0f0f0')
        frame_kontrol_riwayat.pack(fill=tk.X, pady=(0, 8))
        
        tk.Button(frame_kontrol_riwayat, text="Segarkan Riwayat", font=('Arial', 9),
                 command=self._perbarui_riwayat).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(frame_kontrol_riwayat, text="Bersihkan Riwayat", font=('Arial', 9),
                 command=self._bersihkan_riwayat).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(frame_kontrol_riwayat, text="Ekspor Riwayat", font=('Arial', 9),
                 command=self._ekspor_riwayat).pack(side=tk.LEFT)
        
        # Listbox riwayat
        self.listbox_riwayat = tk.Listbox(frame_riwayat, font=('Arial', 9), height=8)
        self.listbox_riwayat.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox_riwayat.bind('<Double-Button-1>', self._muat_dari_riwayat)
    
    def _buat_status_bar(self):

        # Membuat status bar
        self.var_status = tk.StringVar()
        self.var_status.set("Siap menghasilkan deret Fibonacci")
        status_bar = tk.Label(self.root, textvariable=self.var_status, relief=tk.SUNKEN, 
                             anchor=tk.W, bg='#34495e', fg='white', font=('Arial', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _generate_fibonacci(self):

        # Menghasilkan deret Fibonacci berdasarkan input pengguna
        try:
            n = int(self.entry_n.get())
            
            if n <= 0:
                messagebox.showerror("Error Input", "Masukkan bilangan bulat positif!")
                return
            elif n > 1000:
                if not messagebox.askyesno("Input Besar", 
                                          f"Menghasilkan {n} suku Fibonacci mungkin membutuhkan waktu. Lanjutkan?"):
                    return
            
            self.var_status.set("Sedang menghasilkan deret Fibonacci...")
            self.root.update()
            
            # Hitung deret Fibonacci
            deret = self.kalkulator.hitung_fibonacci(n)
            
            # Tampilkan hasil
            self._tampilkan_deret(deret)
            
            # Tampilkan grafik jika diminta
            if self.var_tampil_grafik.get():
                self._tampilkan_grafik(deret)
            
            # Tampilkan statistik jika diminta
            if self.var_tampil_statistik.get():
                self._tampilkan_statistik(deret)
            
            # Simpan ke riwayat
            self.manajer_riwayat.tambah_riwayat(n, deret)
            self._perbarui_riwayat()
            
            self.var_status.set(f"Berhasil menghasilkan {n} suku Fibonacci")
            
        except ValueError:
            messagebox.showerror("Error Input", "Masukkan bilangan bulat yang valid!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            self.var_status.set("Error dalam menghasilkan deret")
    
    def _tampilkan_deret(self, deret):

        # Menampilkan deret Fibonacci di tab deret
        self.text_deret.delete(1.0, tk.END)
        
        if not deret:
            self.text_deret.insert(tk.END, "Tidak ada deret yang dihasilkan")
            return
        
        formatted_sequence = self.kalkulator.format_deret(deret)
        self.text_deret.insert(tk.END, formatted_sequence)
    
    def _tampilkan_grafik(self, deret):

        # Hapus grafik sebelumnya
        for widget in self.frame_tab_grafik.winfo_children():
            widget.destroy()
        
        if not deret:
            tk.Label(self.frame_tab_grafik, text="Tidak ada data untuk ditampilkan", 
                    bg='#f0f0f0', font=('Arial', 12)).pack(expand=True)
            return
        
        # Buat figure matplotlib
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#f0f0f0')
        
        # Plot deret asli
        x = list(range(len(deret)))
        ax1.plot(x, deret, 'b-o', markersize=3, linewidth=1)
        ax1.set_title('Deret Fibonacci')
        ax1.set_xlabel('Indeks Suku')
        ax1.set_ylabel('Nilai')
        ax1.grid(True, alpha=0.3)
        
        # Plot rasio suku berurutan
        if len(deret) > 1:
            rasio = []
            for i in range(1, len(deret)):
                if deret[i-1] != 0:
                    rasio.append(deret[i] / deret[i-1])
                else:
                    rasio.append(0)
            
            ax2.plot(range(1, len(deret)), rasio, 'r-o', markersize=3, linewidth=1)
            ax2.axhline(y=1.61803398875, color='g', linestyle='--', alpha=0.7, label='Golden Ratio (φ)')
            ax2.set_title('Rasio Suku Berurutan')
            ax2.set_xlabel('Indeks Suku')
            ax2.set_ylabel('Rasio F(n)/F(n-1)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Embed plot di Tkinter
        canvas = FigureCanvasTkAgg(fig, self.frame_tab_grafik)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _tampilkan_statistik(self, deret):
        
        # Menampilkan statistik deret Fibonacci
        self.text_statistik.delete(1.0, tk.END)
        
        if not deret:
            self.text_statistik.insert(tk.END, "Tidak ada statistik yang tersedia")
            return
        
        statistik = self.kalkulator.hitung_statistik(deret)
        
        # Tampilkan statistik
        self.text_statistik.insert(tk.END, f"Jumlah suku: {statistik['jumlah_suku']}\n")
        self.text_statistik.insert(tk.END, f"Total semua suku: {statistik['total']}\n")
        self.text_statistik.insert(tk.END, f"Nilai rata-rata: {statistik['rata_rata']:.2f}\n")
        self.text_statistik.insert(tk.END, f"Suku terbesar: {statistik['suku_terbesar']}\n")
        self.text_statistik.insert(tk.END, f"Suku terkecil: {statistik['suku_terkecil']}\n")
        self.text_statistik.insert(tk.END, f"Jumlah suku genap: {statistik['jumlah_genap']}\n")
        self.text_statistik.insert(tk.END, f"Jumlah suku ganjil: {statistik['jumlah_ganjil']}\n")
        
        if statistik['jumlah_suku'] >= 2:
            self.text_statistik.insert(tk.END, f"Rasio dua suku terakhir: {statistik['rasio_terakhir']:.6f}\n")
            self.text_statistik.insert(tk.END, f"Golden Ratio (φ): {statistik['golden_ratio']:.6f}\n")
            self.text_statistik.insert(tk.END, f"Selisih dengan φ: {statistik['selisih_rasio']:.6f}\n")
    
    def _perbarui_riwayat(self):
        
        # Memperbarui tampilan riwayat perhitungan
        self.listbox_riwayat.delete(0, tk.END)
        
        riwayat_terbaru = self.manajer_riwayat.dapatkan_riwayat_terbaru(20)
        
        for entri in reversed(riwayat_terbaru):
            teks_tampilan = f"{entri['timestamp']} - Fibonacci({entri['n']}) = {entri['suku_terakhir']}"
            self.listbox_riwayat.insert(tk.END, teks_tampilan)
    
    def _muat_dari_riwayat(self, event):
        
        # Memuat parameter dari entri riwayat yang dipilih
        pilihan = self.listbox_riwayat.curselection()
        if pilihan:
            index = pilihan[0]
            riwayat_terbaru = self.manajer_riwayat.dapatkan_riwayat_terbaru(20)
            if 0 <= index < len(riwayat_terbaru):

                # Karena ditampilkan terbalik, perlu konversi index
                entri = riwayat_terbaru[len(riwayat_terbaru) - 1 - index]
                self.entry_n.delete(0, tk.END)
                self.entry_n.insert(0, str(entri['n']))
                self._generate_fibonacci()
    
    def _bersihkan_riwayat(self):

        # Membersihkan semua riwayat perhitungan setelah konfirmasi
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua riwayat?"):
            self.manajer_riwayat.bersihkan_riwayat()
            self._perbarui_riwayat()
    
    def _ekspor_riwayat(self):

        # Mengekspor riwayat perhitungan ke file eksternal
        try:
            nama_file = self.manajer_riwayat.ekspor_riwayat_ke_file()
            messagebox.showinfo("Ekspor Berhasil", f"Riwayat berhasil diekspor ke {nama_file}")
        except Exception as e:
            messagebox.showerror("Error Ekspor", f"Gagal mengekspor riwayat: {str(e)}")
    
    def _bersihkan_semua(self):

        # Membersihkan semua input dan hasil di GUI
        self.entry_n.delete(0, tk.END)
        self.text_deret.delete(1.0, tk.END)
        self.text_statistik.delete(1.0, tk.END)
        
        # Hapus grafik
        for widget in self.frame_tab_grafik.winfo_children():
            widget.destroy()
        
        self.var_status.set("Semua input dan hasil telah dibersihkan")