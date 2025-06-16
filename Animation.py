
import pygame
import Constant

class Animation():
    def __init__(self, screen):
        self.screen = screen

    def fade_out_with_circle(self):
        clock = pygame.time.Clock()
        #circle
        width, height = self.screen.get_size()
        center = (width/2,height/2 )
        radius = max(width, height)
        
        convergen = 200/ radius
        
        while radius > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # self.screen.fill((0,0,255))
            blackSurface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            blackSurface.fill((0,0,0, max(0,200 - radius * convergen)))

            pygame.draw.circle(blackSurface,(0,0,0,0), center, int(radius))
          
            self.screen.blit(blackSurface,(0,0))

            pygame.display.flip()
            clock.tick(60)
            radius -= 10
    def fade_in_with_circle(self, background):
        '''background is render'''
        clock = pygame.time.Clock()
        #circle
        width, height = self.screen.get_size()
        center = (width/2,height/2 )
        radius = 0
        radisMax = max(width, height) /2
        
        convergen = 255/ radisMax
        
        while radius < radisMax:
            background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # self.screen.fill((0,0,255))
            blackSurface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            blackSurface.fill((0,0,0, max(0,255 - radius * convergen) ))
            # blackSurface.fill((0,0,0,255 ))
            pygame.draw.circle(blackSurface,(0,0,0,0), center, int(radius))
          
            self.screen.blit(blackSurface,(0,0))

            pygame.display.flip()
            clock.tick(60)
            radius += 10
    def gameOver(self):
        font = pygame.font.SysFont(None, 32)
        nameText = font.render("GAME OVER",True, (255,255,255))
        self.screen.fill((0,0,0))
        self.screen.blit(nameText,(Constant.WIDTH/2 -100, Constant.HEIGHT/2 - 20))





pygame.init()
screen = pygame.display.set_mode((Constant.WIDTH, Constant.HEIGHT), pygame.DOUBLEBUF)
a = Animation(screen)
def xxx():
    pass

# a.fade_in_with_circle(lambda: xxx())
a.gameOver