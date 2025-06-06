from Packets.Messages.Server.TeamLeftMessage import TeamLeftMessage
from Utils.Reader import ByteStream
from Logic.Player import Player
from Database.DatabaseManager import DataBase
from Packets.Messages.Server.TeamChatServerMessage import TeamStreamMessage
from Packets.Messages.Server.TeamMessage import TeamMessage
from Packets.Messages.Server.AllianceTeamsMessage import AllianceTeamsMessage
import random
class TeamLeaveMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player


    def decode(self):
        pass
        

    def process(self):
        if self.player.teamID == 0:
            return "kek"
        
        db = DataBase(self.player)
        db.addGameroomMsg(self.player.teamID, 4, self.player.low_id, self.player.name, "", 103, self.player.low_id, self.player.name)
        tick = db.getNextGameroomKey(self.player.teamID)
        db.loadGameroom()
        gameroomInfo = db.getGameroomInfo("info")
        host = 0
        keys = []
        for player_key, values in gameroomInfo["players"].items():
                if values["host"]:
                    host = int(player_key)
                if int(player_key) != self.player.low_id:
                    keys.append(int(player_key))
                TeamStreamMessage(self.device, self.player, tick).SendTo(player_key)
                TeamMessage(self.device, self.player).SendTo(player_key)
        db.removeGameroomPlayer(self.player.low_id, self.player.teamID, self.player.token)
        if host == self.player.low_id and len(keys) != 0:
            newHost = random.choice(keys)
            gameroomInfo["players"][newHost]["host"] = True
            db.updateGameroomPlayerInfo(newHost, self.player.teamID, gameroomInfo["players"][newHost])
        self.player.teamID = 0
        db.replaceValue("teamID", self.player.teamID)
        TeamLeftMessage(self.device, self.player, 0).Send()
        if len(keys) != 0:
            owner = db.getSpecifiedPlayers([db.getTokenByLowId(host)])[0]
        else:
            owner = db.getSpecifiedPlayers([db.getTokenByLowId(self.player.low_id)])[0]
        if owner["club_id"] == 0:
            return "passed"
        club =  db.loadClub(owner["club_id"])
        self.plrids = []
        for token in club["info"]["memberCount"]:
            memberData = db.getMemberData(token)
            self.plrids.append(memberData["low_id"])
        for id in self.plrids:
                AllianceTeamsMessage(self.device, self.player).Send()