import pygame
import sqlite3
import sys
import random

# Connexion à la base SQLite
conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()

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

# Classe Joueur
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
        if keys[self.controls['right']] and self.rect.right < screen_width:
            self.rect.x += self.vitesse
        if keys[self.controls['up']] and self.rect.top > 0:
            self.rect.y -= self.vitesse
        if keys[self.controls['down']] and self.rect.bottom < screen_height:
            self.rect.y += self.vitesse

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_delay:
            self.last_shot = now
            return True
        return False

# Classe Projectile
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
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()

# Initialisation
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Duel Multijoueur")
clock = pygame.time.Clock()

# Couleurs et police
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
font = pygame.font.Font(None, 36)

current_screen = "menu"

# Fonctions utilitaires
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def menu_principal():
    global current_screen
    selected_option = 0
    options = ["Jouer", "Options", "Instructions", "Quitter"]
    running = True
    while running:
        screen.fill(BLACK)
        for i, option in enumerate(options):
            color = WHITE if i == selected_option else (100, 100, 100)
            text = font.render(f"{'->' if i == selected_option else '   '} {option}", True, color)
            screen.blit(text, (screen_width // 2 - 50, screen_height // 2 - 100 + i * 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                    pygame.time.wait(150)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                    pygame.time.wait(150)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        current_screen = "jeu"
                    elif selected_option == 1:
                        current_screen = "options"
                    elif selected_option == 2:
                        current_screen = "instructions"
                    elif selected_option == 3:
                        pygame.quit()
                        sys.exit()
                    running = False

def saisie_nom_joueur(joueur):
    global current_screen
    

    
    # Configuration du clavier virtuel
    clavier = [
        "ABCDEFG",
        "HIJKLMN",
        "OPQRSTU",
        "VWXYZ_<",
        "VALIDER"
    ]
    
    ligne_selectionnee = 0
    colonne_selectionnee = 0

    # Nom temporaire pour l'édition
    nom_temp = ""
    
    running = True
    while running:
        screen.fill(BLACK)
        
        # Affichage du titre
        draw_text(f"Entrez le nom du Joueur", font, WHITE, screen, screen_width // 2, 50)
        
        # Affichage du nom en cours de saisie
        draw_text(f"Nom: {nom_temp}", font, WHITE, screen, screen_width // 2, 100)
        
        # Affichage du clavier virtuel
        for i, ligne in enumerate(clavier):
            for j, lettre in enumerate(ligne):
                # Dernière ligne (VALIDER)
                if i == len(clavier) - 1:
                    if ligne_selectionnee == i:
                        couleur = YELLOW  # Surbrillance
                    else:
                        couleur = WHITE
                    draw_text(lettre, font, couleur, screen, screen_width // 2, 200 + i * 50)
                    break
                
                # Calcul de la position de la lettre
                x = screen_width // 2 - (len(ligne) * 30) // 2 + j * 30
                y = 200 + i * 50
                
                # Détermination de la couleur (surbrillance si sélectionnée)
                couleur = YELLOW if (i == ligne_selectionnee and j == colonne_selectionnee) else WHITE
                
                # Affichage de la lettre
                draw_text(lettre, font, couleur, screen, x, y)
        
        # Instructions
        draw_text("Utilisez les flèches pour naviguer", font, WHITE, screen, screen_width // 2, screen_height - 100)
        draw_text("Appuyez sur ENTRÉE pour sélectionner", font, WHITE, screen, screen_width // 2, screen_height - 60)
        
        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = "menu"
                    joueur.nom = f"Joueur"
                
                # Navigation dans le clavier
                elif event.key == pygame.K_UP:
                    ligne_selectionnee = (ligne_selectionnee - 1) % len(clavier)
                    # Si on arrive à la ligne VALIDER, pas de colonne
                    if ligne_selectionnee == len(clavier) - 1:
                        colonne_selectionnee = 0
                    # Sinon, s'assurer que la colonne est valide pour la nouvelle ligne
                    elif colonne_selectionnee >= len(clavier[ligne_selectionnee]):
                        colonne_selectionnee = len(clavier[ligne_selectionnee]) - 1
                
                elif event.key == pygame.K_DOWN:
                    ligne_selectionnee = (ligne_selectionnee + 1) % len(clavier)
                    # Si on arrive à la ligne VALIDER, pas de colonne
                    if ligne_selectionnee == len(clavier) - 1:
                        colonne_selectionnee = 0
                    # Sinon, s'assurer que la colonne est valide pour la nouvelle ligne
                    elif colonne_selectionnee >= len(clavier[ligne_selectionnee]):
                        colonne_selectionnee = len(clavier[ligne_selectionnee]) - 1
                
                elif event.key == pygame.K_LEFT and ligne_selectionnee < len(clavier) - 1:
                    colonne_selectionnee = (colonne_selectionnee - 1) % len(clavier[ligne_selectionnee])
                
                elif event.key == pygame.K_RIGHT and ligne_selectionnee < len(clavier) - 1:
                    colonne_selectionnee = (colonne_selectionnee + 1) % len(clavier[ligne_selectionnee])
                
                # Sélection d'une lettre ou action
                elif event.key == pygame.K_RETURN:
                    # Si on est sur la ligne VALIDER
                    if ligne_selectionnee == len(clavier) - 1:
                        # Utiliser le nom par défaut si vide
                        if not nom_temp:
                            nom_temp = f"Joueur {joueur_num}"
                        joueur.nom = nom_temp
                        return
                    else:
                        # Récupération de la lettre sélectionnée
                        lettre = clavier[ligne_selectionnee][colonne_selectionnee]
                        
                        # Traitement selon la lettre
                        if lettre == '<':  # Effacer
                            nom_temp = nom_temp[:-1] if nom_temp else ""
                        elif lettre == '_':  # Espace
                            nom_temp += " "
                        else:  # Lettre normale
                            nom_temp += lettre
        
        clock.tick(60)
    
    # Si on sort de la boucle sans return, on assigne un nom par défaut
    joueur.nom = f"Joueur"


def ecran_de_jeu():
    global current_screen

    # Clavier Mac : ZQSD + E pour Joueur 1, Flèches + Entrée pour Joueur 2
    controls_p1 = {'up': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'shoot': pygame.K_e}
    controls_p2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_RETURN}

    joueur1 = Joueur(100, screen_height // 2, GREEN, controls_p1)
    joueur2 = Joueur(screen_width - 100, screen_height // 2, BLUE, controls_p2)

    # Saisie des noms des joueurs
    saisie_nom_joueur(joueur1)
    # Vérifier si l'utilisateur a quitté pendant la saisie
    if current_screen == "menu":
        return
        
    saisie_nom_joueur(joueur2)
    # Vérifier si l'utilisateur a quitté pendant la saisie
    if current_screen == "menu":
        return

    joueurs = pygame.sprite.Group(joueur1, joueur2)
    projectiles = pygame.sprite.Group()

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_screen = "menu"
                running = False

        keys = pygame.key.get_pressed()
        if keys[joueur1.controls['shoot']] and joueur1.can_shoot():
            proj = Projectile(joueur1.rect.right, joueur1.rect.centery, 1, RED, joueur1)
            projectiles.add(proj)
        if keys[joueur2.controls['shoot']] and joueur2.can_shoot():
            proj = Projectile(joueur2.rect.left, joueur2.rect.centery, -1, YELLOW, joueur2)
            projectiles.add(proj)

        joueurs.update()
        projectiles.update()

        for projectile in projectiles:
            if projectile.owner == joueur1 and joueur2.rect.colliderect(projectile.rect):
                joueur2.vie -= 10
                projectile.kill()
            elif projectile.owner == joueur2 and joueur1.rect.colliderect(projectile.rect):
                joueur1.vie -= 10
                projectile.kill()

        if joueur1.vie <= 0 or joueur2.vie <= 0:
            gagnant = joueur1.nom if joueur2.vie <= 0 else joueur2.nom
            draw_text(f"{gagnant} a gagné !", font, WHITE, screen, screen_width // 2, screen_height // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            current_screen = "menu"
            break

        joueurs.draw(screen)
        projectiles.draw(screen)

        pygame.draw.rect(screen, RED, (20, 20, joueur1.vie * 2, 20))
        pygame.draw.rect(screen, BLUE, (screen_width - 220, 20, joueur2.vie * 2, 20))

        draw_text(joueur1.nom, font, WHITE, screen, 100, 50)
        draw_text(joueur2.nom, font, WHITE, screen, screen_width - 100, 50)

        pygame.display.flip()
        clock.tick(60)

def ecran_options():
    global current_screen
    running = True
    while running:
        screen.fill(GREEN)
        draw_text("Options", font, BLACK, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text("Appuyez sur ECHAP pour retourner au menu principal", font, BLACK, screen, screen_width // 2, screen_height - 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_screen = "menu"
                running = False
        pygame.display.flip()
        clock.tick(60)

def ecran_instructions():
    global current_screen
    running = True
    while running:
        screen.fill(RED)
        draw_text("Instructions", font, WHITE, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text("Joueur 1 : ZQSD + E | Joueur 2 : Flèches + Entrée", font, WHITE, screen, screen_width // 2, screen_height // 2)
        draw_text("Appuyez sur ECHAP pour retourner au menu principal", font, WHITE, screen, screen_width // 2, screen_height - 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_screen = "menu"
                running = False
        pygame.display.flip()
        clock.tick(60)

# Boucle principale
while True:
    if current_screen == "menu":
        menu_principal()
    elif current_screen == "jeu":
        ecran_de_jeu()
    elif current_screen == "options":
        ecran_options()
    elif current_screen == "instructions":
        ecran_instructions()