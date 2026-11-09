import pygame
import random
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain on Window Glass Simulation")
clock = pygame.time.Clock()

# Couleurs (Thème Nuit urbaine / Ambiance feutrée)
NIGHT_BG = (15, 20, 32)
GLASS_TINT = (25, 35, 50, 80)
DROP_COLOR = (220, 240, 255, 180)
HIGHLIGHT_COLOR = (255, 255, 255, 220)
TEXT_COLOR = (240, 245, 255)
GRAY = (120, 130, 150)

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

class Drop:
    def __init__(self, x, y, radius, is_moving=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.is_moving = is_moving
        self.speed = random.uniform(0.8, 2.2) if is_moving else 0.0

    def update(self):
        if self.is_moving:
            self.y += self.speed
            # La goutte grossit légèrement en ramassant de l'humidité sur son passage
            self.radius = min(5.5, self.radius + 0.002)

# Initialisation des lumières de la ville en arrière-plan (bokeh)
city_lights = []
for _ in range(40):
    city_lights.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(80, HEIGHT),
        'radius': random.randint(12, 35),
        'color': random.choice([
            (255, 140, 50),   # Jaune/Orange néon
            (50, 180, 255),   # Bleu néon
            (255, 80, 120),   # Rose/Rouge néon
            (200, 200, 255)   # Blanc chaud
        ])
    })

# Liste des gouttes sur la vitre
drops = []

# Surface pour la vitre et les effets de transparence
glass_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                drops = []

    # Créer de nouvelles gouttes de pluie en continu
    if random.random() < 0.4:
        rx = random.randint(20, WIDTH - 20)
        ry = random.randint(80, HEIGHT - 20)
        # 20% de chances qu'elle commence à couler immédiatement
        is_mov = random.random() < 0.2
        drops.append(Drop(rx, ry, random.uniform(1.5, 3.2), is_moving=is_mov))

    # Si on clique ou maintient la souris, on crée de grosses traînées de pluie
    if mouse_pressed[0] and mouse_pos[1] > 80:
        for _ in range(3):
            drops.append(Drop(mouse_pos[0] + random.randint(-8, 8), mouse_pos[1] + random.randint(-8, 8), random.uniform(2.5, 4.5), is_moving=True))

    # Mettre à jour les gouttes
    for d in drops[:]:
        d.update()
        # Si une goutte mobile devient trop lourde, elle se met à couler
        if not d.is_moving and random.random() < 0.005:
            d.is_moving = True

        # Supprimer les gouttes qui sortent de l'écran en bas
        if d.y > HEIGHT - 20:
            drops.remove(d)

    # --- RENDU GRAPHIQUE ---
    screen.fill(NIGHT_BG)

    # 1. Dessiner les lumières de la ville floutées en arrière-plan (Effet Bokeh)
    for l in city_lights:
        surf = pygame.Surface((l['radius'] * 2, l['radius'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*l['color'], 110), (l['radius'], l['radius']), l['radius'])
        screen.blit(surf, (l['x'] - l['radius'], l['y'] - l['radius']))

    # 2. Dessiner la vitre (voile semi-transparent)
    glass_surface.fill((20, 30, 45, 90))
    screen.blit(glass_surface, (0, 0))

    # 3. Dessiner toutes les gouttes d'eau sur la vitre
    for d in drops:
        dx, dy = int(d.x), int(d.y)
        r = int(d.radius)
        
        # Corps de la goutte
        pygame.draw.circle(screen, (180, 210, 230, 200), (dx, dy), r)
        # Reflet lumineux sur la goutte (effet 3D brillant)
        pygame.draw.circle(screen, (255, 255, 255, 240), (dx - max(1, r//3), dy - max(1, r//3)), max(1, r//2.5))

    # --- HUD ET INSTRUCTIONS ---
    title_txt = font_medium.render("RAIN ON WINDOW GLASS — AMBIANCE RELAXANTE", True, TEXT_COLOR)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 12))

    stats_txt = font_small.render(f"Gouttes sur la vitre : {len(drops)}", True, (100, 200, 255))
    screen.blit(stats_txt, (40, 42))

    inst_txt = font_small.render("CLIC GAUCHE (maintenir) : Dessiner de la pluie | R : Essuyer la vitre", True, GRAY)
    screen.blit(inst_txt, (WIDTH - inst_txt.get_width() - 40, 42))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()