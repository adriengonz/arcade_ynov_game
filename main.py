import pygame
import sqlite3
import sys
#import RPi.GPIO as GPIO


# Connexion a la base SQLite
conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()

# Creation des tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS joueurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT,
    vitesse_rotation REAL,
    vitesse_deplacement REAL,
    points_vie INTEGER,
    puissance_tir REAL,
    delai_tir REAL,
    vitesse_projectile REAL
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT,
    score INTEGER
);
""")
conn.commit()

'''
# Configuration des pins GPIO
GPIO.setmode(GPIO.BCM)
joystick_pins = {
    "up": 18,
    "down": 17,
    "left": 23,
    "right": 22,
    "button1": 24,
    "button2": 25
}
for pin in joystick_pins.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Lecture des entrees joystick
def read_joystick():
    return {action: not GPIO.input(pin) for action, pin in joystick_pins.items()}
'''
class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Vert pour le joueur 1
        self.rect = self.image.get_rect(center=(x, y))
        self.vie = 100

    def update(self, joystick_input):
        if joystick_input["up"]:
            self.rect.y -= 5
        if joystick_input["down"]:
            self.rect.y += 5
        if joystick_input["left"]:
            self.rect.x -= 5
        if joystick_input["right"]:
            self.rect.x += 5

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))  # Rouge pour le projectile
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += 10
        if self.rect.left > screen_width:
            self.kill()

#Gestion du clavier virtuel
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
selected_letter = 0

def draw_keyboard():
    for i, letter in enumerate(alphabet):
        color = (255, 255, 255) if i == selected_letter else (100, 100, 100)
        text = font.render(letter, True, color)
        screen.blit(text, (50 + i * 20, screen_height - 50))

def handle_keyboard_input(joystick_input):
    global selected_letter
    if joystick_input["right"]:
        selected_letter = (selected_letter + 1) % len(alphabet)
    elif joystick_input["left"]:
        selected_letter = (selected_letter - 1) % len(alphabet)

# Calcul du score
def calculer_score(vie_restante_joueur1, vie_restante_joueur2, temps_ecoule):
    return int((vie_restante_joueur1 - vie_restante_joueur2) * (100 / temps_ecoule))


pygame.init()

# Dimensions de la fenêtre
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shoot'em Up")
clock = pygame.time.Clock()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Police
font = pygame.font.Font(None, 36)

# Variable pour suivre l'ecran actuel
current_screen = "menu"

# Fonction pour dessiner du texte centre
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Fonction pour gerer le menu principal
def menu_principal():
    global current_screen
    running = True

    while running:
        screen.fill(BLACK)
        draw_text("Menu Principal", font, WHITE, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text("1. Jouer", font, WHITE, screen, screen_width // 2, screen_height // 2)
        draw_text("2. Options", font, WHITE, screen, screen_width // 2, screen_height // 2 + 50)
        draw_text("3. Instructions", font, WHITE, screen, screen_width // 2, screen_height // 2 + 100)
        draw_text("4. Quitter", font, WHITE, screen, screen_width // 2, screen_height // 2 + 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Jouer
                    current_screen = "jeu"
                    running = False
                elif event.key == pygame.K_2:  # Options
                    current_screen = "options"
                    running = False
                elif event.key == pygame.K_3:  # Instructions
                    current_screen = "instructions"
                    running = False
                elif event.key == pygame.K_4:  # Quitter
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Fonction pour gerer l'ecran de jeu
def ecran_de_jeu():
    global current_screen
    running = True

    while running:
        screen.fill(BLUE)  # Fond bleu pour l'ecran de jeu

        draw_text("Écran de Jeu", font, WHITE, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text("Appuyez sur ECHAP pour retourner au menu principal", font,
                  WHITE,
                  screen,
                  screen_width // 2,
                  screen_height - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Retour au menu principal
                    current_screen = "menu"
                    running = False

        pygame.display.flip()
        clock.tick(60)

# Fonction pour gerer l'ecran d'options
def ecran_options():
    global current_screen
    running = True

    while running:
        screen.fill(GREEN)  # Fond vert pour l'ecran d'options

        draw_text("Options", font,
                  BLACK,
                  screen,
                  screen_width // 2,
                  screen_height // 2 - 100)
        draw_text("Appuyez sur ECHAP pour retourner au menu principal", font,
                  BLACK,
                  screen,
                  screen_width // 2,
                  screen_height - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Retour au menu principal
                    current_screen = "menu"
                    running = False

        pygame.display.flip()
        clock.tick(60)

# Fonction pour gerer l'ecran d'instructions
def ecran_instructions():
    global current_screen
    running = True

    while running:
        screen.fill(RED)  # Fond rouge pour l'ecran d'instructions

        draw_text("Instructions", font,
                  WHITE,
                  screen,
                  screen_width // 2,
                  screen_height // 2 - 100)
        draw_text("Appuyez sur ECHAP pour retourner au menu principal", font,
                  WHITE,
                  screen,
                  screen_width // 2,
                  screen_height - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Retour au menu principal
                    current_screen = "menu"
                    running = False

        pygame.display.flip()
        clock.tick(60)

while True:
    if current_screen == "menu":
        menu_principal()
    elif current_screen == "jeu":
        ecran_de_jeu()
    elif current_screen == "options":
        ecran_options()
    elif current_screen == "instructions":
        ecran_instructions()