import tkinter as tk
from gui.window import AplikasiKontak
import sys

def main():
    try:
        root = tk.Tk()
        app = AplikasiKontak(root)
        root.mainloop()
    except Exception as e:
        print(f"Error menjalankan aplikasi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Memulai Aplikasi Manajemen Kontak...")
    print("✨ Fitur Super Keren:")
    print("   • GUI Modern dengan Tkinter")
    print("   • Database SQLite")
    print("   • History Aktivitas")
    print("   • Statistik Kontak")
    print("   • Pencarian & Filter")
    print("   • Kategori Kontak")
    print()
    main()