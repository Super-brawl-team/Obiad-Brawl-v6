from Packets.Messages.Server.TeamMessage import TeamMessage
from Logic.Player import Player
from Utils.Reader import ByteStream
from Database.DatabaseManager import DataBase
from Packets.Messages.Server.AllianceTeamsMessage import AllianceTeamsMessage
class TeamSetRankedLocationMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player


    def decode(self):
        self.requestIndex1 = self.readVInt()
        self.requestIndex2 = self.readVInt()

    def process(self):
       db = DataBase(self.player)
       eventData = db.loadEvents(1)["info"]["events"][str(self.requestIndex2-1)]
       self.requestID = [15, eventData["ID"]]
       gameroomInfo = db.getGameroomInfo("info")
       gameroomInfo["map_id"] = self.requestID[1]
       db.updateGameroomInfo(gameroomInfo["map_id"], self.player.teamID, "map_id")
       gameroomInfo["map_slot"] = [self.requestIndex1, self.requestIndex2]
       db.updateGameroomInfo(gameroomInfo["map_slot"], self.player.teamID, "map_slot")
       gameroomInfo["room_type"] = 0
       db.updateGameroomInfo(gameroomInfo["room_type"], self.player.teamID, "room_type")
       host = 0
       for player_key, values in gameroomInfo["players"].items():
            if values["host"]:
                host = int(player_key)
            TeamMessage(self.device, self.player).SendTo(player_key)
       owner = db.getSpecifiedPlayers([db.getTokenByLowId(host)])[0]
       if owner["club_id"] == 0:
           return "passed"
       club =  db.loadClub(owner["club_id"])
       self.plrids = []
       for token in club["info"]["memberCount"]:
           memberData = db.getMemberData(token)
           self.plrids.append(memberData["low_id"])
       for id in self.plrids:
               AllianceTeamsMessage(self.device, self.player).Send() 
       

