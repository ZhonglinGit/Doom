import json
import random
import EnemyMore
import EnemyMore.Devil


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

        return room["map"], self.loadEnemy(room)

    def loadEnemy(self, room):
        enemyList = room["enemy"]
        bigBeautifulList = []
        name = 0
        for i in enemyList:
            if i["Type"] == "Devil":
                print(f"[Debug] enemy x type: {type(i['x'])}, value: {i['x']}")
                eneny = EnemyMore.Devil.Devil(self.screen,
                                                self.player,
                                                room["map"],
                                                name,
                                                i["x"], i["y"] )
            #more enemy

            bigBeautifulList.append(eneny)
        return bigBeautifulList



