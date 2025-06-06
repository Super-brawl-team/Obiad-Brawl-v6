from Utils.Writer import Writer
from Database.DatabaseManager import DataBase
from Logic.Player import Player
from Files.CsvLogic.Characters import Characters
class LogicClientAvatar:
    def encode(self: Writer, player):
        self.player = player
        db = DataBase(self.player)
        ressources_ids = [1, 7]
        ressources = [self.player.gold, self.player.upgradeTokens]
        for id in range(3):
            self.writeLogicLong(self.player.high_id, self.player.low_id) # Player ids related to home menu

        self.writeStringReference(self.player.name)
        self.writeBoolean(self.player.name != "Brawler") # nameSet
        self.writeInt(1) # Player region ?

        # motorised arrays stars 
        self.writeVInt(5) # Commodity Array
        self.writeVInt(len(self.player.unlocked_brawlers) + len(ressources_ids)) # cards and ressources array
        for key, brawler_id in self.player.unlocked_brawlers.items():
            for card, amount in brawler_id["Cards"].items():
                cardID = int(card)
            self.writeDataReference(23, cardID)
            self.writeVInt(1) #unlocked

        # ressources
        for res in range(len(ressources_ids)):
            self.writeDataReference(5, ressources_ids[res]) # resource 
            self.writeVInt(ressources[res]) # count
            
        # cards and ressources Array End

        self.writeVInt(len(self.player.unlocked_brawlers))  # brawlers count
        for key, brawler_id in self.player.unlocked_brawlers.items():
            self.writeDataReference(16, int(key))
            self.writeVInt(brawler_id["Trophies"])

        # Brawlers Trophies for Rank array
        self.writeVInt(len(self.player.unlocked_brawlers))  # brawlers count
        for key, brawler_id in self.player.unlocked_brawlers.items():
            self.writeDataReference(16, int(key))
            self.writeVInt(brawler_id["HighestTrophies"])

        self.writeVInt(0) # highest ressources array (smart supercell)
        # brawler seen state array
        self.writeVInt(len(self.player.unlocked_brawlers))  # brawlers count
        for key, brawler_id in self.player.unlocked_brawlers.items():
            self.writeDataReference(16, int(key))
            self.writeVInt(2)

        self.writeVInt(self.player.gems) # gems
        self.writeVInt(13) # free gems (?) 

        self.writeVInt(0) # experience level (unused)
        self.writeVInt(0) # cumulative purchased gems
        self.writeVInt(0) # battles couns
        self.writeVInt(0) # win count
        self.writeVInt(0) # lose count
        self.writeVInt(0) # win/loose streak (in v1 yeah)
        self.writeVInt(0) # npc win count
        self.writeVInt(0) # npc lose count

        self.writeVInt(self.player.tutorialState) # tutorial state
        
        self.player.coins_reward = 0
        db.replaceValue("coins_reward", self.player.coins_reward)
        self.player.trophies_reward = 0
        db.replaceValue("trophies_reward", self.player.trophies_reward)

