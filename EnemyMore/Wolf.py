import Enemy
import pygame
import math
import angles

class Wolf(Enemy.Enemy):
    def __init__(self, screen, player, width, name):
        super().__init__(screen, player, 20, name)
        self.image = pygame.image.load("Doom\picture\WolfPic.jpg")
        self.fullhealth = 5

   


        
    