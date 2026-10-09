import tkinter as tk
from gui import AplikasiDiskon

# Fungsi utama untuk menjalankan aplikasi
def main():
    try:
        root = tk.Tk()
        app = AplikasiDiskon(root)
        root.mainloop()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main()