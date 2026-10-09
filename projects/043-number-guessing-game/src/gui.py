import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import GameLogic
from history_manager import HistoryManager
import random

class TebakAngkaApp:
    # Inisialisasi aplikasi
    def __init__(self, root):
        self.root = root
        self.root.title("Game Tebak Angka")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Inisialisasi game dan history
        self.game = GameLogic()
        self.history_manager = HistoryManager()
        
        # Warna tema
        self.colors = {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "dark": "#2c3e50",
            "light": "#ecf0f1"
        }
        
        self.setup_ui()
        self.update_display()

    # Setup UI   
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["dark"], height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🎯 Game Tebak Angka 🎯", 
            font=("Arial", 18, "bold"),
            fg="white",
            bg=self.colors["dark"]
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Tebak angka antara 1-10. Kamu punya 3 kesempatan!",
            font=("Arial", 10),
            fg=self.colors["light"],
            bg=self.colors["dark"]
        )
        subtitle_label.pack(expand=True)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg=self.colors["light"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel - Game
        left_frame = tk.Frame(main_frame, bg=self.colors["light"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Game Info
        info_frame = tk.LabelFrame(
            left_frame, 
            text="Status Permainan", 
            font=("Arial", 10, "bold"),
            bg=self.colors["light"],
            fg=self.colors["dark"]
        )
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.kesempatan_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 12),
            bg=self.colors["light"],
            fg=self.colors["dark"]
        )
        self.kesempatan_label.pack(pady=5)
        
        self.status_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg=self.colors["light"]
        )
        self.status_label.pack(pady=5)
        
        # Input Frame
        input_frame = tk.LabelFrame(
            left_frame, 
            text="Tebak Angka", 
            font=("Arial", 10, "bold"),
            bg=self.colors["light"],
            fg=self.colors["dark"]
        )
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            input_frame,
            text="Masukkan tebakan (1-10):",
            font=("Arial", 10),
            bg=self.colors["light"]
        ).pack(pady=5)
        
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            input_frame,
            textvariable=self.entry_var,
            font=("Arial", 14),
            justify=tk.CENTER,
            width=10
        )
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda e: self.proses_tebakan())
        
        button_frame = tk.Frame(input_frame, bg=self.colors["light"])
        button_frame.pack(pady=5)
        
        self.tebak_button = tk.Button(
            button_frame,
            text="Tebak!",
            command=self.proses_tebakan,
            bg=self.colors["primary"],
            fg="white",
            font=("Arial", 10, "bold"),
            width=10
        )
        self.tebak_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="Game Baru",
            command=self.reset_game,
            bg=self.colors["secondary"],
            fg="white",
            font=("Arial", 10, "bold"),
            width=10
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # History Tebakan
        history_frame = tk.LabelFrame(
            left_frame, 
            text="History Tebakan", 
            font=("Arial", 10, "bold"),
            bg=self.colors["light"],
            fg=self.colors["dark"]
        )
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_listbox = tk.Listbox(
            history_frame,
            font=("Arial", 10),
            height=6
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right Panel - Statistics
        right_frame = tk.Frame(main_frame, bg=self.colors["light"], width=200)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # Statistics
        stats_frame = tk.LabelFrame(
            right_frame, 
            text="Statistik", 
            font=("Arial", 10, "bold"),
            bg=self.colors["light"],
            fg=self.colors["dark"]
        )
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 10),
            bg=self.colors["light"],
            justify=tk.LEFT
        )
        self.stats_label.pack(pady=5, padx=5, anchor=tk.W)
        
        # Recent Games
        recent_frame = tk.LabelFrame(
            right_frame, 
            text="Permainan Terakhir", 
            font=("Arial", 10, "bold"),
            bg=self.colors["light"],
            fg=self.colors["dark"]
        )
        recent_frame.pack(fill=tk.BOTH, expand=True)
        
        self.recent_listbox = tk.Listbox(
            recent_frame,
            font=("Arial", 9),
            height=8
        )
        self.recent_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.colors["dark"], height=30)
        footer_frame.pack(fill=tk.X, padx=10, pady=5)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Game Tebak Angka",
            font=("Arial", 8),
            fg="white",
            bg=self.colors["dark"]
        )
        footer_label.pack(expand=True)
        
    # Proses tebakan pemain
    def proses_tebakan(self):
        try:
            angka = int(self.entry_var.get())
            result = self.game.tebak_angka(angka)
            
            if result["status"] == "error":
                messagebox.showerror("Error", result["pesan"])
            elif result["status"] == "menang":
                self.status_label.config(text=result["pesan"], fg=self.colors["secondary"])
                self.tebak_button.config(state=tk.DISABLED)
                self.history_manager.add_game_record(
                    "menang", 
                    self.game.tebakan_sebelumnya, 
                    3 - result["kesempatan"]
                )
            elif result["status"] == "kalah":
                self.status_label.config(text=result["pesan"], fg=self.colors["danger"])
                self.tebak_button.config(state=tk.DISABLED)
                self.history_manager.add_game_record(
                    "kalah", 
                    self.game.tebakan_sebelumnya, 
                    3
                )
            else:
                self.status_label.config(text=result["pesan"], fg=self.colors["warning"])
                
            self.entry_var.set("")
            self.update_display()
            
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    # Reset permainan 
    def reset_game(self):
        self.game.reset_game()
        self.tebak_button.config(state=tk.NORMAL)
        self.entry_var.set("")
        self.update_display()

    # Update tampilan UI berdasarkan status permainan dan history    
    def update_display(self):
        # Update kesempatan
        state = self.game.get_game_state()
        self.kesempatan_label.config(
            text=f"Kesempatan tersisa: {state['kesempatan']}"
        )
        
        # Update history tebakan
        self.history_listbox.delete(0, tk.END)
        for i, tebakan in enumerate(state['tebakan_sebelumnya']):
            status = "✓" if tebakan == state['angka_rahasia'] else "✗"
            self.history_listbox.insert(
                tk.END, 
                f"Tebakan {i+1}: {tebakan} {status}"
            )
            
        # Update statistik
        stats = self.history_manager.get_statistics()
        stats_text = f"Total Permainan: {stats['total_game']}\n"
        stats_text += f"Menang: {stats['menang']}\n"
        stats_text += f"Kalah: {stats['kalah']}\n"
        if stats['total_game'] > 0:
            persentase = (stats['menang'] / stats['total_game']) * 100
            stats_text += f"Persentase Menang: {persentase:.1f}%\n"
            stats_text += f"Rata-rata Tebakan: {stats['rata_rata_tebakan']}"
        self.stats_label.config(text=stats_text)
        
        # Update permainan terakhir
        self.recent_listbox.delete(0, tk.END)
        recent_games = self.history_manager.get_recent_games(5)
        for game in reversed(recent_games):
            status_emoji = "🎉" if game["status"] == "menang" else "😞"
            self.recent_listbox.insert(
                tk.END, 
                f"{game['tanggal'][11:16]} {status_emoji} {game['status'].upper()}"
            )