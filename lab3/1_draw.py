import pygame
from pygame.draw import *
from  random import randint

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 400))

#field
rect(screen, (0, 154, 34), (0, 200, 600, 200), 150)
#sky
rect(screen, (180, 255, 255), (0, 0, 600, 250), 150)
#sun
ellipse(screen, (220, 220, 0), (15, 15, 50, 50))
#clouds
def clouds(x, y, r):
    ellipse(screen, (255, 255, 255), (x, y, r, r))
    ellipse(screen, (0, 0, 0), (x, y, r, r), 1)
    ellipse(screen, (255, 255, 255), (x + 20, y, r, r))
    ellipse(screen, (0, 0, 0), (x + 20, y, r, r), 1)
    ellipse(screen, (255, 255, 255), (x + 40, y, r, r))
    ellipse(screen, (0, 0, 0), (x + 40, y, r, r), 1)
    ellipse(screen, (255, 255, 255), (x + 60, y, r, r))
    ellipse(screen, (0, 0, 0), (x + 60, y, r, r), 1)
    ellipse(screen, (255, 255, 255), (x + 20, y - 20, r, r))
    ellipse(screen, (0, 0, 0), (x + 20, y - 20, r, r), 1)
    ellipse(screen, (255, 255, 255), (x + 40, y - 20, r, r))
    ellipse(screen, (0, 0, 0), (x + 40, y - 20, r, r), 1)
def house(x, y, h, w):
    rect(screen, (170, 120, 0), (x, y, w, h))
    rect(screen, (0, 0, 0), (x, y, w, h), 1)
    polygon(screen, (255, 0, 0), ((x, y), (x + w // 2, y - h // 2), (x + w, y), (x, y)))
    polygon(screen, (0, 0, 0), ((x, y), (x + w // 2, y - h // 2), (x + w, y), (x, y)), 1)
    rect(screen, (0, 150, 200), ((x + w // 2.5), (y + h // 3), h // 3, h // 3))
    rect(screen, (0, 0, 0), ((x + w // 2.5), (y + h // 3), h // 3, h // 3), 1)
def tree(x, y, w, h, r):
    rect(screen, (116, 48, 0), (x, y, w, h))
    x = x + w // 2
    y = y + h // 4
    circle(screen, (0, 102, 0), (x, y - h), r)
    circle(screen, (0, 0, 0), (x, y - h), r, 1)
    circle(screen, (0, 102, 0), (x - w * 2, y - h // 3), r)
    circle(screen, (0, 0, 0), (x - w * 2, y - h // 3),  r, 1)
    circle(screen, (0, 102, 0), (x + w * 2, y - h // 3), r)
    circle(screen, (0, 0, 0), (x + w * 2, y - h // 3), r, 1)
    circle(screen, (0, 102, 0), (x, y - h//2), r)
    circle(screen, (0, 0, 0), (x, y - h//2), r, 1)
    circle(screen, (0, 102, 0), (x - w * 2, y - 2 * h // 3), r)
    circle(screen, (0, 0, 0), (x - w * 2, y - h // 3), r, 1)
    circle(screen, (0, 102, 0), (x + w * 2, y - 2 * h // 3), r)
    circle(screen, (0, 0, 0), (x + w * 2, y - h // 3), r, 1)



clouds(100, 70, 35)
clouds(300, 130, 30)
clouds(500, 90, 40)
house(100, 300, 50, 70)
house(300, 290, 45, 65)
tree(200, 300, 10, 60, 20)
tree(400, 280, 10, 60, 20)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()