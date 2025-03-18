import pygame
import random
import math
from constants import *

class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.fart_x = 0  # vandret fart
        self.fart_y = 0  # lodret fart
        self.skade = 0   # hvor meget skade spilleren har taget
        self.retning = 1 # 1 = højre, -1 = venstre
        self.oplader = False  # om vi er ved at lade op til angreb 
        self.styrke = 0      # hvor meget kraft der er i angrebet
        self.powerup = False  # om vi er ved at lave en special attack
        self.energi = 0      # hvor meget power der er i special tackhauduken
        self.damage = 0  #

    def move(self, v, h, boost, hop, platform):
        # v = venstre knap, h = højre knap
        k = pygame.key.get_pressed()
        
        # tjek hvilken vej vi kigger
        if k[v]:
            self.retning = -1 #venstre
            if not self.oplader:
                self.fart_x = -PLAYER_SPEED
        if k[h]:
            self.retning = 1 #højre
            if not self.oplader:
                self.fart_x = PLAYER_SPEED
                
        # angrebs charge
        if k[boost]:
            self.oplader = True
            self.styrke = min(self.styrke + 0.2, MAX_CHARGE_POWER)
            self.fart_x *= 0.1  # sænk farten mens vi lader op
        elif self.oplader: #oplader = charge
            self.oplader = False
            self.fart_x = self.retning * (PLAYER_SPEED + self.styrke * 2)
            self.styrke = 0
            
        # hop kun hvis vi rører platformen
        if k[hop] and self.rect.bottom >= platform.top: #HAR EN BBUG, man kan hoppe i luften, da den kun tjekker for pos AZAD FIX
            self.fart_y = JUMP_STRENGTH

    def fysik(self, platform):
        # tyngdekraft osv
        self.fart_y += GRAVITY
        self.rect.x += self.fart_x
        self.rect.y += self.fart_y
        self.fart_x *= FRICTION  # friktion i luften osv

        # tjek om vi rammer platformen (og er over den)
        if self.rect.bottom >= platform.top and self.rect.left < platform.right and self.rect.right > platform.left: #FIX AZAD
            self.rect.bottom = platform.top
            self.fart_y = 0
            
        # bliv på skærmen (vandret)
        if self.rect.left < 0:
            self.rect.left = 0
            self.fart_x = 0
        elif self.rect.right > 800:
            self.rect.right = 800
            self.fart_x = 0

    def draw(self, vindue): #power bar draw øhhhh
        # tegn power bar hvis vi lader op 
        if self.oplader:
            kraft = 50 * (self.styrke / MAX_CHARGE_POWER)
            powerbar = pygame.Rect(self.rect.x, self.rect.y - 10, kraft, 5)
            pygame.draw.rect(vindue, (255, 255, 0), powerbar)
        
        # farv spilleren efter hvor meget nas de har fået
        nas_farve = self.hentfarve()
        pygame.draw.ellipse(vindue, nas_farve, self.rect)
        
        #  "øjne" så vi ved den retning vi kigger
        spids_x = self.rect.centerx + self.retning * 20
        pygame.draw.line(vindue, (255, 255, 255), self.rect.center, (spids_x, self.rect.centery), 3)

    def hentfarve(self): #skifter farve afhængig af skade
        r, g, b = self.color
        nas_faktor = min(self.skade / 100.0, 1.0)
        return (
            min(255, r + int(nas_faktor * 100)),
            max(0, g - int(nas_faktor * 100)), 
            max(0, b - int(nas_faktor * 100))
        )

    def hentmidt(self):
        # returner midtpunktet (bruges til kollision) i re
        return self.rect.center

    def hentpower(self):
        # returner hvor meget kraft der er i bevægelsen
        return abs(self.fart_x) + abs(self.fart_y)