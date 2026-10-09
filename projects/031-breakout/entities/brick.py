import pygame

class Brick:
    def __init__(self, x, y, width, height, color, health=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = health
        self.active = True
    
    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.active = False
        return not self.active
    
    def draw(self, screen):
        if self.active:
            # Gambar brick dengan efek 3D sederhana
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (min(255, self.color[0] + 50),
                                     min(255, self.color[1] + 50),
                                     min(255, self.color[2] + 50)), 
                           self.rect, 2)
            # Efek highlight
            pygame.draw.line(screen, (255, 255, 255), 
                           (self.rect.x, self.rect.y), 
                           (self.rect.right, self.rect.y), 1)

class BrickManager:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.bricks = []
    
    def create_bricks(self):
        from config import BRICK_WIDTH, BRICK_HEIGHT, BRICK_OFFSET_TOP, BRICK_PADDING, BRICK_COLORS
        
        self.bricks = []
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_OFFSET_TOP
                # Warna berdasarkan baris
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, color)
                self.bricks.append(brick)
    
    def check_collision(self, ball):
        for brick in self.bricks:
            if brick.active and ball.rect.colliderect(brick.rect):
                if brick.hit():
                    return True
        return False
    
    def get_remaining_bricks(self):
        return sum(1 for brick in self.bricks if brick.active)
    
    def draw(self, screen, color_list):
        for brick in self.bricks:
            brick.draw(screen)