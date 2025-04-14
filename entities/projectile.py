import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, owner):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vitesse = 10 * direction
        self.owner = owner

    def update(self):
        self.rect.x += self.vitesse
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()

# === main.py (exemple de contenu de base) ===
from db.database import init_db
from core.settings import screen_width, screen_height
from core.utils import draw_text
import pygame

conn, cursor = init_db()