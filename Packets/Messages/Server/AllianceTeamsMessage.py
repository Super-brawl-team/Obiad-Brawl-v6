from Utils.Writer import Writer
from Database.DatabaseManager import DataBase
import time
from Files.CsvLogic.Locations import Locations
from Packets.Messages.Server.TeamMessage import TeamMessage
class AllianceTeamsMessage(Writer):
           def __init__(self, device, player):
               self.id = 24364
               self.device = device
               self.player = player
               super().__init__(self.device)

           def encode(self):
                self.writeBoolean(True) # has at least one team
                db = DataBase(self.player)
                teams=[]
                club = db.loadClub(self.player.club_id)
                for token in club["info"]["memberCount"]:
                    memberData = db.getMemberData(token)
                    if memberData["teamID"]:
                        teams.append(memberData["teamID"])
                self.writeVInt(len(teams)) #count (max 3)
                for x in teams:
                    gameroomInfo = db.getGameroomInfo("info", x)
                    host = 0
                    for player_key, values in gameroomInfo["players"].items():
                            if values["host"]:
                                host = int(player_key)
                    type = gameroomInfo["room_type"]
                    if Locations().GetGamemode(gameroomInfo["map_id"]) in ("Survival", "BossFight"):
                        type = 2
                    self.writeVInt(type) # event type (0: ranked, 1: friendly, 2: ticketed)
                    self.writeBoolean(False) # is in friend list
                    self.writeVInt(len(gameroomInfo["players"])) # current amount of players
                    self.writeVInt(TeamMessage(self.device, self.player).getMaxPlayersForTeam(gameroomInfo["map_id"], gameroomInfo["room_type"])) # max players
                    self.writeLong(0,x) # team id
                    self.writeVInt(gameroomInfo["map_slot"][0] if gameroomInfo["map_slot"][0] >= 0 else 0) # event index1
                    self.writeVInt(gameroomInfo["map_slot"][1] if gameroomInfo["map_slot"][0] >= 0 else 0) # event index2 (mismatch with the index1 doesnt show the selected event and hides the coins left)
                    self.writeDataReference(15,gameroomInfo["map_id"]) # map
                    self.writeVInt(2 if gameroomInfo["advertiseToBand"] else 1) # unk (0: team disapear, 1: appears, 2+: players needed)
                    owner = db.getSpecifiedPlayers([db.getTokenByLowId(host)])[0]
                    self.writeString(owner["name"]) # name of the team owner