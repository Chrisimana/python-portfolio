import tkinter as tk
from gui import AntarmukaFibonacci

def main():

    # Inisialisasi dan jalankan antarmuka pengguna
    try:
        root = tk.Tk()
        app = AntarmukaFibonacci(root)
        root.mainloop()
    except Exception as e:
        print(f"Error menjalankan aplikasi: {e}")

if __name__ == "__main__":
    main()