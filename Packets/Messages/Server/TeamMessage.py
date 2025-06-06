from Utils.Writer import Writer
from Files.CsvLogic.Cards import Cards
from Database.DatabaseManager import DataBase
from Files.CsvLogic.Locations import Locations
class TeamMessage(Writer):
    def __init__(self, device, player):
        self.id = 24124
        self.device = device
        self.player = player
        super().__init__(self.device)
    def getMaxPlayersForTeam(self, mapID, type):
        gamemode = Locations().GetGamemode(mapID)
        if gamemode in ("BattleRoyale", "BattleRoyaleTeam"):
            if type==1:
             return 10
            elif gamemode =="BattleRoyale":
                return 1
            return 2
        elif gamemode in ("Survival", "BossFight"):
            return 3
        else:
            if type ==1:
                return 6
            return 3
    def encode(self):
            db = DataBase(self.player)
            gameroomInfo = db.getGameroomInfo("info")
            self.writeVInt(gameroomInfo["room_type"])  # Game Room Type
            self.writeBoolean(gameroomInfo["practice"]) # Practice With Bots
            self.writeVInt(self.getMaxPlayersForTeam(gameroomInfo["map_id"], gameroomInfo["room_type"])) # Game Room Maximun Players
            self.writeLong(0, self.player.teamID)
            self.writeVInt(1) # Unk, is this a timestamp
            self.writeBoolean(gameroomInfo["advertiseToBand"]) # advertise to friends
            self.writeVLong(gameroomInfo["map_slot"][0], gameroomInfo["map_slot"][1])
            self.writeDataReference(15, gameroomInfo["map_id"]) # Location ID
            self.playerCount = gameroomInfo["player_count"]
            self.writeVInt(self.playerCount)
            for player, values in gameroomInfo["players"].items():
                playerToken = db.getTokenByLowId(gameroomInfo["players"][player]["low_id"])
                playersData = (db.getSpecifiedPlayers([playerToken]))[0]
                self.writeBoolean(gameroomInfo["players"][player]["host"]) # is host
                self.writeLong(0, gameroomInfo["players"][player]["low_id"]) # Player ID
                
                self.writeString(gameroomInfo["players"][player]["name"]) # Player Name
                self.writeVInt(69) # Player Experience Level (unused)
                self.writeDataReference(16, gameroomInfo["players"][player]["brawler_id"]) # Player Brawler
                self.writeDataReference(0, 1) # Player Skin
                brawler_id = str(gameroomInfo["players"][player]["brawler_id"])
                self.writeVInt(playersData["unlocked_brawlers"][brawler_id]["Trophies"]) # Brawler Trophies
                self.writeVInt(playersData["unlocked_brawlers"][brawler_id]["HighestTrophies"]) # Brawler Trophies for Rank
                powerLevel = 0
                for card, amount in playersData["unlocked_brawlers"][brawler_id]["Cards"].items():
                    if not Cards().isUnlock(card):
                        powerLevel += amount
                self.writeVInt(powerLevel-1)
                self.writeVInt(gameroomInfo["players"][player]["status"] if playersData["player_status"] != 0 else 0) # Player Status
                self.writeBoolean(gameroomInfo["players"][player]["ready"]) # Ready State
                self.writeVInt(gameroomInfo["players"][player]["team"]) # Player Team
            # Players Array End