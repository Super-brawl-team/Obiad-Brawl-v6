from Packets.Messages.Server.TeamMessage import TeamMessage
from Logic.Player import Player
from Utils.Reader import ByteStream
from Database.DatabaseManager import DataBase
from Packets.Messages.Server.TeamErrorMessage import TeamErrorMessage
from Packets.Messages.Server.AllianceTeamsMessage import AllianceTeamsMessage
class TeamSpectateMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player


    def decode(self):
        self.fields = {}
        self.fields["Unk1"] = self.readVInt()
        self.fields["Unk2"] = self.readVInt()
        self.fields["Unk3"] = self.readVInt()

    def process(self):
        if self.player.teamID != 0:
            return "nuh uh"
        db = DataBase(self.player)
        #try:
        joined = db.joinGameroom(self.fields["Unk2"])
        if joined:
            db.connection.commit()
            self.player.teamID = self.fields["Unk2"]
            gameroomInfo = db.getGameroomInfo("info")
            maxPlayers = TeamMessage(self.device, self.player).getMaxPlayersForTeam(gameroomInfo["map_id"], gameroomInfo["room_type"])
            if maxPlayers<=len(gameroomInfo["players"]):
                self.player.teamID = 0
                TeamErrorMessage(self.device, self.player, 2).Send()
            db.replaceValue('teamID', self.player.teamID)
            db.addGameroomMsg(self.player.teamID, 4, self.player.low_id, self.player.name, " ", 102, self.player.low_id, self.player.name)
            for player_key, values in gameroomInfo["players"].items():
                TeamMessage(self.device, self.player).SendTo(player_key)
            owner = db.getSpecifiedPlayers([db.getTokenByLowId(gameroomInfo["players"]["1"]["low_id"])])[0]
            if owner["club_id"] == 0:
                return "passed"
            club =  db.loadClub(owner["club_id"])
            self.plrids = []
            for token in club["info"]["memberCount"]:
                memberData = db.getMemberData(token)
                self.plrids.append(memberData["low_id"])
            for id in self.plrids:
                    AllianceTeamsMessage(self.device, self.player).Send()
            
        else:
            TeamErrorMessage(self.device, self.player, 6).Send()