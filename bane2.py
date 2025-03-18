import pygame
import random
import math
from constants import *
from bane import Player
# landskab klasse


class Bane:
    def __init__(self, width, height):
        # initialize funktion banens dimensioner
        self.width = width  # Bredde af banen
        self.height = height  # Højde af banen
        
        platform_width = width * 0.7  # Platform 70% af width
        platform_x = (width - platform_width) / 2  # Center the platform
        platform_y = height * 0.75  # Platform 75% height
        self.platform_segments = [
            pygame.Rect(platform_x, platform_y, platform_width, 20)  # 
        ]
        
        # Void under platform
        self.void_y = platform_y + 30  # Start void a bit below platform
        
        # 
        self.players = [
            Player(200, 400, (255, 0, 0)),  # Player 1 (red)
            Player(550, 400, (0, 0, 255))   # Player 2 (blue)
        ]
        self.tree_positions = [
            {"x": self.width * 0.18, "health": 1.0},  # venstre træ
            
            {"x": self.width * 0.82, "health": 1.0}   # højre træ
        ]
        
        # Farvetemaer for dag og nat gamel kode
        self.color_themes = {
            "day": {
                "background": (135, 206, 235),  # Lyseblå himmel
                "mountain": (101, 67, 33),  # Brun bjerg
                "ground": (34, 139, 34),  # Grøn jord
                "platform": (139, 69, 19)  # Brun platform
            },
            "night": {
                "background": (25, 25, 112),  # Mørkeblå nattehimmel
                "mountain": (72, 61, 139),  # Mørklilla bjerg
                "ground": (0, 100, 0),  # Mørkegrøn jord
                "platform": (85, 45, 10)  # Mørkebrun platform
            }
        }
        
        # Aktuelle farvetema (starter med dag)
        self.current_theme = "day"
        
        # Tid for sidste temaændring
        self.last_theme_change = 0
        
        # Interval for temaændring i millisekunder (10 sekunder)
        self.theme_change_interval = 10000

    # Hent de aktuelle farver baseret på temaet
    def get_current_colors(self):
        # Returner farverne for det aktuelle tema
        return self.color_themes[self.current_theme]

    # Opdater banen (f.eks. skift mellem dag og nat)
    def update(self, current_time):
        # Tjek om det er tid til at skifte tema
        if current_time - self.last_theme_change > self.theme_change_interval:
            # Skift mellem dag og nat
            self.current_theme = "night" if self.current_theme == "day" else "day"
            # Opdater tidspunkt for sidste ændring
            self.last_theme_change = current_time

        for player in self.players:
            player.fysik(self.platform_segments[0])

        self.handle_collisions()

    # Tegn banen med alle elementer 
    def draw(self, surface: pygame.Surface):
        # Hent de aktuelle farver
        colors = self.get_current_colors()
        
        # Opret gradient himmel - mørk indigo til marineblå for skumring/nat effekt
        for y in range(self.height):
            # Opret gradient fra mørk indigo øverst til marineblå nær horisonten
            gradient_value = max(0, min(50 + y // 2, 80))
            pygame.draw.line(surface, (gradient_value//2, gradient_value//2, gradient_value), 
                          (0, y), (self.width, y))
        
        # Draw void area (dark abyss below platform)
        void_rect = pygame.Rect(0, self.void_y, self.width, self.height - self.void_y)
        pygame.draw.rect(surface, (10, 10, 15), void_rect)
        
        # Add some particle effects in the void
        for _ in range(20):
            particle_x = random.randint(0, self.width)
            particle_y = random.randint(int(self.void_y), self.height)
            particle_size = random.randint(1, 3)
            particle_color = (30, 30, 40)
            pygame.draw.circle(surface, particle_color, (particle_x, particle_y), particle_size)
        
        # Tegn fjerne bakker
        hill_color = (30, 40, 45)  # Mørke blå-grønne bakker
        hills = [
            # Venstre fjerne bakker
            [(0, self.height * 0.6), 
             (self.width * 0.15, self.height * 0.55), 
             (self.width * 0.35, self.height * 0.58), 
             (self.width * 0.4, self.height * 0.6)],
            # Højre fjerne bakker
            [(self.width * 0.6, self.height * 0.6), 
             (self.width * 0.7, self.height * 0.57), 
             (self.width * 0.9, self.height * 0.59), 
             (self.width, self.height * 0.58), 
             (self.width, self.height * 0.65)]
        ]
        
        # Tegn hver bakke som en polygon
        for hill in hills:
            pygame.draw.polygon(surface, hill_color, hill)
        
        # Tegn Mount Fuji i midten
        # Bjergets base (mørk del)
        mountain_base = [
            (self.width * 0.5, self.height * 0.2),    # Toppunkt
            (self.width * 0.46, self.height * 0.25),  # Let kurve til højre for toppen
            (self.width * 0.42, self.height * 0.28),  # Højre skulder
            (self.width * 0.36, self.height * 0.35),  # Højre skråning
            (self.width * 0.28, self.height * 0.45),  # Midt-højre skråning
            (self.width * 0.2, self.height * 0.55),   # Nedre højre skråning
            (self.width * 0.12, self.height * 0.7),   # Højre base
            (self.width * 0.88, self.height * 0.7),   # Venstre base
            (self.width * 0.8, self.height * 0.55),   # Nedre venstre skråning
            (self.width * 0.72, self.height * 0.45),  # Midt-venstre skråning
            (self.width * 0.64, self.height * 0.35),  # Venstre skråning
            (self.width * 0.58, self.height * 0.28),  # Venstre skulder
            (self.width * 0.54, self.height * 0.25),  # Let kurve til venstre for toppen
        ]
        # Tegn bjergets base med mørk brun-grå farve
        pygame.draw.polygon(surface, (60, 50, 55), mountain_base)
        
        # Tegn snehætte med uregelmæssig, naturlig kant
        snow_cap = [
            (self.width * 0.5, self.height * 0.2),    # Toppunkt
            (self.width * 0.46, self.height * 0.25),  # Højre for toppen
            (self.width * 0.42, self.height * 0.28),  # Højre skulder
            (self.width * 0.39, self.height * 0.31),  # Sne dyk 1
            (self.width * 0.37, self.height * 0.32),  # Sne punkt 1
            (self.width * 0.35, self.height * 0.33),  # Sne dyk 2
            (self.width * 0.33, self.height * 0.34),  # Sne punkt 2
            (self.width * 0.31, self.height * 0.39),  # Sne dyk 3
            (self.width * 0.29, self.height * 0.4),   # Sne kurve
            (self.width * 0.28, self.height * 0.41),  # Sne slut højre
            (self.width * 0.72, self.height * 0.41),  # Sne slut venstre
            (self.width * 0.71, self.height * 0.4),   # Sne kurve
            (self.width * 0.69, self.height * 0.39),  # Sne dyk 3 spejl
            (self.width * 0.67, self.height * 0.34),  # Sne punkt 2 spejl
            (self.width * 0.65, self.height * 0.33),  # Sne dyk 2 spejl
            (self.width * 0.63, self.height * 0.32),  # Sne punkt 1 spejl
            (self.width * 0.61, self.height * 0.31),  # Sne dyk 1 spejl
            (self.width * 0.58, self.height * 0.28),  # Venstre skulder
            (self.width * 0.54, self.height * 0.25),  # Venstre for toppen
        ]
        # Tegn snehætten med hvid farve
        pygame.draw.polygon(surface, (240, 240, 240), snow_cap)
        
        # Tegn kirsebærtræer (stiliseret)
        self.draw_cherry_tree(self.width * 0.18, self.height * 0.2, self.tree_positions[0]["health"], surface=surface)
        self.draw_cherry_tree(self.width * 0.82, self.height * 0.2, self.tree_positions[1]["health"], flip=True, surface=surface)
        
        # Tegn en torii-port silhuet (traditionel japansk port)
        torii_color = (180, 40, 40)  # Rød torii-port
        torii_x = self.width * 0.5
        torii_y = self.height * 0.65
        torii_width = self.width * 0.15
        torii_height = self.height * 0.1
        
        # Torii søjler
        pygame.draw.rect(surface, torii_color, 
                      (torii_x - torii_width/2, torii_y, 
                       torii_width * 0.1, torii_height))
        pygame.draw.rect(surface, torii_color, 
                      (torii_x + torii_width/2 - torii_width * 0.1, torii_y, 
                       torii_width * 0.1, torii_height))
        
        # Torii topbjælker
        pygame.draw.rect(surface, torii_color, 
                      (torii_x - torii_width/2 - torii_width * 0.05, 
                       torii_y, torii_width * 1.1, torii_height * 0.15))
        pygame.draw.rect(surface, torii_color, 
                      (torii_x - torii_width/2, torii_y + torii_height * 0.25, 
                       torii_width, torii_height * 0.1))
        
        # Tegn jorden med lidt tekstur
        ground_rect = pygame.Rect(0, self.height * 0.7, self.width, self.height * 0.3)
        pygame.draw.rect(surface, (40, 50, 40), ground_rect)
        
        # Tilføj græs/tekstur til jorden
        for _ in range(100):
            grass_x = random.randint(0, self.width)
            grass_height = random.randint(2, 5)
            pygame.draw.line(surface, (50, 70, 50), 
                          (grass_x, self.height * 0.7), 
                          (grass_x, self.height * 0.7 - grass_height))
        
        # Tegn platform og andre spilelementer
        for platform in self.platform_segments:
            # Hovedplatform med traditionel træfarve
            pygame.draw.rect(surface, (120, 80, 40), platform)
            
            # Tilføj dekorative linjer (som træårer)
            line_spacing = 20
            for y in range(platform.top, platform.bottom, line_spacing):
                pygame.draw.line(surface, (90, 60, 30),
                               (platform.left, y),
                               (platform.right, y), 2)
            
            # Tilføj platformkanter
            pygame.draw.rect(surface, (90, 60, 30), platform, 4)
            
            # Tilføj traditionelle japanske platformendestykker
            cap_width = 8
            pygame.draw.rect(surface, (140, 90, 40), 
                          (platform.left - cap_width//2, platform.top - 5,
                           platform.width + cap_width, 10))

        # Add platform edges/shadows
        for platform in self.platform_segments:
            # Bottom shadow
            pygame.draw.rect(surface, (80, 50, 25), 
                           (platform.left, platform.bottom, platform.width, 3))
            # Side shadows
            pygame.draw.rect(surface, (100, 65, 35), 
                           (platform.left - 2, platform.top, 2, platform.height))
            pygame.draw.rect(surface, (100, 65, 35), 
                           (platform.right, platform.top, 2, platform.height))

        for player in self.players:
            player.draw(surface)

        # Draw damage percentage for each player
        font = pygame.font.Font(None, 36)
        for i, player in enumerate(self.players):
            damage_text = f"{int(player.damage)}%"
            text_surface = font.render(damage_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.tree_positions[i]["x"]
            text_rect.y = self.height * 0.2
            surface.blit(text_surface, text_rect)

    # Tjek om en position er på en platform
    def is_on_platform(self, x, y):
        # Gennemgå alle platformsegmenter
        for platform in self.platform_segments:
            # Tjek om positionen er inden for platformens grænser
            if platform.collidepoint(x, y):
                return True
        # Hvis ingen platform blev fundet, returner False
        return False

    # Find y-koordinaten for den øverste platform ved en given x-koordinat
    def get_platform_y(self, x):
        # Initialiser med en høj værdi
        min_y = float('inf')
        # Gennemgå alle platformsegmenter
        for platform in self.platform_segments:
            # Tjek om x-koordinaten er inden for platformens x-grænser
            if platform.left <= x <= platform.right:
                # Opdater min_y hvis denne platform er højere oppe
                min_y = min(min_y, platform.top)
        # Returner den fundne y-koordinat eller None hvis ingen platform blev fundet
        return min_y if min_y != float('inf') else None

    def handle_input(self):
        # Player 1: WASD + LSHIFT for charge
        self.players[0].move(pygame.K_a, pygame.K_d, pygame.K_LSHIFT, pygame.K_w, self.platform_segments[0])
        # Player 2: Arrow keys + RSHIFT for charge
        self.players[1].move(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT, pygame.K_UP, self.platform_segments[0])

    def handle_collisions(self):
        player1, player2 = self.players
        center1 = player1.hentmidt()
        center2 = player2.hentmidt()

        # Calculate the distance between the players
        distance = math.dist(center1, center2)

        # Check if players are colliding
        if distance < PLAYER_RADIUS * 2:
            # Calculate momentum and damage
            p1_momentum = player1.hentpower()
            p2_momentum = player2.hentpower()
            
            # The player with more momentum deals more damage
            if p1_momentum > p2_momentum:
                damage = p1_momentum * DAMAGE_MULTIPLIER
                player2.damage += damage
                knockback_mult = 1 + (player2.damage / 100)  # Increased knockback with damage
                player2.fart_x = BASE_KNOCKBACK * knockback_mult * (1 if center1[0] < center2[0] else -1)
                player2.fart_y = -5  # Add some vertical knockback
                
                # Update right tree health
                self.tree_positions[1]["health"] = max(0, 1 - (player2.damage / 100))
                
            elif p2_momentum > p1_momentum:
                damage = p2_momentum * DAMAGE_MULTIPLIER
                player1.damage += damage
                knockback_mult = 1 + (player1.damage / 100)  # Increased knockback with damage
                player1.fart_x = BASE_KNOCKBACK * knockback_mult * (1 if center2[0] < center1[0] else -1)
                player1.fart_y = -5  # Add some vertical knockback
                
                # Update left tree health
                self.tree_positions[0]["health"] = max(0, 1 - (player1.damage / 100))

            # Separate players
            overlap = PLAYER_RADIUS * 2 - distance
            direction = (center1[0] - center2[0], center1[1] - center2[1])
            if direction[0] != 0 or direction[1] != 0:  # Avoid division by zero
                norm = math.sqrt(direction[0]**2 + direction[1]**2)
                direction = (direction[0] / norm, direction[1] / norm)
                player1.rect.x += direction[0] * overlap / 2
                player1.rect.y += direction[1] * overlap / 2
                player2.rect.x -= direction[0] * overlap / 2
                player2.rect.y -= direction[1] * overlap / 2

        # Check for ring out (falling into void)
        for i, player in enumerate(self.players):
            if player.rect.top > self.void_y:
                # Player has fallen into the void
                player.damage = 100  # Max damage
                self.tree_positions[i]["health"] = 0  # Destroy their tree
                # Reset player position
                player.rect.x = 200 if i == 0 else 550
                player.rect.y = 400
                player.fart_x = 0
                player.fart_y = 0

    def draw_cherry_tree(self, x, height, health, flip=False, surface=None):
        if surface is None:
            return
            
        # Træstamme - darker and more defined
        trunk_width = self.width * 0.025
        trunk_height = self.height * 0.15
        
        # Main trunk
        trunk = pygame.Rect(
            x - trunk_width // 2,
            self.height * 0.7 - trunk_height,
            trunk_width,
            trunk_height
        )
        # Draw trunk with darker brown and outline
        pygame.draw.rect(surface, (45, 30, 20), trunk)
        pygame.draw.rect(surface, (35, 20, 15), trunk, 2)
        
        # Define tree foliage as connected circles in pixel art style
        foliage_center_y = self.height * 0.7 - trunk_height - self.height * 0.08
        foliage_radius = self.width * 0.06 * health  # Scale foliage with health
        
        # Draw main foliage shapes
        foliage_positions = [
            (x, foliage_center_y),  # Center
            (x - foliage_radius * 0.7, foliage_center_y + foliage_radius * 0.3),  # Left
            (x + foliage_radius * 0.7, foliage_center_y + foliage_radius * 0.3),  # Right
            (x, foliage_center_y + foliage_radius * 0.5),  # Bottom
            (x, foliage_center_y - foliage_radius * 0.5),  # Top
        ]
        
        # Calculate damage-based colors
        damage_factor = 1 - health
        base_color = (
            min(255, 200 + int(damage_factor * 55)),  # More red with damage
            max(0, 100 - int(damage_factor * 100)),   # Less green with damage
            max(0, 150 - int(damage_factor * 150))    # Less blue with damage
        )
        light_color = (
            min(255, 255 - int(damage_factor * 73)),
            max(0, 182 - int(damage_factor * 182)),
            max(0, 193 - int(damage_factor * 193))
        )
        
        # Draw foliage with damage-based colors
        for pos_x, pos_y in foliage_positions:
            pygame.draw.circle(surface, base_color, (int(pos_x), int(pos_y)), int(foliage_radius))
            pygame.draw.circle(surface, light_color, (int(pos_x), int(pos_y)), int(foliage_radius * 0.85))
