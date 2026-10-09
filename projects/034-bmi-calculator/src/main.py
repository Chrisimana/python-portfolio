import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkfont
from bmi_calculator import BMICalculator
from history_manager import HistoryManager
from styles import COLORS, CATEGORY_COLORS, FONTS

class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator BMI")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["background"])
        
        # Initialize components
        self.calculator = BMICalculator()
        self.history_manager = HistoryManager()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Kalkulator Tab
        self.setup_calculator_tab()
        
        # History Tab
        self.setup_history_tab()
        
        # About Tab
        self.setup_about_tab()
    
    def setup_calculator_tab(self):
        # Frame untuk kalkulator
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="Kalkulator BMI")
        
        # Header
        header_frame = ttk.Frame(calc_frame)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(
            header_frame, 
            text="KALKULATOR BMI (Body Mass Index)", 
            font=FONTS["title"],
            fg=COLORS["primary"],
            bg=COLORS["background"]
        )
        title_label.pack()
        
        # Input Frame
        input_frame = ttk.LabelFrame(calc_frame, text="Data Diri", padding=15)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Nama
        tk.Label(input_frame, text="Nama:", font=FONTS["normal"]).grid(row=0, column=0, sticky='w', pady=5)
        self.nama_entry = tk.Entry(input_frame, width=30, font=FONTS["normal"])
        self.nama_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        # Berat Badan
        tk.Label(input_frame, text="Berat Badan (kg):", font=FONTS["normal"]).grid(row=1, column=0, sticky='w', pady=5)
        self.berat_entry = tk.Entry(input_frame, width=30, font=FONTS["normal"])
        self.berat_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        # Tinggi Badan
        tk.Label(input_frame, text="Tinggi Badan (m):", font=FONTS["normal"]).grid(row=2, column=0, sticky='w', pady=5)
        self.tinggi_entry = tk.Entry(input_frame, width=30, font=FONTS["normal"])
        self.tinggi_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        # Contoh
        contoh_label = tk.Label(
            input_frame, 
            text="Contoh: Tinggi 170 cm = 1.70", 
            font=FONTS["small"], 
            fg="gray"
        )
        contoh_label.grid(row=3, column=1, sticky='w', padx=10)
        
        # Button Frame
        button_frame = ttk.Frame(calc_frame)
        button_frame.pack(fill='x', padx=20, pady=10)
        
        calc_button = tk.Button(
            button_frame,
            text="Hitung BMI",
            command=self.calculate_bmi,
            bg=COLORS["primary"],
            fg="white",
            font=FONTS["heading"],
            padx=20,
            pady=10
        )
        calc_button.pack(side='left', padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Bersihkan",
            command=self.clear_inputs,
            bg=COLORS["secondary"],
            fg="white",
            font=FONTS["normal"],
            padx=20,
            pady=10
        )
        clear_button.pack(side='left', padx=5)
        
        # Result Frame
        self.result_frame = ttk.LabelFrame(calc_frame, text="Hasil", padding=15)
        self.result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Initially hide result frame
        self.result_frame.pack_forget()
    
    def setup_history_tab(self):
        # Frame untuk history
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="Riwayat")
        
        # Header dengan button
        history_header = ttk.Frame(history_frame)
        history_header.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            history_header, 
            text="Riwayat Perhitungan BMI", 
            font=FONTS["heading"]
        ).pack(side='left')
        
        clear_history_btn = tk.Button(
            history_header,
            text="Hapus Riwayat",
            command=self.clear_history,
            bg=COLORS["danger"],
            fg="white",
            font=FONTS["normal"]
        )
        clear_history_btn.pack(side='right')
        
        # Text area untuk menampilkan history
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=FONTS["normal"]
        )
        self.history_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Load history saat tab dibuka
        self.load_history_display()
    
    def setup_about_tab(self):
        # Frame untuk about
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="Tentang")
        
        content = """
KALKULATOR BMI

Fitur:
• Perhitungan BMI akurat
• Kategori berat badan
• Rentang berat ideal
• Penyimpanan riwayat
• Antarmuka yang user-friendly

Kategori BMI:
• Kekurangan berat badan: BMI < 18.5
• Normal: 18.5 - 24.9
• Kelebihan berat badan: 25 - 29.9
• Obesitas: BMI ≥ 30

Cara penggunaan:
1. Masukkan nama (opsional)
2. Masukkan berat badan dalam kilogram
3. Masukkan tinggi badan dalam meter
4. Klik tombol 'Hitung BMI'

Aplikasi ini membantu Anda memantau kesehatan 
dan mencapai berat badan ideal.

"""
        
        about_text = tk.Text(
            about_frame,
            wrap=tk.WORD,
            padx=20,
            pady=20,
            font=FONTS["normal"],
            bg=COLORS["background"]
        )
        about_text.pack(fill='both', expand=True)
        about_text.insert('1.0', content)
        about_text.config(state='disabled')
    
    def calculate_bmi(self):
        try:
            # Get inputs
            nama = self.nama_entry.get().strip() or "Anonim"
            berat = float(self.berat_entry.get())
            tinggi = float(self.tinggi_entry.get())
            
            if berat <= 0 or tinggi <= 0:
                messagebox.showerror("Error", "Berat dan tinggi harus lebih dari 0!")
                return
            
            # Calculate BMI
            bmi = self.calculator.calculate_bmi(berat, tinggi)
            kategori, category_key = self.calculator.get_kategori(bmi)
            berat_ideal_bawah, berat_ideal_atas = self.calculator.get_berat_ideal_range(tinggi)
            
            # Save to history
            self.history_manager.save_record(nama, berat, tinggi, bmi, kategori)
            
            # Display results
            self.show_results(bmi, kategori, category_key, berat_ideal_bawah, berat_ideal_atas, nama)
            
        except ValueError as e:
            messagebox.showerror("Error", "Masukkan angka yang valid untuk berat dan tinggi!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def show_results(self, bmi, kategori, category_key, berat_bawah, berat_atas, nama):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Show result frame
        self.result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Color based on category
        color = CATEGORY_COLORS.get(category_key, COLORS["dark"])
        
        # Header dengan nama
        tk.Label(
            self.result_frame,
            text=f"Hasil untuk: {nama}",
            font=FONTS["heading"],
            fg=COLORS["primary"]
        ).pack(pady=5)
        
        # BMI Value
        tk.Label(
            self.result_frame,
            text=f"Nilai BMI:",
            font=FONTS["normal"]
        ).pack(pady=2)
        
        tk.Label(
            self.result_frame,
            text=f"{bmi} kg/m²",
            font=("Arial", 24, "bold"),
            fg=color
        ).pack(pady=5)
        
        # Kategori
        tk.Label(
            self.result_frame,
            text="Kategori:",
            font=FONTS["normal"]
        ).pack(pady=2)
        
        tk.Label(
            self.result_frame,
            text=kategori,
            font=FONTS["heading"],
            fg=color
        ).pack(pady=5)
        
        # Berat Ideal
        tk.Label(
            self.result_frame,
            text=f"Rentang Berat Badan Ideal:",
            font=FONTS["normal"]
        ).pack(pady=2)
        
        tk.Label(
            self.result_frame,
            text=f"{berat_bawah} kg - {berat_atas} kg",
            font=FONTS["heading"],
            fg=COLORS["success"]
        ).pack(pady=5)
        
        # Pesan berdasarkan kategori
        pesan = self.get_recommendation(category_key)
        tk.Label(
            self.result_frame,
            text="Rekomendasi:",
            font=FONTS["normal"]
        ).pack(pady=2)
        
        # Text widget untuk rekomendasi dengan wrap
        recommendation_text = tk.Text(
            self.result_frame,
            height=4,
            wrap=tk.WORD,
            font=FONTS["normal"],
            bg=COLORS["light"],
            padx=10,
            pady=10
        )
        recommendation_text.pack(fill='x', padx=10, pady=5)
        recommendation_text.insert('1.0', pesan)
        recommendation_text.config(state='disabled')
    
    def get_recommendation(self, category):
        recommendations = {
            "underweight": """• Tingkatkan asupan kalori dengan makanan bergizi
• Konsumsi protein yang cukup
• Lakukan latihan kekuatan untuk membangun otot
• Konsultasi dengan ahli gizi jika diperlukan""",
            
            "normal": """• Pertahankan pola makan sehat dan seimbang
• Tetap aktif berolahraga secara teratur
• Monitor berat badan secara berkala
• Jaga kualitas tidur dan kelola stres""",
            
            "overweight": """• Kurangi asupan kalori berlebih
• Tingkatkan aktivitas fisik
• Konsumsi lebih banyak serat dan protein
• Hindari makanan tinggi gula dan lemak jenuh""",
            
            "obese": """• Konsultasi dengan dokter atau ahli gizi
• Program penurunan berat badan yang terstruktur
• Aktivitas fisik teratur dan bertahap
• Perubahan gaya hidup jangka panjang"""
        }
        return recommendations.get(category, "Konsultasi dengan profesional kesehatan.")
    
    def clear_inputs(self):
        self.nama_entry.delete(0, tk.END)
        self.berat_entry.delete(0, tk.END)
        self.tinggi_entry.delete(0, tk.END)
        self.result_frame.pack_forget()
    
    def load_history_display(self):
        records = self.history_manager.get_recent_records(20)
        self.history_text.delete('1.0', tk.END)
        
        if not records:
            self.history_text.insert('1.0', "Belum ada riwayat perhitungan.")
            return
        
        for record in reversed(records):
            self.history_text.insert('1.0', 
                f"Waktu: {record['timestamp']}\n"
                f"Nama: {record['nama']}\n"
                f"Berat: {record['berat']} kg | Tinggi: {record['tinggi']} m\n"
                f"BMI: {record['bmi']} | Kategori: {record['kategori']}\n"
                f"{'='*50}\n"
            )
    
    def clear_history(self):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua riwayat?"):
            if self.history_manager.clear_history():
                messagebox.showinfo("Sukses", "Riwayat berhasil dihapus!")
                self.load_history_display()
            else:
                messagebox.showinfo("Info", "Tidak ada riwayat yang perlu dihapus.")

def main():
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()