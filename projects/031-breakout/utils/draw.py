import pygame

# Fungsi utilitas untuk menggambar elemen game dengan efek visual sederhana
def draw_text(screen, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    screen.blit(text_surface, text_rect)

# Fungsi untuk menggambar background gradasi
def draw_gradient_background(screen, color1, color2):
    for y in range(screen.get_height()):
        # Interpolasi warna
        ratio = y / screen.get_height()
        r = color1[0] * (1 - ratio) + color2[0] * ratio
        g = color1[1] * (1 - ratio) + color2[1] * ratio
        b = color1[2] * (1 - ratio) + color2[2] * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (screen.get_width(), y))

# Fungsi untuk menggambar persegi panjang dengan sudut melengkung
def draw_rounded_rect(screen, color, rect, radius=5):
    pygame.draw.rect(screen, color, rect, border_radius=radius)

# Fungsi untuk menggambar bayangan sederhana
def draw_shadow(screen, rect, shadow_offset=3):
    shadow_rect = rect.copy()
    shadow_rect.x += shadow_offset
    shadow_rect.y += shadow_offset
    pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect)