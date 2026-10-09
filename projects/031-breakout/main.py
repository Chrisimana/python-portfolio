import pygame
import sys
from config import *
from entities.paddle import Paddle
from entities.ball import Ball
from entities.brick import BrickManager
from utils.draw import draw_text, draw_gradient_background

class BreakoutGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Flag untuk tracking penekanan space
        self.space_pressed_last_frame = False
        
        self.reset_game()
    
    def reset_game(self):
        # Inisialisasi objek
        self.paddle = Paddle(
            WIDTH//2 - PADDLE_WIDTH//2,
            HEIGHT - PADDLE_Y_OFFSET,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_SPEED
        )
        
        self.ball = Ball(
            WIDTH//2,
            HEIGHT - PADDLE_Y_OFFSET - 20,
            BALL_SIZE,
            BALL_SPEED_X,
            BALL_SPEED_Y
        )
        
        self.brick_manager = BrickManager(BRICK_ROWS, BRICK_COLS)
        self.brick_manager.create_bricks()
        
        self.score = 0
        self.lives = 3
        self.running = True
        self.paused = False
        self.game_over = False
        self.victory = False
        
        # Efek visual
        self.particle_effect = []
        self.flash_effect = 0
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Kontrol paddle
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move_right()
        
        # Reset dengan R
        if keys[pygame.K_r]:
            self.reset_game()
    
    def update(self):
        if self.paused or self.game_over or self.victory:
            return
        
        # Update posisi
        self.paddle.update(WIDTH)
        
        # Update ball
        self.ball.update()
        
        # Bola menempel di paddle (mode start)
        if self.ball.stuck:
            self.ball.rect.centerx = self.paddle.rect.centerx
            self.ball.rect.bottom = self.paddle.rect.top - 5
        
        # Tabrakan dengan paddle
        if self.ball.collide_with_paddle(self.paddle):
            self.ball.bounce_y()
            # Efek berdasarkan posisi tumbukan
            hit_pos = (self.ball.rect.centerx - self.paddle.rect.left) / PADDLE_WIDTH
            angle = (hit_pos - 0.5) * 2  # -1 sampai 1
            self.ball.speed_x += angle * 2
            # Batasi kecepatan
            self.ball.speed_x = max(-7, min(7, self.ball.speed_x))
        
        # Tabrakan dengan dinding
        if self.ball.rect.left <= 0 or self.ball.rect.right >= WIDTH:
            self.ball.bounce_x()
        if self.ball.rect.top <= 0:
            self.ball.bounce_y()
        
        # Bola jatuh (kehilangan nyawa)
        if self.ball.rect.top >= HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.reset_ball()
            else:
                self.game_over = True
        
        # Tabrakan dengan brick
        hit_brick = self.brick_manager.check_collision(self.ball)
        if hit_brick:
            self.score += 10
            self.ball.bounce_y()
            
            # Efek flash
            self.flash_effect = 5
            
            # Cek kemenangan
            if self.brick_manager.get_remaining_bricks() == 0:
                self.victory = True
    
    def reset_ball(self):
        self.ball.stuck = True
        self.ball.rect.centerx = WIDTH//2
        self.ball.rect.bottom = self.paddle.rect.top - 5
        self.ball.speed_x = BALL_SPEED_X
        self.ball.speed_y = -BALL_SPEED_Y
    
    def draw(self):
        # Background gradasi
        draw_gradient_background(self.screen, BLACK, GRAY)
        
        # Efek flash saat menghancurkan brick
        if self.flash_effect > 0:
            flash_surface = pygame.Surface((WIDTH, HEIGHT))
            flash_surface.set_alpha(100)
            flash_surface.fill(WHITE)
            self.screen.blit(flash_surface, (0, 0))
            self.flash_effect -= 1
        
        # Gambar semua brick
        self.brick_manager.draw(self.screen, BRICK_COLORS)
        
        # Gambar paddle
        self.paddle.draw(self.screen, ACCENT_COLOR)
        
        # Gambar ball
        self.ball.draw(self.screen, WHITE)
        
        # Tampilkan skor dan nyawa
        draw_text(self.screen, f"SCORE: {self.score}", self.font, WHITE, 20, 20)
        
        # Tampilan nyawa (bullet points)
        for i in range(self.lives):
            pygame.draw.circle(self.screen, ACCENT_COLOR, (WIDTH - 40 - i*30, 35), 8)
        
        # Pesan pause
        if self.paused and not self.game_over and not self.victory:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, "PAUSE", self.big_font, WHITE, WIDTH//2, HEIGHT//2 - 50, center=True)
            draw_text(self.screen, "Tekan SPACE untuk melanjutkan", self.font, LIGHT_GRAY, WIDTH//2, HEIGHT//2 + 20, center=True)
        
        # Pesan game over
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, "GAME OVER", self.big_font, ACCENT_COLOR, WIDTH//2, HEIGHT//2 - 50, center=True)
            draw_text(self.screen, f"Skor Akhir: {self.score}", self.font, WHITE, WIDTH//2, HEIGHT//2 + 20, center=True)
            draw_text(self.screen, "Tekan R untuk bermain lagi", self.font, LIGHT_GRAY, WIDTH//2, HEIGHT//2 + 70, center=True)
        
        # Pesan kemenangan
        if self.victory:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, "VICTORY!", self.big_font, ACCENT_COLOR, WIDTH//2, HEIGHT//2 - 50, center=True)
            draw_text(self.screen, f"Skor Akhir: {self.score}", self.font, WHITE, WIDTH//2, HEIGHT//2 + 20, center=True)
            draw_text(self.screen, "Tekan R untuk bermain lagi", self.font, LIGHT_GRAY, WIDTH//2, HEIGHT//2 + 70, center=True)
        
        # Petunjuk kontrol
        if not self.game_over and not self.victory and not self.paused:
            controls = [
                "A D  : Gerakan paddle",
                "SPACE : Lempar bola / Pause",
                "R : Reset permainan"
            ]
            for i, text in enumerate(controls):
                draw_text(self.screen, text, pygame.font.Font(None, 20), WHITE, 20, HEIGHT - 70 + i*20)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                # Handle space key press sebagai event, bukan continuous state
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Pause atau lempar bola
                        if not self.game_over and not self.victory:
                            if self.ball.stuck:
                                # Lempar bola
                                self.ball.stuck = False
                            else:
                                # Toggle pause
                                self.paused = not self.paused
            
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = BreakoutGame()
    game.run()