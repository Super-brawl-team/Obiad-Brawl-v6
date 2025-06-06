from Packets.Messages.Server.BattleEndMessage import BattleEndMessage
from Files.CsvLogic.Locations import Locations
from Utils.Reader import ByteStream
from Files.CsvLogic.Cards import Cards
from Database.DatabaseManager import DataBase

class AskForBattleEndMessage(ByteStream):

	def __init__(self, data, device, player):
		super().__init__(data)
		self.device = device
		self.data = data
		self.player = player

	def decode(self):
		self.plrs = {}
		self.plrs["BattleEndType"] = self.readVInt() # battle result
		self.plrs["BattleTime"] = self.readVInt() # time played ?

		self.plrs["BattleRank"] = self.readVInt() # rank so basically is won/lose/draw for 3v3 and the rank for sd
		self.plrs["CsvID0"] = self.readVInt() # secndary event index
		self.plrs["Location"] = self.readVInt() # actually its index of event
		self.plrs["PlayersAmount"] = self.readVInt() # Battle End Players
		self.plrs["Brawlers"] = []
		for x in range(self.plrs["PlayersAmount"]):
		# HeroDataEntry::encode
			self.plrs["Brawlers"].append({
				"CharacterID": self.readDataReference(),
				"SkinID": self.readDataReference(),
				"Team": self.readVInt(),
				"IsPlayer": self.readBoolean(), 
				"Name": self.readString(),
				"powerLevel": 0,
				"trophies": 0
			})

		self.plrs["Brawlers"][0]["powerLevel"] = self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["PowerLevel"]
		self.plrs["Brawlers"][0]["trophies"] = self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]
		self.plrs["isInRealGame"] = True
	def process(self):
		db = DataBase(self.player)
		eventsData = db.loadEvents(1)["info"]["events"]
		self.plrs["Gamemode"] = Locations().GetGamemode(eventsData[str(self.plrs["Location"]-1)]["ID"])
		BattleEndMessage(self.device, self.player, self.plrs).Send()