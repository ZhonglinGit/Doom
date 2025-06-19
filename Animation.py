
import pygame
import Constant
clock = pygame.time.Clock()
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
        
        while radius >= 0:
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
            radius -= 20
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
            radius += 20
        
    def fade_in_with_circle_purple(self, background):
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
            blackSurface.fill((160,60,190, max(0,255 - radius * convergen) ))
            # blackSurface.fill((0,0,0,255 ))
            pygame.draw.circle(blackSurface,(0,0,0,0), center, int(radius))
          
            self.screen.blit(blackSurface,(0,0))

            pygame.display.flip()
            clock.tick(60)
            radius += 10
    def gameOver(self):
        youDied =  pygame.image.load("Doom\picture\dead.PNG").convert_alpha()

        w = youDied.get_width()
        h = youDied.get_height()

        stuck = True
        while stuck:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stuck = False

        

            click = pygame.mouse.get_pressed()
                
            self.screen.blit(youDied,(Constant.WIDTH // 2 - w //2 , Constant.HEIGHT //2 - h //2 ))
            

            if click[0]:
                stuck = False

            pygame.display.flip()

            clock.tick(60)
    def rickThank(self):
        
        self.rick()
        pygame.time.delay(3000)
        self.thank()
        pygame.time.delay(3000)

    def gameStart(self):
        youDied =  pygame.image.load("Doom\picture/title.png").convert_alpha()
        
        xx = pygame.transform.scale(youDied, (Constant.WIDTH, Constant.HEIGHT))

        w = xx.get_width()
        h = xx.get_height()


        stuck = True
        while stuck:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stuck = False

        

            click = pygame.mouse.get_pressed()
                
            # self.screen.blit(youDied,(Constant.WIDTH // 2 - w //2 , Constant.HEIGHT //2 - h //2 ))
            self.screen.blit(xx,(0,0))
            

            if click[0]:
                stuck = False

            pygame.display.flip()

            clock.tick(60)
    def rick(self):
        youDied =  pygame.image.load("Doom\picture/rick.jpg").convert_alpha()
        
        xx = pygame.transform.scale(youDied, (Constant.WIDTH, Constant.HEIGHT))

        w = xx.get_width()
        h = xx.get_height()


        stuck = True
        while stuck:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stuck = False

        

            click = pygame.mouse.get_pressed()
                
            # self.screen.blit(youDied,(Constant.WIDTH // 2 - w //2 , Constant.HEIGHT //2 - h //2 ))
            self.screen.blit(xx,(0,0))
            

            if click[0]:
                stuck = False

            pygame.display.flip()

            clock.tick(60)
    def thank(self):
        youDied =  pygame.image.load("Doom\picture/thank.PNG").convert_alpha()
        
        xx = pygame.transform.scale(youDied, (Constant.WIDTH, Constant.HEIGHT))


        stuck = True
        while stuck:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stuck = False

        

            click = pygame.mouse.get_pressed()
                
            # self.screen.blit(youDied,(Constant.WIDTH // 2 - w //2 , Constant.HEIGHT //2 - h //2 ))
            self.screen.blit(xx,(0,0))
            
            if click[0]:
                stuck = False

            pygame.display.flip()

            clock.tick(60)
        self.screen.fill((0,0,0))
    def deadMenu(self, main):
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

        font = pygame.font.SysFont(None, 32)
        clock = pygame.time.Clock()

        stuck = True
        while stuck:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            buttonHeight = Constant.HEIGHT / 2
            buttonWidth = 500

            rectsList = []
            for i in range(2):
                #opotion button
                rect = pygame.Rect(Constant.WIDTH//2 - buttonWidth // 2, 
                                    buttonHeight * 0.1 + i *buttonHeight,
                                    buttonWidth,
                                    buttonHeight * 0.8)
                rectsList.append(rect)

                #high light when hover 
            
                #gray
                if rect.collidepoint(mouse):
                    pygame.draw.rect(self.screen, (80, 80, 80), rect)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50), rect)
                #a white edge
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)

                if i == 0:
                    replayText = font.render("replay",True, (255,255,255))
                    self.screen.blit(replayText,( rect.x + 20, rect.y + buttonHeight /2 - 50))
                else:
                    quitText = font.render("quit", True, (255,255,255))
                    self.screen.blit(quitText, (rect.x + 20, rect.y + buttonHeight /2 - 10))


            if click[0] and rectsList[0].collidepoint(mouse):
                main()
                
            if click[1] and rectsList[1].collidepoint(mouse):
                pygame.quit()
                exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()
            clock.tick(60)





# pygame.init()
# screen = pygame.display.set_mode((Constant.WIDTH, Constant.HEIGHT), pygame.DOUBLEBUF)
# a = Animation(screen)
# def xxx():
#     pass

# a.fade_in_with_circle_purple(lambda: xxx())
# # a.gameOver