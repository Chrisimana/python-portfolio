import tkinter as tk
from tkinter import messagebox

BACKGROUND_COLOR = "#1f1a17"
ACCENT_COLOR = "#c68b59"
TEXT_COLOR = "#f5f0eb"
BUTTON_COLOR = "#3a2f2a"


# Merepresentasikan satu item menu beserta harga dan kebutuhan bahannya
class MenuItem:
    def __init__(self, name, water, milk, coffee, cost):
        self.name = name
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.cost = cost


# Menyimpan seluruh daftar menu yang tersedia di mesin kopi
class Menu:
    def __init__(self):
        self.items = [
            MenuItem("espresso", water=50, milk=0, coffee=18, cost=1.5),
            MenuItem("latte", water=200, milk=150, coffee=24, cost=2.5),
            MenuItem("cappuccino", water=250, milk=100, coffee=24, cost=3.0),
        ]

    # Mengembalikan daftar nama semua menu yang tersedia
    def get_items(self):
        return [item.name for item in self.items]

    # Mencari objek MenuItem berdasarkan nama
    def find_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None


# Mengelola sumber daya mesin kopi (air, susu, kopi) dan proses pembuatan kopi
class CoffeeMaker:
    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }

    # Mengecek apakah sumber daya cukup untuk membuat pesanan tertentu
    def is_resource_sufficient(self, drink: MenuItem):
        missing = []
        if drink.water > self.resources["water"]:
            missing.append("air")
        if drink.milk > self.resources["milk"]:
            missing.append("susu")
        if drink.coffee > self.resources["coffee"]:
            missing.append("biji kopi")
        return missing

    # Mengurangi sumber daya sesuai kebutuhan minuman yang dibuat
    def make_coffee(self, drink: MenuItem):
        self.resources["water"] -= drink.water
        self.resources["milk"] -= drink.milk
        self.resources["coffee"] -= drink.coffee

    # Mengembalikan laporan sumber daya saat ini dalam bentuk teks
    def report(self):
        return (
            f"Air     : {self.resources['water']}ml\n"
            f"Susu    : {self.resources['milk']}ml\n"
            f"Kopi    : {self.resources['coffee']}g"
        )


# Mengelola transaksi uang, termasuk penghitungan koin dan kembalian
class CashRegister:
    def __init__(self):
        self.profit = 0.0

    # Menghitung total uang dari jumlah masing-masing jenis koin
    def calculate_total(self, quarters, dimes, nickels, pennies):
        return (
            quarters * 0.25
            + dimes * 0.10
            + nickels * 0.05
            + pennies * 0.01
        )

    # Memproses pembayaran, mengembalikan (berhasil, kembalian)
    def process_payment(self, cost, amount_paid):
        if amount_paid < cost:
            return False, 0.0
        change = round(amount_paid - cost, 2)
        self.profit += cost
        return True, change

    # Mengembalikan total profit yang sudah terkumpul dalam bentuk teks
    def report(self):
        return f"Uang terkumpul: ${self.profit:.2f}"


