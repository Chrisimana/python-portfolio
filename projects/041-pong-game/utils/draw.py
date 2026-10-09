import pygame

def draw_text(screen, text, font, color, x, y, center=False):
    """Fungsi untuk menggambar teks di layar"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    screen.blit(text_surface, text_rect)

def draw_dashed_line(screen, color, start_pos, end_pos, dash_length=10):
    """Menggambar garis putus-putus"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    dashes = int(length / dash_length)
    
    for i in range(dashes):
        start = (x1 + (x2 - x1) * i / dashes,
                 y1 + (y2 - y1) * i / dashes)
        end = (x1 + (x2 - x1) * (i + 0.5) / dashes,
               y1 + (y2 - y1) * (i + 0.5) / dashes)
        pygame.draw.line(screen, color, start, end, 2)