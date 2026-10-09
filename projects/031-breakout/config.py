# Konfigurasi Game Breakout
import pygame

# Ukuran layar
WIDTH, HEIGHT = 800, 600
FPS = 60

# Warna (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# Warna brick
BRICK_COLORS = [
    (255, 100, 100),  # Merah
    (255, 150, 100),  # Oranye
    (255, 200, 100),  # Kuning
    (150, 255, 100),  # Hijau muda
    (100, 255, 200),  # Toska
    (100, 200, 255),  # Biru muda
    (150, 100, 255),  # Ungu
]

ACCENT_COLOR = (0, 255, 200)  # Cyan aksen

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 12
PADDLE_SPEED = 7
PADDLE_Y_OFFSET = 50  # Jarak dari bawah

# Ball
BALL_SIZE = 8
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# Brick
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS - 4
BRICK_HEIGHT = 20
BRICK_OFFSET_TOP = 60
BRICK_PADDING = 2

# Power-up
POWERUP_SIZE = 20
POWERUP_SPEED = 3