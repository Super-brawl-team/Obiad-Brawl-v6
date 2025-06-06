from Packets.Messages.Server.TeamMessage import TeamMessage
from Logic.Player import Player
from Utils.Reader import ByteStream
from Database.DatabaseManager import DataBase
from Packets.Messages.Server.AllianceTeamsMessage import AllianceTeamsMessage
class TeamSetLocationMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player


    def decode(self):
        self.requestID = self.readDataReference()

    def process(self):
       db = DataBase(self.player)
       gameroomInfo = db.getGameroomInfo("info")
       gameroomInfo["map_id"] = self.requestID[1]
       db.updateGameroomInfo(gameroomInfo["map_id"], self.player.teamID, "map_id")
       gameroomInfo["room_type"] = 1
       db.updateGameroomInfo(gameroomInfo["room_type"], self.player.teamID, "room_type")
       gameroomInfo["map_slot"] = [0,0]
       db.updateGameroomInfo(gameroomInfo["map_slot"], self.player.teamID, "map_slot")
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
    

