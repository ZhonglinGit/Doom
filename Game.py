#zhonglin
#2025 05 23

import pygame
import math
import Player
import Enemy
import RayCasting
import EnemyMore
import Maploader
import Constant
import PerkChoser
import Animation
import cProfile
import pstats

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("picture/Beast_Combat Soundtrack_Horror Boss Fight_Intense Battle Music (OST).mp3")
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1) 

shoot_sound = pygame.mixer.Sound("picture/baga.wav")

screen = pygame.display.set_mode((Constant.WIDTH, Constant.HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

xxx = False
class Game:
    def __init__(self):
        #up date this at new level
        self.map = "xxx"
        self.Player = Player.Player(screen)

        self.Player.shotSound = shoot_sound
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

        # self.map.drawMinimap(screen, self.Player, self.enemyList)

        if not self.mapLoader.nextLevel == "none":
            self.map.drawMinimap(screen, self.Player, self.enemyList)
        self.Player.renderUI()
   
        
    def initGame(self):
        self.animation.fade_in_with_circle(lambda: None)
        self.animation.gameStart()
        self.mapLoader.loadFile()

        self.Player.health = self.Player.Fullhealth
        self.mapLoader.nextLevel = "level_1"
        self.Player.twoGun = False
        self.Player.blinkFrame = False
        self.perkChoser.options = 3
        self.perkChoser.rarePerk = self.perkChoser.rarePerkCopy.copy()

        self.Player.fireGap = 600
        self.Player.damage = 1
        self.Player.energyBarMax = 2000
        self.Player.energyGain = 10
        self.Player.viewDis = 240


        self.newLevel()

    def newLevel(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        #if = [] -> level1
        #then next level
        self.Player.x = 1.5 * Constant.SPACE
        self.Player.y = 1.5 * Constant.SPACE

        self.Player.energy = self.Player.energyBarMax

        # if self.map == "xxx":
        #     self.map, self.enemyList = self.mapLoader.loadRoomEnemy("level_6")
        #     self.Player.map = self.map
        # else:
        self.map, self.enemyList = self.mapLoader.loadRoomEnemy(self.mapLoader.nextLevel)
        self.Player.map = self.map
        if self.mapLoader.nextLevel == "none":
            self.animation.fade_in_with_circle_purple(lambda: self.render())
        else:
            self.animation.fade_in_with_circle(lambda: self.render())
        self.perkChoser.enemyList = self.enemyList
    
    
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
                if self.mapLoader.nextLevel == "none":
                    self.animation.rickThank()
                    
                    self.animation.deadMenu(self.main)

                else:
                    self.animation.fade_out_with_circle()
                    self.perkChoser.perkMenu()
                    self.newLevel()

            if self.Player.health <= 0:
                self.animation.fade_out_with_circle()
                self.animation.gameOver()
                self.animation.deadMenu(self.main)

            
                
            pygame.display.set_caption(str(clock.get_fps()))
            clock.tick(60)

        pygame.quit()
    
if xxx:
    xxxx = cProfile.Profile()
    xxxx.enable()

    game = Game()
    game.main()

    xxxx.disable()
    stats = pstats.Stats(xxxx)
    stats.sort_stats("cuntime")
    stats.print_stats()
else:
    game = Game()
    game.main()