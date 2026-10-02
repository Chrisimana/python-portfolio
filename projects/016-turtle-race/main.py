import turtle as turtle_module
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
FINISH_LINE_X = 230
START_X = -230
LANE_SPACING = 50


# Mengelola seluruh logika dan tampilan balapan kura-kura
class TurtleRace:
    def __init__(self, colors):
        self.colors = colors
        self.screen = None
        self.racers = []
        self.winner = None

    # Menyiapkan layar permainan
    def setup_screen(self):
        self.screen = turtle_module.Screen()
        self.screen.title("Turtle Race")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor("white")

    # Menanyakan tebakan warna pengguna lewat kotak dialog turtle
    def ask_user_guess(self):
        return self.screen.textinput(
            "Tebak Pemenangnya",
            f"Kura-kura warna apa yang akan menang? Pilih dari: {', '.join(self.colors)}",
        )

    # Membuat seluruh kura-kura (racer) dan menempatkannya di garis start
    def create_racers(self):
        total_lanes = len(self.colors)
        start_y = -(total_lanes - 1) * LANE_SPACING / 2

        for index, color in enumerate(self.colors):
            racer = turtle_module.Turtle(shape="turtle")
            racer.color(color)
            racer.penup()
            y_position = start_y + (index * LANE_SPACING)
            racer.goto(START_X, y_position)
            self.racers.append(racer)

    # Menggambar garis start dan garis finis sebagai penanda visual
    def draw_track_lines(self):
        marker = turtle_module.Turtle()
        marker.hideturtle()
        marker.penup()
        marker.speed("fastest")

        for x in (START_X, FINISH_LINE_X):
            marker.goto(x, -120)
            marker.pendown()
            marker.goto(x, 120)
            marker.penup()

    # Menjalankan animasi balapan hingga salah satu kura-kura mencapai garis finis
    def run_race(self):
        while self.winner is None:
            for racer in self.racers:
                distance = random.randint(0, 10)
                racer.forward(distance)

                if racer.xcor() >= FINISH_LINE_X:
                    self.winner = racer.pencolor()
                    break

    # Menampilkan hasil akhir balapan, membandingkan tebakan pengguna dengan pemenang sesungguhnya
    def show_result(self, user_guess):
        if user_guess is None:
            result_text = f"Pemenangnya adalah {self.winner}!"
        elif user_guess.lower() == self.winner.lower():
            result_text = f"Anda benar! Kura-kura {self.winner} memenangkan balapan!"
        else:
            result_text = f"Anda salah tebak. Pemenangnya adalah kura-kura {self.winner}."

        print(result_text)
        self.screen.textinput("Hasil Balapan", result_text + "\nKlik OK untuk keluar.")

    # Menjalankan seluruh alur: setup, buat racer, tanya tebakan, balapan, tampilkan hasil
    def start(self):
        self.setup_screen()
        self.draw_track_lines()
        self.create_racers()

        user_guess = self.ask_user_guess()

        if user_guess is not None:
            self.run_race()
            self.show_result(user_guess)
        else:
            self.run_race()
            self.show_result(None)

        self.screen.bye()


# Titik masuk program
def main():
    race = TurtleRace(COLORS)
    race.start()


if __name__ == "__main__":
    main()