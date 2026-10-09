import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import locale
import sys
import os

# Tambahkan path modules ke sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database import DatabaseManager
from report_generator import ReportGenerator

# Set locale untuk format currency Indonesia
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except:
    pass

class CicilanRumahApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.report_generator = ReportGenerator(self.db)
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):

        self.root = tk.Tk()
        self.root.title("Kalkulator Cicilan Rumah 🏠")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2C3E50')
        
        # Style configuration
        self.setup_styles()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tab_kalkulator = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)
        self.tab_grafik = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_kalkulator, text='🧮 Kalkulator')
        self.notebook.add(self.tab_history, text='📊 History')
        self.notebook.add(self.tab_grafik, text='📈 Grafik')
        
        self.setup_kalkulator_tab()
        self.setup_history_tab()
        self.setup_grafik_tab()
    
    # Setup style untuk widgets
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TFrame', background='#2C3E50')
        style.configure('Title.TLabel', background='#2C3E50', foreground='white', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', background='#2C3E50', foreground='#ECF0F1', font=('Arial', 12, 'bold'))
        style.configure('Result.TLabel', background='#34495E', foreground='white', font=('Arial', 10, 'bold'))
        style.configure('Custom.TButton', background='#3498DB', foreground='white', font=('Arial', 10, 'bold'))
        style.configure('Success.TButton', background='#27AE60', foreground='white')
        style.configure('Danger.TButton', background='#E74C3C', foreground='white')
        
    # Setup tab kalkulator
    def setup_kalkulator_tab(self):
        # Main frame
        main_frame = ttk.Frame(self.tab_kalkulator)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="KALKULATOR CICILAN RUMAH", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text=" Input Data ", padding=15)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Nama Proyek
        ttk.Label(input_frame, text="Nama Proyek:", style='Subtitle.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nama = ttk.Entry(input_frame, width=40, font=('Arial', 10))
        self.entry_nama.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        # Harga Asal
        ttk.Label(input_frame, text="Harga Asal Rumah (Rp):", style='Subtitle.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.entry_harga_asal = ttk.Entry(input_frame, width=40, font=('Arial', 10))
        self.entry_harga_asal.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        # Harga Jual
        ttk.Label(input_frame, text="Harga Jual ke Klien (Rp):", style='Subtitle.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.entry_harga_jual = ttk.Entry(input_frame, width=40, font=('Arial', 10))
        self.entry_harga_jual.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        # Lama Cicilan
        ttk.Label(input_frame, text="Lama Cicilan (tahun):", style='Subtitle.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        self.combo_cicilan = ttk.Combobox(input_frame, values=["5", "10", "15", "20"], state="readonly", width=37)
        self.combo_cicilan.set("15")
        self.combo_cicilan.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', padx=10, pady=20)
        
        btn_hitung = ttk.Button(button_frame, text="🚀 HITUNG CICILAN", 
                              command=self.hitung_cicilan, style='Custom.TButton')
        btn_hitung.pack(side='left', padx=5)
        
        btn_clear = ttk.Button(button_frame, text="🗑️ CLEAR FORM", 
                             command=self.clear_form, style='Danger.TButton')
        btn_clear.pack(side='left', padx=5)
        
        btn_export = ttk.Button(button_frame, text="📄 EXPORT LAPORAN", 
                              command=self.export_laporan, style='Success.TButton')
        btn_export.pack(side='right', padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text=" Hasil Perhitungan ", padding=15)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollable text for results
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, font=('Arial', 10),
                                                     bg='#34495E', fg='white', wrap=tk.WORD)
        self.results_text.pack(fill='both', expand=True)
        self.results_text.config(state=tk.DISABLED)
    
    # Setup tab history
    def setup_history_tab(self):
        # Toolbar frame
        toolbar_frame = ttk.Frame(self.tab_history)
        toolbar_frame.pack(fill='x', padx=10, pady=10)
        
        btn_refresh = ttk.Button(toolbar_frame, text="🔄 Refresh History", 
                               command=self.load_history, style='Custom.TButton')
        btn_refresh.pack(side='left', padx=5)
        
        btn_clear = ttk.Button(toolbar_frame, text="🗑️ Hapus Semua History", 
                             command=self.clear_history, style='Danger.TButton')
        btn_clear.pack(side='left', padx=5)
        
        # Treeview frame
        tree_frame = ttk.Frame(self.tab_history)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview with scrollbar
        columns = ("ID", "Tanggal", "Proyek", "Harga Asal", "Harga Jual", "Lama", "Cicilan/Tahun", "Keuntungan")
        
        self.tree_history = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Define headings
        headings = {
            "ID"           : "ID",
            "Tanggal"      : "Tanggal",
            "Proyek"       : "Nama Proyek", 
            "Harga Asal"   : "Harga Asal (Rp)",
            "Harga Jual"   : "Harga Jual (Rp)",
            "Lama"         : "Lama (thn)",
            "Cicilan/Tahun": "Cicilan/Thn (Rp)",
            "Keuntungan"   : "Keuntungan (Rp)"
        }
        
        for col, text in headings.items():
            self.tree_history.heading(col, text=text)
        
        # Set column widths
        column_widths = {
            "ID": 50,
            "Tanggal": 120,
            "Proyek": 150,
            "Harga Asal": 120,
            "Harga Jual": 120,
            "Lama": 80,
            "Cicilan/Tahun": 120,
            "Keuntungan": 120
        }
        
        for col, width in column_widths.items():
            self.tree_history.column(col, width=width, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_history.yview)
        self.tree_history.configure(yscrollcommand=scrollbar.set)
        
        self.tree_history.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load initial history
        self.load_history()
    
    # Setup tab grafik
    def setup_grafik_tab(self):
        # Toolbar frame
        toolbar_frame = ttk.Frame(self.tab_grafik)
        toolbar_frame.pack(fill='x', padx=10, pady=10)
        
        btn_generate = ttk.Button(toolbar_frame, text="📈 GENERATE GRAFIK", 
                                command=self.generate_grafik, style='Custom.TButton')
        btn_generate.pack(side='left', padx=5)
        
        # Graph frame
        self.grafik_frame = ttk.Frame(self.tab_grafik)
        self.grafik_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Format angka menjadi format currency Indonesia
    def format_currency(self, value):
        try:
            return f"Rp{value:,.0f}".replace(",", ".")
        except:
            return f"Rp{value:,.0f}"
    
    # Mengosongkan form input
    def clear_form(self):
        self.entry_nama.delete(0, 'end')
        self.entry_harga_asal.delete(0, 'end')
        self.entry_harga_jual.delete(0, 'end')
        self.combo_cicilan.set("15")
        
        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    # Menghitung cicilan berdasarkan input
    def hitung_cicilan(self):
        try:
            nama_proyek = self.entry_nama.get().strip()
            harga_asal = float(self.entry_harga_asal.get().replace('.', '').replace(',', ''))
            harga_jual = float(self.entry_harga_jual.get().replace('.', '').replace(',', ''))
            lama_cicilan = int(self.combo_cicilan.get())
            
            if not nama_proyek:
                messagebox.showwarning("Peringatan", "Mohon isi nama proyek!")
                return
            
            if harga_asal <= 0 or harga_jual <= 0:
                messagebox.showwarning("Peringatan", "Harga harus lebih dari 0!")
                return
            
            if harga_jual < harga_asal:
                messagebox.showwarning("Peringatan", "Harga jual harus lebih besar dari harga asal!")
                return
            
            total_selisih = harga_jual - harga_asal
            cicilan_per_tahun = harga_jual / lama_cicilan
            cicilan_per_bulan = cicilan_per_tahun / 12
            keuntungan_persen = (total_selisih / harga_asal) * 100
            
            # Simpan ke database
            data = {
                'nama_proyek': nama_proyek,
                'harga_asal': harga_asal,
                'harga_jual': harga_jual,
                'lama_cicilan': lama_cicilan,
                'cicilan_per_tahun': cicilan_per_tahun,
                'total_selisih': total_selisih,
                'metadata': {
                    'cicilan_per_bulan': cicilan_per_bulan,
                    'keuntungan_persen': keuntungan_persen
                }
            }
            
            self.db.simpan_perhitungan(data)
            
            # Tampilkan hasil
            self.tampilkan_hasil(data)
            
            # Refresh history
            self.load_history()
            
        except ValueError as e:
            messagebox.showerror("Error", "Input tidak valid! Pastikan format angka benar.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    # Menampilkan hasil perhitungan
    def tampilkan_hasil(self, data):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        hasil_text = f"""
{'='*60}
📋 HASIL PERHITUNGAN CICILAN RUMAH
{'='*60}

📋 Nama Proyek          : {data['nama_proyek']}
💰 Harga Asal           : {self.format_currency(data['harga_asal'])}
🏷️ Harga Jual           : {self.format_currency(data['harga_jual'])}
📈 Keuntungan           : {self.format_currency(data['total_selisih'])}
📅 Lama Cicilan         : {data['lama_cicilan']} tahun
🎯 Cicilan per Tahun    : {self.format_currency(data['cicilan_per_tahun'])}
📆 Cicilan per Bulan    : {self.format_currency(data['metadata']['cicilan_per_bulan'])}
📊 Persentase Keuntungan: {data['metadata']['keuntungan_persen']:.2f}%

{'='*60}
💡 ANALISIS:
• Keuntungan yang didapat: {self.format_currency(data['total_selisih'])}
• Persentase keuntungan: {data['metadata']['keuntungan_persen']:.2f}%
• Cicilan bulanan: {self.format_currency(data['metadata']['cicilan_per_bulan'])}
{'='*60}
"""
        
        self.results_text.insert(tk.END, hasil_text)
        self.results_text.config(state=tk.DISABLED)
    
    # Memuat data history
    def load_history(self):
        # Clear existing data
        for item in self.tree_history.get_children():
            self.tree_history.delete(item)
        
        history_data = self.db.ambil_history()
        
        for row in history_data:
            formatted_row = (
                row[0],  # ID
                row[1][:16],  # Tanggal
                row[2],  # Proyek
                self.format_currency(row[3]),  # Harga Asal
                self.format_currency(row[4]),  # Harga Jual
                row[5],  # Lama Cicilan
                self.format_currency(row[6]),  # Cicilan per Tahun
                self.format_currency(row[7]),  # Keuntungan
            )
            self.tree_history.insert("", "end", values=formatted_row)
    
    # Menghapus semua history
    def clear_history(self):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua history? Tindakan ini tidak dapat dibatalkan!"):
            self.db.hapus_semua_history()
            self.load_history()
            messagebox.showinfo("Sukses", "History berhasil dihapus!")
    
    # Generate grafik analisis
    def generate_grafik(self):
        try:
            history_data = self.db.ambil_history(limit=10)
            
            if not history_data:
                messagebox.showinfo("Info", "Tidak ada data untuk ditampilkan dalam grafik")
                return
            
            # Clear previous graph
            for widget in self.grafik_frame.winfo_children():
                widget.destroy()
            
            # Create matplotlib figure
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle('ANALISIS PERHITUNGAN CICILAN RUMAH', fontsize=16, fontweight='bold')
            
            # Prepare data
            proyek_names = [row[2] for row in history_data]
            harga_asals = [row[3] for row in history_data]
            harga_juals = [row[4] for row in history_data]
            selisihs = [row[7] for row in history_data]
            
            # Grafik 1: Perbandingan Harga
            x = range(len(proyek_names))
            width = 0.35
            
            bars1 = ax1.bar([i - width/2 for i in x], harga_asals, width, 
                           label='Harga Asal', alpha=0.7, color='#2E86AB')
            bars2 = ax1.bar([i + width/2 for i in x], harga_juals, width, 
                           label='Harga Jual', alpha=0.7, color='#A23B72')
            
            ax1.set_xlabel('Proyek')
            ax1.set_ylabel('Harga (Rp)')
            ax1.set_title('PERBANDINGAN HARGA ASAL vs HARGA JUAL')
            ax1.set_xticks(x)
            ax1.set_xticklabels(proyek_names, rotation=45, ha='right')
            ax1.legend()
            ax1.ticklabel_format(style='plain', axis='y')
            
            # Tambahkan nilai di atas bar
            for bar in bars1 + bars2:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'Rp{height:,.0f}',
                        ha='center', va='bottom', rotation=90, fontsize=8)
            
            # Grafik 2: Keuntungan
            bars3 = ax2.bar(proyek_names, selisihs, color='#4CAF50', alpha=0.7)
            ax2.set_xlabel('Proyek')
            ax2.set_ylabel('Keuntungan (Rp)')
            ax2.set_title('KEUNTUNGAN PER PROYEK')
            ax2.ticklabel_format(style='plain', axis='y')
            plt.xticks(rotation=45, ha='right')
            
            # Tambahkan nilai di atas bar
            for bar in bars3:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'Rp{height:,.0f}',
                        ha='center', va='bottom', rotation=90, fontsize=8)
            
            plt.tight_layout()
            
            # Embed graph in tkinter
            canvas = FigureCanvasTkAgg(fig, self.grafik_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal generate grafik: {str(e)}")
    
    # Export laporan ke file
    def export_laporan(self):
        try:
            filename = self.report_generator.generate_pdf_report()
            messagebox.showinfo("Sukses", f"Laporan berhasil diexport!\n\nFile: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal export laporan: {str(e)}")
    
    # Menjalankan aplikasi
    def run(self):
        self.root.mainloop()