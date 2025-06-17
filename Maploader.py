import json
import random
import EnemyMore
import EnemyMore.Devil
import EnemyMore.Ghost
import EnemyMore.PhaseReaper
import Map


class Maploader():
    def __init__(self, screen, player):
        self.file = self.loadFile()
        self.screen = screen
        self.player = player
        #will change later
        self.nextLevel = "level_1"

    def loadFile(self):
        with open("Doom/room.json") as f:           
            return json.load(f)
        
    def loadRoomEnemy(self, level):
        '''need a str like: level_1, return map, enemyList'''
        room = random.choice(self.file[level])
        self.nextLevel = room["nextLevel"]

        map = Map.Map(room["map"])

        return map, self.loadEnemy(room, map)

    def loadEnemy(self, room, map):
        enemyList = room["enemy"]
        bigBeautifulList = []
        name = 0
        for i in enemyList:
            if i["Type"] == "Devil":
                eneny = EnemyMore.Devil.Devil(self.screen,
                                                self.player,
                                                map,
                                                i["x"], i["y"], 
                                                name)
            if i["Type"] == "Ghost":
                eneny = EnemyMore.Ghost.Ghost(self.screen,
                                                self.player,
                                                map,
                                                i["x"], i["y"], 
                                                name)
            if i["Type"] == "PhaseReaper":
                eneny = EnemyMore.PhaseReaper.PhaseReaper(self.screen,
                                                self.player,
                                                map,
                                                i["x"], i["y"], 
                                                name)
            #more enemy

            bigBeautifulList.append(eneny)
        return bigBeautifulList



