import pygame
import sys
from config import *
from game.paddle import Paddle
from game.ball import Ball
from game.score import Score
from utils.draw import draw_text, draw_dashed_line

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        # Inisialisasi objek
        self.left_paddle = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
        self.right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
        self.ball = Ball(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SPEED_X, BALL_SPEED_Y)
        self.score = Score()
        self.running = True
        self.paused = False
        self.game_over = False
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Paddle kiri (W/S)
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()
        
        # Paddle kanan (Arrow keys)
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()
        
        # Pause dengan SPACE
        if keys[pygame.K_SPACE] and not self.game_over:
            self.paused = not self.paused
        
        # Reset dengan R
        if keys[pygame.K_r]:
            self.reset_game()
    
    def update(self):
        if self.paused or self.game_over:
            return
        
        # Update posisi
        self.left_paddle.update(HEIGHT)
        self.right_paddle.update(HEIGHT)
        self.ball.update()
        
        # Tabrakan dengan paddle
        if self.ball.collide_with_paddle(self.left_paddle, self.right_paddle):
            self.ball.bounce_x()
        
        # Tabrakan dengan dinding atas/bawah
        if self.ball.collide_with_walls(HEIGHT):
            self.ball.bounce_y()
        
        # Skor
        scorer = self.ball.check_score(WIDTH)
        if scorer == "left":
            self.score.add_left()
            self.ball.reset(WIDTH//2, HEIGHT//2)
        elif scorer == "right":
            self.score.add_right()
            self.ball.reset(WIDTH//2, HEIGHT//2)
        
        # Cek game over
        if self.score.left >= WINNING_SCORE or self.score.right >= WINNING_SCORE:
            self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Garis tengah putus-putus
        draw_dashed_line(self.screen, GRAY, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 15)
        
        # Gambar paddle dan bola
        self.left_paddle.draw(self.screen, ACCENT)
        self.right_paddle.draw(self.screen, ACCENT)
        self.ball.draw(self.screen, WHITE)
        
        # Gambar skor
        draw_text(self.screen, str(self.score.left), self.big_font, WHITE, WIDTH//4, 30, center=True)
        draw_text(self.screen, str(self.score.right), self.big_font, WHITE, 3*WIDTH//4, 30, center=True)
        
        # Pesan pause
        if self.paused and not self.game_over:
            draw_text(self.screen, "PAUSE", self.font, GRAY, WIDTH//2, HEIGHT//2, center=True)
            draw_text(self.screen, "Tekan SPACE untuk melanjutkan", self.font, GRAY, WIDTH//2, HEIGHT//2 + 40, center=True)
        
        # Pesan game over
        if self.game_over:
            winner = "KIRI" if self.score.left >= WINNING_SCORE else "KANAN"
            draw_text(self.screen, f"{winner} MENANG!", self.big_font, ACCENT, WIDTH//2, HEIGHT//2 - 50, center=True)
            draw_text(self.screen, "Tekan R untuk bermain lagi", self.font, GRAY, WIDTH//2, HEIGHT//2 + 20, center=True)
        
        # Petunjuk kontrol
        controls = [
            "Player Kiri: W / S",
            "Player Kanan: Panah Atas / Bawah",
            "SPACE: Pause",
            "R: Reset"
        ]
        for i, text in enumerate(controls):
            draw_text(self.screen, text, self.font, GRAY, 10, HEIGHT - 100 + i*25, center=False)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = PongGame()
    game.run()