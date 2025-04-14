import pygame
import sys
import sqlite3


from core.settings import screen_width, screen_height, font, clock, WHITE, BLACK, RED, GREEN, BLUE, YELLOW
from core.utils import draw_text
from entities.joueur import Joueur
from entities.projectile import Projectile

def menu_principal(screen):
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
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return "jeu"
                    elif selected_option == 1:
                        return "options"
                    elif selected_option == 2:
                        return "instructions"
                    elif selected_option == 3:
                        pygame.quit()
                        sys.exit()

        clock.tick(60)

def clavier_virtuel(screen):
    nom_temp = ""
    ligne_selectionnee = 0
    colonne_selectionnee = 0

    clavier = [
        "ABCDEFG",
        "HIJKLMN",
        "OPQRSTU",
        "VWXYZ_<",
        "VALIDER"
    ]

    while True:
        screen.fill((20, 20, 50))
        draw_text("Entrez le nom du Joueur", font, WHITE, screen, screen_width // 2, 50)
        draw_text(f"Nom: {nom_temp}", font, WHITE, screen, screen_width // 2, 100)

        for i, ligne in enumerate(clavier):
            for j, lettre in enumerate(ligne):
                if i == len(clavier) - 1:
                    color = YELLOW if ligne_selectionnee == i else WHITE
                    draw_text(lettre, font, color, screen, screen_width // 2, 200 + i * 50)
                    break

                x = screen_width // 2 - (len(ligne) * 30) // 2 + j * 30
                y = 200 + i * 50
                color = YELLOW if (i == ligne_selectionnee and j == colonne_selectionnee) else WHITE
                draw_text(lettre, font, color, screen, x, y)

        draw_text("Flèches pour naviguer | Entrée pour valider", font, WHITE, screen, screen_width // 2, screen_height - 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Joueur"
                elif event.key == pygame.K_UP:
                    ligne_selectionnee = (ligne_selectionnee - 1) % len(clavier)
                    colonne_selectionnee = min(colonne_selectionnee, len(clavier[ligne_selectionnee]) - 1)
                elif event.key == pygame.K_DOWN:
                    ligne_selectionnee = (ligne_selectionnee + 1) % len(clavier)
                    colonne_selectionnee = min(colonne_selectionnee, len(clavier[ligne_selectionnee]) - 1)
                elif event.key == pygame.K_LEFT and ligne_selectionnee < len(clavier) - 1:
                    colonne_selectionnee = (colonne_selectionnee - 1) % len(clavier[ligne_selectionnee])
                elif event.key == pygame.K_RIGHT and ligne_selectionnee < len(clavier) - 1:
                    colonne_selectionnee = (colonne_selectionnee + 1) % len(clavier[ligne_selectionnee])
                elif event.key == pygame.K_RETURN:
                    if ligne_selectionnee == len(clavier) - 1:
                        return nom_temp if nom_temp else "Joueur"
                    else:
                        lettre = clavier[ligne_selectionnee][colonne_selectionnee]
                        if lettre == '<':
                            nom_temp = nom_temp[:-1]
                        elif lettre == '_':
                            nom_temp += " "
                        else:
                            nom_temp += lettre
        clock.tick(60)

def ecran_de_jeu(screen, conn, cursor):
    controls_p1 = {'up': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'shoot': pygame.K_e}
    controls_p2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_RETURN}

    joueur1 = Joueur(100, screen_height // 2, GREEN, controls_p1)
    joueur2 = Joueur(screen_width - 100, screen_height // 2, BLUE, controls_p2)

        # Charger les paramètres depuis la base de données
    try:
        cursor.execute("SELECT * FROM joueurs WHERE id = 1")
        joueur1_data = cursor.fetchone()
        if joueur1_data:
            joueur1.vitesse = joueur1_data[3]  # vitesse_deplacement
            joueur1.vie = joueur1_data[4]      # points_vie
            joueur1.shot_delay = joueur1_data[6]  # delai_tir
            
        cursotempr.execute("SELECT * FROM joueurs WHERE id = 2")
        joueur2_data = cursor.fetchone()
        if joueur2_data:
            joueur2.vitesse = joueur2_data[3]  # vitesse_deplacement
            joueur2.vie = joueur2_data[4]      # points_vie
            joueur2.shot_delay = joueur2_data[6]  # delai_tir
    except:
        pass  # Si la table n'existe pas encore ou autre erreur

    joueur1.nom = clavier_virtuel(screen)
    joueur2.nom = clavier_virtuel(screen)

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
                return "menu"

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
            return "menu"

        joueurs.draw(screen)
        projectiles.draw(screen)

        pygame.draw.rect(screen, RED, (20, 20, joueur1.vie * 2, 20))
        pygame.draw.rect(screen, BLUE, (screen_width - 220, 20, joueur2.vie * 2, 20))
        draw_text(joueur1.nom, font, WHITE, screen, 100, 50)
        draw_text(joueur2.nom, font, WHITE, screen, screen_width - 100, 50)

        pygame.display.flip()
        clock.tick(60)

def ecran_instructions(screen):
    running = True
    while running:
        screen.fill((20, 20, 50))
        draw_text("Instructions", font, WHITE, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text("Joueur 1 : ZQSD + E", font, WHITE, screen, screen_width // 2, screen_height // 2 - 30)
        draw_text("Joueur 2 : Flèches + Entrée", font, WHITE, screen, screen_width // 2, screen_height // 2 + 10)
        draw_text("ÉCHAP pour revenir au menu", font, WHITE, screen, screen_width // 2, screen_height - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        pygame.display.flip()
        clock.tick(60)

def ecran_options(screen, cursor, conn):
    parametres = [
        {"nom": "Vitesse de déplacement", "attribut": "vitesse", "min": 1, "max": 10, "pas": 1, "valeur_j1": 5, "valeur_j2": 5},
        {"nom": "Points de vie", "attribut": "vie", "min": 50, "max": 200, "pas": 10, "valeur_j1": 100, "valeur_j2": 100},
        {"nom": "Délai de tir (ms)", "attribut": "shot_delay", "min": 100, "max": 1000, "pas": 50, "valeur_j1": 500, "valeur_j2": 500}
    ]

    try:
        cursor.execute("SELECT * FROM joueurs WHERE id = 1")
        joueur1_data = cursor.fetchone()
        if joueur1_data:
            parametres[0]["valeur_j1"] = joueur1_data[3]
            parametres[1]["valeur_j1"] = joueur1_data[4]
            parametres[2]["valeur_j1"] = joueur1_data[6]
        cursor.execute("SELECT * FROM joueurs WHERE id = 2")
        joueur2_data = cursor.fetchone()
        if joueur2_data:
            parametres[0]["valeur_j2"] = joueur2_data[3]
            parametres[1]["valeur_j2"] = joueur2_data[4]
            parametres[2]["valeur_j2"] = joueur2_data[6]
    except:
        pass

    param_selectionne = 0
    joueur_selectionne = 0

    running = True
    while running:
        screen.fill((20, 20, 50))
        draw_text("OPTIONS", font, WHITE, screen, screen_width // 2, 50)
        draw_text("↑/↓: Naviguer | ←/→: Modifier | Tab: Joueur | Entrée: Sauvegarder | ÉCHAP: Retour",
                  pygame.font.Font(None, 24), WHITE, screen, screen_width // 2, screen_height - 30)

        draw_text("Paramètre", font, YELLOW, screen, screen_width // 4, 100)
        draw_text("Joueur 1", font, GREEN, screen, screen_width // 2, 100)
        draw_text("Joueur 2", font, BLUE, screen, 3 * screen_width // 4, 100)

        for i, param in enumerate(parametres):
            couleur_param = YELLOW if i == param_selectionne else WHITE
            draw_text(param["nom"], font, couleur_param, screen, screen_width // 4, 150 + i * 60)
            for j in range(2):
                valeur_cle = "valeur_j1" if j == 0 else "valeur_j2"
                couleur_valeur = GREEN if i == param_selectionne and j == joueur_selectionne and j == 0 else (
                    BLUE if i == param_selectionne and j == joueur_selectionne else WHITE)
                pos_x = screen_width // 2 if j == 0 else 3 * screen_width // 4
                draw_text(str(param[valeur_cle]), font, couleur_valeur, screen, pos_x, 150 + i * 60)

        save_y = 150 + len(parametres) * 60 + 30
        save_selected = param_selectionne == len(parametres)
        save_color = YELLOW if save_selected else WHITE
        pygame.draw.rect(screen, save_color, (screen_width // 2 - 100, save_y - 20, 200, 40), 2)
        draw_text("SAUVEGARDER", font, save_color, screen, screen_width // 2, save_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key == pygame.K_UP:
                    param_selectionne = (param_selectionne - 1) % (len(parametres) + 1)
                elif event.key == pygame.K_DOWN:
                    param_selectionne = (param_selectionne + 1) % (len(parametres) + 1)
                elif event.key == pygame.K_TAB and param_selectionne < len(parametres):
                    joueur_selectionne = 1 - joueur_selectionne
                elif event.key == pygame.K_LEFT and param_selectionne < len(parametres):
                    param = parametres[param_selectionne]
                    valeur_cle = "valeur_j1" if joueur_selectionne == 0 else "valeur_j2"
                    param[valeur_cle] = max(param["min"], param[valeur_cle] - param["pas"])
                elif event.key == pygame.K_RIGHT and param_selectionne < len(parametres):
                    param = parametres[param_selectionne]
                    valeur_cle = "valeur_j1" if joueur_selectionne == 0 else "valeur_j2"
                    param[valeur_cle] = min(param["max"], param[valeur_cle] + param["pas"])
                elif event.key == pygame.K_RETURN and save_selected:
                    for joueur_id in [1, 2]:
                        valeur_cle = "valeur_j1" if joueur_id == 1 else "valeur_j2"
                        cursor.execute("SELECT id FROM joueurs WHERE id = ?", (joueur_id,))
                        exists = cursor.fetchone()
                        if exists:
                            cursor.execute("""
                                UPDATE joueurs 
                                SET vitesse_deplacement = ?, points_vie = ?, delai_tir = ? 
                                WHERE id = ?
                            """, (
                                parametres[0][valeur_cle],
                                parametres[1][valeur_cle],
                                parametres[2][valeur_cle],
                                joueur_id
                            ))
                        else:
                            cursor.execute("""
                                INSERT INTO joueurs 
                                (id, pseudo, vitesse_deplacement, vitesse_rotation, points_vie, puissance_tir, delai_tir, vitesse_projectile) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                joueur_id,
                                f"Joueur {joueur_id}",
                                parametres[0][valeur_cle],
                                1.0,
                                parametres[1][valeur_cle],
                                1.0,
                                parametres[2][valeur_cle],
                                10.0
                            ))
                    conn.commit()
                    draw_text("Paramètres sauvegardés !", font, GREEN, screen, screen_width // 2, screen_height - 80)
                    pygame.display.flip()
                    pygame.time.wait(1000)

        pygame.display.flip()
        clock.tick(60)