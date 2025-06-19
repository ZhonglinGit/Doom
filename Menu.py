

import pygame
import Constant
import Game

game = Game.Game()
game.main()

def deadMenu(self):
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)

    font = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()

    stuck = True
    while stuck:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        buttonHeight = Constant.HEIGHT / self.options
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
            pygame.quit()
            exit()
        if click[1] and rectsList[1].collidepoint(mouse):
            game.main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(60)
