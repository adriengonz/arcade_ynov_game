import pygame

class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vitesse = 5
        self.vie = 100
        self.controls = controls
        self.last_shot = pygame.time.get_ticks()
        self.shot_delay = 500
        self.nom = ""

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']] and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if keys[self.controls['right']] and self.rect.right < 800:
            self.rect.x += self.vitesse
        if keys[self.controls['up']] and self.rect.top > 0:
            self.rect.y -= self.vitesse
        if keys[self.controls['down']] and self.rect.bottom < 600:
            self.rect.y += self.vitesse

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_delay:
            self.last_shot = now
            return True
        return False