#zhonglin
#2025 05 23

import pygame
import math
import numpy
import sympy
import Player
import Enemy
import RayCasting

pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()


class Map():
    def __init__(self):
        
        self.map = [[1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,1],
                    [1,0,1,0,0,1,0,1],
                    [1,0,0,0,0,0,0,1],
                    [1,0,1,0,0,0,1,1],
                    [1,0,1,0,0,0,1,1],
                    [1,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1]]
        self.space = 60
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.color = (255,0, 0)
    
    def getmap(self):
        return self.map

class Game:
    def __init__(self):
        self.map = Map()
        self.Player = Player.Player(self.map)
        self.enemy1 = Enemy.Enemy(screen, self.Player, 50, "xxx")
        self.rayCasting = RayCasting.RayCasting(screen)
        self.oldMouse = 0
        self.MouseSensitivity = 0.8

    def update(self):
        self.enemy1.update()
        self.Player.inputMove()
        
    def initGame(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.rayCasting.addItem(self.enemy1)
        
        # self.enemy1.midX = self.Player.x + 100 * math.cos(self.Player.angle)
        # self.enemy1.midY = self.Player.y + 100 * math.sin(self.Player.angle)
    def main(self):
        self.initGame()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                

            self.update()

            # print(self.Player.x / self.map.space, self.Player.y/ self.map.space)
            # print(self.Player.angleL, self.Player.angleR)

            screen.fill((0, 0, 0))
            
            self.rayCasting.drawRays(self.Player, self.map)
            self.enemy1.render()
            self.oldMouse = pygame.mouse.get_pos()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
game = Game()
game.main()    
