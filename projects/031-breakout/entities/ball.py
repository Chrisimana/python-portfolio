import pygame

class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.initial_speed_x = speed_x
        self.initial_speed_y = speed_y
        self.stuck = True  # Bola menempel di paddle awal
    
    def update(self):
        if not self.stuck:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
    
    def bounce_x(self):
        self.speed_x *= -1
    
    def bounce_y(self):
        self.speed_y *= -1
    
    def collide_with_paddle(self, paddle):
        if not self.stuck and self.rect.colliderect(paddle.get_rect()) and self.speed_y > 0:
            # Pastikan bola hanya memantul dari atas paddle
            if self.rect.bottom >= paddle.rect.top:
                return True
        return False
    
    def reset(self, x, y):
        self.rect.center = (x, y)
        self.speed_x = self.initial_speed_x
        self.speed_y = self.initial_speed_y
        self.stuck = True
    
    def draw(self, screen, color):
        # Gambar bola dengan efek glow
        pygame.draw.ellipse(screen, color, self.rect)
        pygame.draw.ellipse(screen, color, self.rect.inflate(4, 4), 2)