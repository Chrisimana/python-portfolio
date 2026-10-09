import pygame
import random
from config import WIDTH

class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x * random.choice([-1, 1])
        self.speed_y = speed_y * random.choice([-1, 1])
        self.initial_speed_x = speed_x
        self.initial_speed_y = speed_y
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
    def bounce_x(self):
        self.speed_x *= -1
    
    def bounce_y(self):
        self.speed_y *= -1
    
    def collide_with_paddle(self, left_paddle, right_paddle):
        if self.rect.colliderect(left_paddle.get_rect()) or self.rect.colliderect(right_paddle.get_rect()):
            return True
        return False
    
    def collide_with_walls(self, screen_height):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            return True
        return False
    
    def check_score(self, screen_width):
        if self.rect.left <= 0:
            return "right"  # Skor untuk pemain kanan
        elif self.rect.right >= screen_width:
            return "left"   # Skor untuk pemain kiri
        return None
    
    def reset(self, x, y):
        self.rect.center = (x, y)
        self.speed_x = self.initial_speed_x * random.choice([-1, 1])
        self.speed_y = self.initial_speed_y * random.choice([-1, 1])
    
    def draw(self, screen, color):
        pygame.draw.ellipse(screen, color, self.rect)