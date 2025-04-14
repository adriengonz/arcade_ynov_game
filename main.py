import pygame
import sys

from db.database import init_db
from core.settings import screen_width, screen_height, clock, font
from core.screens import menu_principal, ecran_de_jeu, ecran_options, ecran_instructions
from core.utils import draw_text

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shoot em up Duel")

# Initialisation de la base de données
conn, cursor = init_db()

# État actuel de l’écran
current_screen = "menu"

# Boucle principale du jeu
while True:
    if current_screen == "menu":
        current_screen = menu_principal(screen)
    elif current_screen == "jeu":
        current_screen = ecran_de_jeu(screen, conn, cursor)
    elif current_screen == "options":
        current_screen = ecran_options(screen, cursor, conn)
    elif current_screen == "instructions":
        current_screen = ecran_instructions(screen)