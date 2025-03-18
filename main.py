import pygame
from bane2 import Bane

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sumoslammer")
    clock = pygame.time.Clock()
    run = True
    bane = Bane(WIDTH, HEIGHT)

    while run:
        screen.fill((255, 255, 255))
        bane.draw(screen)
        bane.handle_input()
        bane.update(pygame.time.get_ticks())
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main() 