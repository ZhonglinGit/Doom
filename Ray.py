#zhonglin
#2025 05 23

import pygame
import math
import numpy
import sympy
import EnemyMore.Devil
import Player
import Enemy
import RayCasting
import EnemyMore
import Maploader
import Constant
import PerkChoser
import Animation

pygame.init()
screen = pygame.display.set_mode((Constant.WIDTH, Constant.HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        #up date this at new level
        self.map = "xxx"
        self.Player = Player.Player(screen)
        # self.enemy1 = Enemy.Enemy(screen, self.Player,self.map, "xxx")
        # self.enemy2 = EnemyMore.Devil.Devil(screen, self.Player,self.map, 300, 300, "xxx")

        self.enemyList = []

        self.mapLoader = Maploader.Maploader(screen, self.Player)

        self.perkChoser = PerkChoser.PerkChoser(screen, self.Player)

        self.animation = Animation.Animation(screen)

        self.rayCasting = RayCasting.RayCasting(screen)
        self.oldMouse = 0
        self.MouseSensitivity = 0.8
        self.pointer = "xxx"

    def update(self):
        for i in self.enemyList:
            i.update()

        self.Player.inputMove(self.enemyList)

    def render(self):
        self.rayCasting.drawRays(self.Player, self.map)

        for i in self.enemyList:
            i.render(self.rayCasting.depthList)

        self.map.drawMinimap(screen, self.Player, self.enemyList)
        self.Player.renderUI()
   
        
    def initGame(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mapLoader.loadFile()

        # self.enemy1.image = pygame.image.load("Doom\picture\obamaFix.PNG").convert_alpha()
        # self.pointer = pygame.image.load("Doom\picture\point.PNG").convert_alpha()

        self.newLevel()

    def newLevel(self):
        #if = [] -> level1
        #then next level
        self.Player.x = 1.5 * Constant.SPACE
        self.Player.y = 1.5 * Constant.SPACE
        if self.map == "xxx":
            self.map, self.enemyList = self.mapLoader.loadRoomEnemy("level_1")
            self.Player.map = self.map
        else:
            self.map, self.enemyList = self.mapLoader.loadRoomEnemy(self.mapLoader.nextLevel)
            self.Player.map = self.map
        self.animation.fade_in_with_circle(lambda: self.render())
    def main(self):
        self.initGame()
        running = True
        fadeIn = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            self.update()

            # print(self.Player.x / self.map.space, self.Player.y/ self.map.space)
            # print(self.Player.angleL, self.Player.angleR)

            screen.fill((0, 0, 0))
            
            
            self.render()
            pygame.display.flip()
            # scaledPointer = pygame.transform.scale(self.pointer, (500,500))
            # screen.blit(scaledPointer,(Constant.WIDTH // 2, 80))
            
            


            for e in self.enemyList:
                if e.health == 0:
                    self.enemyList.remove(e)
            if self.enemyList == []:
                self.animation.fade_out_with_circle()
                self.perkChoser.perkMenu()
                self.newLevel()

            if self.Player.health <= 0:
                self.animation.gameOver()
                
            
            clock.tick(60)

        pygame.quit()
game = Game()
game.main()    
