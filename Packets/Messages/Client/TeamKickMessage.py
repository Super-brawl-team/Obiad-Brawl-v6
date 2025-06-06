from Packets.Messages.Server.TeamLeftMessage import TeamLeftMessage
from Utils.Reader import ByteStream
from Logic.Player import Player
from Database.DatabaseManager import DataBase
from Packets.Messages.Server.TeamChatServerMessage import TeamStreamMessage
from Packets.Messages.Server.TeamMessage import TeamMessage
from Packets.Messages.Server.AllianceTeamsMessage import AllianceTeamsMessage
class TeamKickMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player


    def decode(self):
        self.targetID = self.readLogicLong()

    def process(self):
        if self.player.teamID == 0:
            return "kek"
        
        db = DataBase(self.player)
        gameroomInfo = db.getGameroomInfo("info")
        TeamLeftMessage(self.device, self.player, 1).SendTo(self.targetID[1])
        playerToken = db.getTokenByLowId(self.targetID[1])
        db.removeGameroomPlayer(self.targetID[1], self.player.teamID, playerToken)
        db.addGameroomMsg(self.player.teamID, 4, self.player.low_id, self.player.name, "", 104, self.targetID[1], self.player.name)
        tick = db.getNextGameroomKey(self.player.teamID)
        db.loadGameroom()
        host = 0
        for player_key, values in gameroomInfo["players"].items():
                if values["host"]:
                    host = int(player_key)
        for player_key, values in gameroomInfo["players"].items():
            if player_key != self.targetID[1]:
                TeamStreamMessage(self.device, self.player, tick).SendTo(player_key)
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
        if str(self.targetID[1]) in self.device.ClientDict["Clients"]:
            self.device.ClientDict["Clients"][str(self.targetID[1])]["Player"].teamID = 0
        db.replaceOtherValue("teamID", 0, playerToken)
        