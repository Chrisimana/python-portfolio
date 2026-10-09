import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.original_width = width
    
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed
    
    def update(self, screen_width):
        # Batasi paddle agar tidak keluar layar
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
    
    def draw(self, screen, color):
        # Gambar paddle dengan efek glow
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, color, self.rect.inflate(6, 6), 2)
        
        # Gradasi sederhana
        for i in range(3):
            pygame.draw.rect(screen, (min(255, color[0] + i*20), 
                                     min(255, color[1] + i*20), 
                                     min(255, color[2] + i*20)), 
                           (self.rect.x, self.rect.y + i*2, 
                            self.rect.width, self.rect.height//3), 1)
    
    def get_rect(self):
        return self.rect