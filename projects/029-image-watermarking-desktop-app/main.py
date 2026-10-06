import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

BACKGROUND_COLOR = "#20232a"
ACCENT_COLOR = "#61dafb"
TEXT_COLOR = "#f1f1f1"
PREVIEW_MAX_SIZE = (420, 420)


# Menangani seluruh logika pemrosesan gambar: memuat, menambahkan watermark, dan menyimpan
class WatermarkProcessor:
    def __init__(self):
        self.original_image = None
        self.watermarked_image = None

    # Memuat gambar dari path file yang dipilih pengguna
    def load_image(self, file_path):
        self.original_image = Image.open(file_path).convert("RGBA")
        return self.original_image

    # Menambahkan teks watermark ke gambar yang sudah dimuat, mengembalikan hasilnya
    def apply_watermark(self, text, opacity, font_size, position):
        if self.original_image is None:
            raise ValueError("Belum ada gambar yang dimuat.")

        base = self.original_image.copy()
        overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        margin = 20
        positions = {
            "Kanan Bawah": (base.width - text_width - margin, base.height - text_height - margin),
            "Kiri Bawah": (margin, base.height - text_height - margin),
            "Kanan Atas": (base.width - text_width - margin, margin),
            "Kiri Atas": (margin, margin),
            "Tengah": ((base.width - text_width) // 2, (base.height - text_height) // 2),
        }
        text_position = positions.get(position, positions["Kanan Bawah"])

        alpha = int(255 * (opacity / 100))
        draw.text(text_position, text, font=font, fill=(255, 255, 255, alpha))

        self.watermarked_image = Image.alpha_composite(base, overlay)
        return self.watermarked_image

    # Menyimpan hasil gambar berwatermark ke path file tujuan
    def save(self, output_path):
        if self.watermarked_image is None:
            raise ValueError("Belum ada hasil watermark untuk disimpan.")

        final_image = self.watermarked_image.convert("RGB")
        final_image.save(output_path)


# Class utama yang mengatur seluruh antarmuka GUI Image Watermarking
class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.processor = WatermarkProcessor()
        self.loaded_file_path = None

        self.root.title("Image Watermarking Desktop App")
        self.root.configure(bg=BACKGROUND_COLOR, padx=20, pady=20)
        self.root.resizable(False, False)

        self._build_layout()

    # Membangun seluruh komponen tampilan (kontrol kiri, preview kanan)
    def _build_layout(self):
        title_label = tk.Label(
            self.root, text="IMAGE WATERMARKING", font=("Helvetica", 16, "bold"),
            bg=BACKGROUND_COLOR, fg=ACCENT_COLOR,
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        control_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        control_frame.grid(row=1, column=0, sticky="n", padx=(0, 20))

        open_button = tk.Button(control_frame, text="Pilih Gambar", command=self.open_image, width=25)
        open_button.pack(pady=(0, 15))

        tk.Label(control_frame, text="Teks Watermark:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        self.text_entry = tk.Entry(control_frame, width=28)
        self.text_entry.insert(0, "© Nama Anda")
        self.text_entry.pack(pady=(0, 10))

        tk.Label(control_frame, text="Ukuran Font:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        self.font_size_scale = tk.Scale(control_frame, from_=10, to=80, orient="horizontal", length=220)
        self.font_size_scale.set(32)
        self.font_size_scale.pack(pady=(0, 10))

        tk.Label(control_frame, text="Opasitas (%):", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        self.opacity_scale = tk.Scale(control_frame, from_=10, to=100, orient="horizontal", length=220)
        self.opacity_scale.set(70)
        self.opacity_scale.pack(pady=(0, 10))

        tk.Label(control_frame, text="Posisi:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        self.position_var = tk.StringVar(value="Kanan Bawah")
        position_menu = tk.OptionMenu(
            control_frame, self.position_var,
            "Kanan Bawah", "Kiri Bawah", "Kanan Atas", "Kiri Atas", "Tengah",
        )
        position_menu.config(width=20)
        position_menu.pack(pady=(0, 15))

        apply_button = tk.Button(control_frame, text="Terapkan Watermark", command=self.apply_watermark, width=25, bg=ACCENT_COLOR)
        apply_button.pack(pady=(0, 10))

        save_button = tk.Button(control_frame, text="Simpan Gambar", command=self.save_image, width=25)
        save_button.pack()

        self.preview_label = tk.Label(self.root, bg="#111", width=60, height=28)
        self.preview_label.grid(row=1, column=1, sticky="n")

    # Membuka dialog pemilihan file gambar dan menampilkan preview awal
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Gambar", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not file_path:
            return

        self.loaded_file_path = file_path
        image = self.processor.load_image(file_path)
        self._show_preview(image)

    # Menampilkan sebuah objek gambar PIL ke dalam label preview, otomatis diubah ukurannya
    def _show_preview(self, pil_image):
        preview = pil_image.copy()
        preview.thumbnail(PREVIEW_MAX_SIZE)

        tk_image = ImageTk.PhotoImage(preview)
        self.preview_label.config(image=tk_image)
        self.preview_label.image = tk_image  # mencegah garbage collection

    # Dipanggil saat tombol "Terapkan Watermark" ditekan
    def apply_watermark(self):
        if self.loaded_file_path is None:
            messagebox.showwarning("Belum ada gambar", "Mohon pilih gambar terlebih dahulu.")
            return

        text = self.text_entry.get().strip()
        if not text:
            messagebox.showwarning("Teks kosong", "Mohon masukkan teks watermark.")
            return

        result_image = self.processor.apply_watermark(
            text=text,
            opacity=self.opacity_scale.get(),
            font_size=self.font_size_scale.get(),
            position=self.position_var.get(),
        )
        self._show_preview(result_image)

    # Dipanggil saat tombol "Simpan Gambar" ditekan
    def save_image(self):
        if self.processor.watermarked_image is None:
            messagebox.showwarning("Belum ada hasil", "Terapkan watermark terlebih dahulu sebelum menyimpan.")
            return

        default_name = "watermarked_" + os.path.basename(self.loaded_file_path)
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
        )
        if not output_path:
            return

        self.processor.save(output_path)
        messagebox.showinfo("Berhasil", f"Gambar berhasil disimpan ke:\n{output_path}")


def main():
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()