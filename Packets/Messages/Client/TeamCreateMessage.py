from Packets.Messages.Server.TeamMessage import TeamMessage
from Utils.Reader import ByteStream
from Database.DatabaseManager import DataBase
import time
from Packets.Messages.Server.TeamStreamMessage import TeamStreamMessage
from Packets.Messages.Server.AllianceTeamsMessage import AllianceTeamsMessage

class TeamCreateMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player


    def decode(self):
        self.slot1 = self.readVInt()
        self.slot2 = self.readVInt()
        self.roomType = self.readVInt()
        self.unkBool = self.readBoolean()
    def process(self):
        if self.player.teamID != 0:
            return "nuh uh"
        db = DataBase(self.player)
        db.getRoomId()
        db.replaceValue('teamID', self.player.teamID)
        if self.slot2 > 0:
            eventData = db.loadEvents(1)["info"]["events"][str(self.slot2-1)]
            self.player.map_id = eventData["ID"]
            mapSlot = [self.slot1, self.slot2]
        else:
            self.roomType = 1
            mapSlot = [0,0]
        db.createGameroom(self.roomType, {"info": {"roomID": self.player.teamID, "messages": { "0": {"EventType": 4, "Event": 101, "Tick": 1, "PlayerID": self.player.low_id, "PlayerName": self.player.name, "Message": "", "promotedTeam": 0, "TimeStamp": time.time(), "targetID": self.player.low_id, "targetName": self.player.name}}}})
        gameroomInfo = db.getGameroomInfo("info")
        gameroomInfo["map_slot"] = mapSlot
        db.updateGameroomInfo(gameroomInfo["map_slot"], self.player.teamID, "map_slot")
        TeamMessage(self.device, self.player).Send()
        TeamStreamMessage(self.device, self.player).Send()
        if self.player.club_id == 0:
            return "passed"
        club =  db.loadClub(self.player.club_id)
        self.plrids = []
        for token in club["info"]["memberCount"]:
            memberData = db.getMemberData(token)
            self.plrids.append(memberData["low_id"])
        for id in self.plrids:
                AllianceTeamsMessage(self.device, self.player).Send()