# Class utama yang mengatur seluruh antarmuka GUI dan menghubungkan
# Menu, CoffeeMaker, dan CashRegister menjadi satu aplikasi utuh
class CoffeeMachineApp:
    def __init__(self, root):
        self.root = root
        self.menu = Menu()
        self.coffee_maker = CoffeeMaker()
        self.cash_register = CashRegister()

        self.root.title("Coffee Machine")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)

        self._build_layout()
        self._refresh_report()

    # Membangun seluruh komponen tampilan (judul, tombol menu, laporan, status)
    def _build_layout(self):
        title_label = tk.Label(
            self.root,
            text="MESIN KOPI",
            font=("Helvetica", 20, "bold"),
            bg=BACKGROUND_COLOR,
            fg=ACCENT_COLOR,
        )
        title_label.pack(pady=(20, 10))

        button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        for item in self.menu.items:
            btn = tk.Button(
                button_frame,
                text=f"{item.name.capitalize()}\n${item.cost:.2f}",
                width=12,
                height=3,
                bg=BUTTON_COLOR,
                fg=TEXT_COLOR,
                activebackground=ACCENT_COLOR,
                font=("Helvetica", 10, "bold"),
                command=lambda name=item.name: self._select_drink(name),
            )
            btn.pack(side=tk.LEFT, padx=8)

        self.status_label = tk.Label(
            self.root,
            text="Silakan pilih minuman.",
            font=("Helvetica", 11),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            wraplength=340,
            justify="center",
        )
        self.status_label.pack(pady=(15, 10))

        self.report_label = tk.Label(
            self.root,
            text="",
            font=("Courier", 11),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            justify="left",
        )
        self.report_label.pack(pady=(0, 20))

    # Memperbarui tampilan laporan sumber daya dan profit
    def _refresh_report(self):
        text = self.coffee_maker.report() + "\n" + self.cash_register.report()
        self.report_label.config(text=text)

    # Dipanggil saat pengguna memilih salah satu tombol menu
    def _select_drink(self, drink_name):
        drink = self.menu.find_item(drink_name)
        missing = self.coffee_maker.is_resource_sufficient(drink)

        if missing:
            self.status_label.config(
                text=f"Maaf, {', '.join(missing)} tidak mencukupi untuk membuat {drink.name}."
            )
            return

        self._open_payment_window(drink)

    # Membuka jendela kecil untuk memasukkan koin sebagai simulasi pembayaran
    def _open_payment_window(self, drink: MenuItem):
        payment_window = tk.Toplevel(self.root)
        payment_window.title(f"Bayar {drink.name.capitalize()}")
        payment_window.configure(bg=BACKGROUND_COLOR)
        payment_window.resizable(False, False)

        tk.Label(
            payment_window,
            text=f"Harga {drink.name.capitalize()}: ${drink.cost:.2f}",
            bg=BACKGROUND_COLOR,
            fg=ACCENT_COLOR,
            font=("Helvetica", 12, "bold"),
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10))

        coin_labels = ["Quarters (25c):", "Dimes (10c):", "Nickels (5c):", "Pennies (1c):"]
        entries = []

        for i, label_text in enumerate(coin_labels):
            tk.Label(
                payment_window, text=label_text, bg=BACKGROUND_COLOR, fg=TEXT_COLOR
            ).grid(row=i + 1, column=0, sticky="w", padx=15, pady=4)

            entry = tk.Entry(payment_window, width=8)
            entry.insert(0, "0")
            entry.grid(row=i + 1, column=1, padx=15, pady=4)
            entries.append(entry)

        def confirm_payment():
            try:
                quarters = int(entries[0].get())
                dimes = int(entries[1].get())
                nickels = int(entries[2].get())
                pennies = int(entries[3].get())
            except ValueError:
                messagebox.showerror("Input tidak valid", "Mohon masukkan angka bulat untuk setiap koin.")
                return

            amount_paid = self.cash_register.calculate_total(quarters, dimes, nickels, pennies)
            success, change = self.cash_register.process_payment(drink.cost, amount_paid)

            if not success:
                messagebox.showwarning(
                    "Uang tidak cukup",
                    f"Uang yang dimasukkan (${amount_paid:.2f}) kurang dari harga (${drink.cost:.2f}).",
                )
                return

            self.coffee_maker.make_coffee(drink)
            self._refresh_report()

            self.status_label.config(
                text=f"Berikut {drink.name} Anda. Kembalian: ${change:.2f}. Selamat menikmati!"
            )
            payment_window.destroy()

        confirm_btn = tk.Button(
            payment_window,
            text="Konfirmasi Pembayaran",
            bg=ACCENT_COLOR,
            fg=BACKGROUND_COLOR,
            font=("Helvetica", 10, "bold"),
            command=confirm_payment,
        )
        confirm_btn.grid(row=5, column=0, columnspan=2, pady=15)


# Titik masuk program
def main():
    root = tk.Tk()
    app = CoffeeMachineApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()