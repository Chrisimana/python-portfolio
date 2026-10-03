import tkinter as tk
import math

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
SESSIONS_BEFORE_LONG_BREAK = 4


# Mengelola seluruh logika timer Pomodoro: sesi, hitung mundur, dan status
class PomodoroTimer:
    def __init__(self, on_tick, on_session_complete):
        self.on_tick = on_tick
        self.on_session_complete = on_session_complete
        self.reps = 0
        self.timer_job = None
        self.is_running = False

    # Menentukan jenis sesi berikutnya (kerja, istirahat pendek, atau panjang)
    def _get_next_session(self):
        self.reps += 1

        if self.reps % (SESSIONS_BEFORE_LONG_BREAK * 2) == 0:
            return "Istirahat Panjang", LONG_BREAK_MIN * 60
        elif self.reps % 2 == 0:
            return "Istirahat Pendek", SHORT_BREAK_MIN * 60
        else:
            return "Waktunya Fokus", WORK_MIN * 60

    # Memulai sesi berikutnya dan menjalankan hitung mundur
    def start_next_session(self, canvas_update_callback):
        session_name, total_seconds = self._get_next_session()
        self.canvas_update_callback = canvas_update_callback
        self._count_down(session_name, total_seconds)

    # Menjalankan hitung mundur satu detik demi satu detik secara rekursif
    def _count_down(self, session_name, remaining_seconds):
        minutes = math.floor(remaining_seconds / 60)
        seconds = remaining_seconds % 60
        time_text = f"{minutes:02d}:{seconds:02d}"

        self.on_tick(session_name, time_text)
        self.canvas_update_callback(time_text)

        if remaining_seconds > 0:
            self.timer_job = self._schedule(1000, self._count_down, session_name, remaining_seconds - 1)
        else:
            self.on_session_complete(session_name, self.reps)

    # Membungkus pemanggilan root.after agar class ini tidak bergantung langsung pada Tkinter
    def _schedule(self, delay_ms, func, *args):
        return self._after_func(delay_ms, lambda: func(*args))

    # Menghubungkan fungsi penjadwalan (root.after) dari luar class
    def set_scheduler(self, after_func, cancel_func):
        self._after_func = after_func
        self._cancel_func = cancel_func

    # Menghentikan dan mengatur ulang timer ke kondisi awal
    def reset(self):
        if self.timer_job is not None:
            self._cancel_func(self.timer_job)
            self.timer_job = None
        self.reps = 0


# Class utama yang mengatur seluruh antarmuka GUI Pomodoro
class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.timer = PomodoroTimer(
            on_tick=self._update_title,
            on_session_complete=self._handle_session_complete,
        )
        self.timer.set_scheduler(self.root.after, self.root.after_cancel)

        self.root.title("Pomodoro Timer")
        self.root.configure(bg=YELLOW, padx=40, pady=30)
        self.root.resizable(False, False)

        self._build_layout()

    # Membangun seluruh komponen tampilan (judul, canvas, label, tombol, checkmark)
    def _build_layout(self):
        self.title_label = tk.Label(
            self.root, text="Timer", font=(FONT_NAME, 32, "bold"), bg=YELLOW, fg=GREEN
        )
        self.title_label.grid(row=0, column=1)

        self.canvas = tk.Canvas(self.root, width=220, height=224, bg=YELLOW, highlightthickness=0)
        self.timer_text = self.canvas.create_text(
            110, 112, text="25:00", fill="white", font=(FONT_NAME, 32, "bold")
        )
        self.canvas.grid(row=1, column=1)

        self.start_button = tk.Button(
            self.root, text="Mulai", highlightthickness=0, command=self.start_timer
        )
        self.start_button.grid(row=2, column=0)

        self.reset_button = tk.Button(
            self.root, text="Reset", highlightthickness=0, command=self.reset_timer
        )
        self.reset_button.grid(row=2, column=2)

        self.check_label = tk.Label(self.root, text="", bg=YELLOW, fg=GREEN)
        self.check_label.grid(row=3, column=1)

    # Memperbarui label judul sesuai jenis sesi yang sedang berjalan
    def _update_title(self, session_name, time_text):
        color = GREEN if session_name == "Waktunya Fokus" else PINK if "Pendek" in session_name else RED
        self.title_label.config(text=session_name, fg=color)

    # Memperbarui teks hitung mundur di dalam canvas
    def _update_canvas(self, time_text):
        self.canvas.itemconfig(self.timer_text, text=time_text)

    # Dipanggil saat sesi mencapai 00:00, melanjutkan ke sesi berikutnya dan menambah checkmark
    def _handle_session_complete(self, session_name, reps):
        if session_name == "Waktunya Fokus":
            completed_sessions = reps // 2
            self.check_label.config(text=f"Sesi kerja selesai: {completed_sessions}")

        self.timer.start_next_session(self._update_canvas)

    # Dipanggil saat tombol Mulai ditekan
    def start_timer(self):
        self.start_button.config(state="disabled")
        self.timer.start_next_session(self._update_canvas)

    # Mengatur ulang seluruh tampilan dan state timer ke kondisi awal
    def reset_timer(self):
        self.timer.reset()
        self.canvas.itemconfig(self.timer_text, text="25:00")
        self.title_label.config(text="Timer", fg=GREEN)
        self.check_label.config(text="")
        self.start_button.config(state="normal")


# Titik masuk program
def main():
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()