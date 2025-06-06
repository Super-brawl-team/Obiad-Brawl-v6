from Utils.Writer import Writer
import random
from Database.DatabaseManager import DataBase


class StartLoadingMessage(Writer):
    def __init__(self, device, player):
        self.id = 20559
        self.device = device
        self.player = player
        super().__init__(self.device)


    def encode(self):
        db = DataBase(self.player)
        battleInfo = db.getBattleInfo([self.player.battleID])[0]
        self.writeInt(6) # Game Mode Total Players
        self.writeInt(0)
        self.writeInt(0)


        #Logic Player Array
        self.writeInt(6) # Players Count
        for x in range(1):
             
             self.writeLong(self.player.high_id, self.player.low_id)
             self.writeString(self.player.name) # Player name
             self.writeVInt(x) # Player Team
             self.writeVInt(0) # ???
             self.writeVInt(0) # ??
             self.writeInt(0) # unk
             self.writeDataReference(16, battleInfo["gameObjects"]["csvIDArray"]["1"]["instanceID"]) # Player Brawler
             self.writeDataReference(0) # Player Skin
             self.writeBoolean(0) # has sp ig
        for x in range(2):
             
             self.writeLong(0, random.randint(30, 300)) # friend bot id
             self.writeString("Bot") # Player name
             self.writeVInt(x+1) # Player Team
             self.writeVInt(0) # ???
             self.writeVInt(0) # ???
             self.writeInt(0) # unk
             self.writeDataReference(16, battleInfo["gameObjects"]["csvIDArray"][str(x+2)]["instanceID"]) # Player Brawler
             self.writeDataReference(0, 0) # Player Skin
             self.writeBoolean(0) # has sp ig
        for x in range(3):
             
             self.writeLong(0, random.randint(30, 300)) # enemy bot id
             self.writeString("Bot") # Player name
             self.writeVInt(3+x) # Player Team
             self.writeVInt(1) # ???
             self.writeVInt(0) # ???
             self.writeInt(0) # unk
             self.writeDataReference(16, battleInfo["gameObjects"]["csvIDArray"][str(x+4)]["instanceID"]) # Player Brawler
             self.writeDataReference(0, 0) # Player Skin
             self.writeBoolean(0) # has sp ig
        
        self.writeInt(0) # 
        self.writeInt(0)
        self.writeVInt(1) # unknown
        self.writeVInt(1) # drawmap
        self.writeVInt(2) # control mode
        self.writeBoolean(False) # Is spectating

        self.writeDataReference(15, 26) # Location ID