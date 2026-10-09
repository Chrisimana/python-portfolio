import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
    
    def move_up(self):
        self.rect.y -= self.speed
    
    def move_down(self):
        self.rect.y += self.speed
    
    def update(self, screen_height):
        # Batasi paddle agar tidak keluar layar
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    
    def draw(self, screen, color):
        # Efek glow minimalis
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, color, self.rect.inflate(4, 4), 2)
    
    def get_rect(self):
        return self.rect