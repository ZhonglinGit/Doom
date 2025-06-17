
import pygame
import Perk
import Constant
import random

class PerkChoser():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.options = 3

        self.rarePerk = [Perk.Perk("TRIPLE DAMAGE",
                              "damage * 3",
                              lambda player: setattr(player, "damage", player.damage * 3)),
                        Perk.Perk("one more option",
                                "add 1 more perk option",
                                self.addOneOption)
                        
        ]

        self.perkList = [Perk.Perk("Max energy up",
                              "increase max energy by 400",
                              lambda player: setattr(player, "energyBarMax", player.energyBarMax + 400)),
                    Perk.Perk("damage up",
                              "increase damage by 1",
                              lambda player: setattr(player, "damage", player.damage + 1)),
                    Perk.Perk("damage uuuup",
                              "increase damage by 20%",
                              lambda player: setattr(player, "damage", player.damage * 1.2)),
                    Perk.Perk("energy recover up",
                              "enegy recover times 2 ",
                              lambda player: setattr(player, "energyGain", player.energyGain * 2)),
                    Perk.Perk("quick heal",
                              "heal 3 health",
                              lambda player: setattr(player, "health", player.health + 5)),
                    Perk.Perk("see further",
                              "view distance increase by 60",
                              lambda player: setattr(player, "viewDis", player.viewDis + 60))
                    ]
        
    def perkMenu(self):
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

        font = pygame.font.SysFont(None, 32)
        clock = pygame.time.Clock()
        buttonHeight = Constant.HEIGHT / self.options
        buttonWidth = 500
        randomPerk = []

        for i in range(self.options):
            if random.random() < 0.1:
                xxx = random.choice(self.rarePerk)
            else:
                xxx = random.choice(self.perkList)
            randomPerk.append(xxx)

        stuck = True
        while stuck:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            rectsList = []
            for i, perk in enumerate(randomPerk):
                #opotion button
                rect = pygame.Rect(Constant.WIDTH//2 - buttonWidth // 2, 
                                   buttonHeight * 0.1 + i *buttonHeight,
                                   buttonWidth,
                                   buttonHeight * 0.8)
                rectsList.append(rect)

                #high light when hover 
                if perk in self.rarePerk:
                    #gold
                    if rect.collidepoint(mouse):
                        pygame.draw.rect(self.screen, (220, 200, 80), rect)
                    else:
                        pygame.draw.rect(self.screen, (255, 215, 0), rect)
                    
                else:
                    #gray
                    if rect.collidepoint(mouse):
                        pygame.draw.rect(self.screen, (80, 80, 80), rect)
                    else:
                        pygame.draw.rect(self.screen, (50, 50, 50), rect)
                #a white edge
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)

                nameText = font.render(perk.name,True, (255,255,255))
                desText = font.render(perk.text, True, (255,255,255))
                self.screen.blit(nameText,( rect.x + 20, rect.y + buttonHeight /2 - 50))
                self.screen.blit(desText, (rect.x + 20, rect.y + buttonHeight /2 - 10))

                if click[0] and rect.collidepoint(mouse):
                    perk.runable(self.player)
                    print(perk.name)
                    stuck = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()
            clock.tick(60)
    
    def addOneOption(self, _):
        self.options += 1       


