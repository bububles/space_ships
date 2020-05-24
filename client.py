import pygame
import time
from network import Network
from player import Player

pygame.init()

win = pygame.display.set_mode((400, 400))
pygame.display.set_caption("///")

color1 = (255, 255, 0)
color2 = (0, 225, 255)

background = pygame.image.load("background.png")
ship1 = pygame.image.load("ship1.png")
ship2 = pygame.image.load("ship2.png")
won = pygame.image.load("won.png")
lost = pygame.image.load("lost.png")
waiting = pygame.image.load("waiting.png")


def redrawWindow(win, player1, player2, add):
    win.blit(background, (0, 0))
    draw(player1, win)
    draw(player2, win)
    if add is not None:
        win.blit(add, (0, 0))
    pygame.display.update()


def draw(player, win):
    if player.color == color1:
        img = pygame.image.load("ship1.png")
    else:
        img = pygame.image.load("ship2.png")
    win.blit(img, (player.x, player.y))
    player.healthbar(win)
    for laser in player.lasers:
        laser.draw(win)

def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("quit")
                pygame.quit()
        add = None
        end = False
        if p.alive & (not p2.alive):
            add = waiting
        if p.health == 0:
            add = lost
            end = True
        if p2.health == 0:
            add = won
            end = True
        if p.health > 0:
            p.move(p2)
        redrawWindow(win, p, p2, add)
        if end:
            time.sleep(3)
            run = False
            pygame.quit()


main()
