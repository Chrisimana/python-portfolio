import turtle as turtle_module
import random
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SEGMENT_SIZE = 20
STARTING_LENGTH = 3
MOVE_DISTANCE = 20
GAME_SPEED = 0.1

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


# Merepresentasikan ular, termasuk seluruh segmen tubuh dan pergerakannya
class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    # Membuat segmen awal ular sejumlah STARTING_LENGTH
    def create_snake(self):
        starting_positions = [(0, 0), (-SEGMENT_SIZE, 0), (-SEGMENT_SIZE * 2, 0)]

        for position in starting_positions:
            self.add_segment(position)

    # Menambahkan satu segmen baru ke tubuh ular pada posisi tertentu
    def add_segment(self, position):
        new_segment = turtle_module.Turtle(shape="square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    # Menambah panjang ular satu segmen di posisi segmen terakhir
    def extend(self):
        self.add_segment(self.segments[-1].position())

    # Menggerakkan seluruh tubuh ular: setiap segmen mengikuti posisi segmen di depannya
    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)

        self.head.forward(MOVE_DISTANCE)

    # Mengubah arah hadap kepala ular, mencegah ular berbalik 180 derajat
    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)


# Merepresentasikan makanan yang muncul di posisi acak di dalam layar
class Food(turtle_module.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("lightgreen")
        self.speed("fastest")
        self.refresh()

    # Memindahkan makanan ke posisi acak baru di dalam batas layar
    def refresh(self):
        half_width = (SCREEN_WIDTH // 2) - 40
        half_height = (SCREEN_HEIGHT // 2) - 40

        random_x = random.randint(-half_width, half_width)
        random_y = random.randint(-half_height, half_height)
        self.goto(random_x, random_y)


# Mengelola dan menampilkan skor pemain di layar
class Scoreboard(turtle_module.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, SCREEN_HEIGHT // 2 - 40)
        self.update_display()

    # Menampilkan ulang teks skor dan rekor tertinggi di layar
    def update_display(self):
        self.clear()
        self.write(
            f"Skor: {self.score}  Rekor Tertinggi: {self.high_score}",
            align="center",
            font=("Courier", 16, "normal"),
        )

    # Menambah skor saat ular berhasil memakan makanan
    def increase_score(self):
        self.score += 1
        self.update_display()

    # Menampilkan pesan game over dan memperbarui rekor tertinggi jika perlu
    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score

        self.goto(0, 0)
        self.write(
            "GAME OVER",
            align="center",
            font=("Courier", 24, "bold"),
        )


# Mengelola seluruh alur permainan: layar, input, dan deteksi tabrakan
class SnakeGame:
    def __init__(self):
        self.screen = turtle_module.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title("Snake Game")
        self.screen.tracer(0)

        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()

        self._setup_controls()
        self.game_is_on = True

    # Mendaftarkan tombol panah untuk mengendalikan arah ular
    def _setup_controls(self):
        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")

    # Mengecek apakah kepala ular bertabrakan dengan makanan
    def _check_food_collision(self):
        if self.snake.head.distance(self.food) < 15:
            self.food.refresh()
            self.snake.extend()
            self.scoreboard.increase_score()

    # Mengecek apakah kepala ular menabrak dinding layar
    def _check_wall_collision(self):
        half_width = SCREEN_WIDTH // 2
        half_height = SCREEN_HEIGHT // 2

        if (
            self.snake.head.xcor() > half_width - 10
            or self.snake.head.xcor() < -half_width + 10
            or self.snake.head.ycor() > half_height - 10
            or self.snake.head.ycor() < -half_height + 10
        ):
            self.game_is_on = False
            self.scoreboard.game_over()

    # Mengecek apakah kepala ular menabrak salah satu segmen tubuhnya sendiri
    def _check_tail_collision(self):
        for segment in self.snake.segments[1:]:
            if self.snake.head.distance(segment) < 10:
                self.game_is_on = False
                self.scoreboard.game_over()
                break

    # Loop utama permainan yang berjalan hingga ular menabrak sesuatu
    def run(self):
        while self.game_is_on:
            self.screen.update()
            time.sleep(GAME_SPEED)
            self.snake.move()

            self._check_food_collision()
            self._check_wall_collision()
            self._check_tail_collision()

        self.screen.exitonclick()


# Titik masuk program
def main():
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()