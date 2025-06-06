from Utils.Writer import Writer
from Database.DatabaseManager import DataBase
import json
from Entries.LogicDailyData import LogicDailyData
from Entries.LogicConfData import LogicConfData
class LogicClientHome:
    def encode(self: Writer, player):
        self.player = player
        db = DataBase(self.player)
        LogicDailyData.encode(self, self.player)
        LogicConfData.encode(self, self.player)
        self.writeLong(self.player.high_id, self.player.low_id)  # Player id
        seenNotifs = []
        for key in self.player.homeNotifications:
            notif = self.player.homeNotifications[key]
            if not notif["seen"]:
                seenNotifs.append(key)
        self.writeVInt(len(seenNotifs))
        for key in seenNotifs:
            notif = self.player.homeNotifications[key]
            self.writeVInt(notif["ID"]) # notif id 97 (expired coins booster), 98 (gatcha drop or someshit) or 99 (season end)
            if notif["ID"] == 96:
                self.writeVInt(1)
                self.writeVInt(2)
                self.writeVInt(3)
            if notif["ID"] == 97:
                self.writeVInt(notif["type"])
            elif notif["ID"] == 98:
                self.writeVInt(1) # unk
                self.writeVInt(2) # unk
            elif notif["ID"] == 99:
                # region 1
                self.writeVInt(self.player.unlocked_brawlers[str(notif["bestBrawler"])]["Trophies"]) # total best brawler trophies
                self.writeVInt(notif["bestBrawlerPoints"]) # total season points for the best hero
                self.writeVInt(notif["bestBrawlerCoins"]) # coins gained for the best hero
                self.writeVInt(notif["bestBrawlerBonus"]) # bonus coins gained for the best hero
                # end
                # region 2
                self.writeVInt(self.player.trophies) # total trophies
                self.writeVInt(notif["totalTrophiesPoints"]) # total trophies total points
                self.writeVInt(notif["totalTrophiesCoins"]) # total trophies gained coins
                self.writeVInt(notif["totalTrophiesBonus"]) # total trophies gained bonus
                # end
                self.writeVInt(0) # idk
                self.writeVInt(9000) # idk
                self.writeDataReference(16, notif["bestBrawler"]) # best braler
                self.writeVInt(9000) # idk
                self.writeVInt(0) # idk