from Packets.Messages.Server.BattleEndMessage import BattleEndMessage
from Logic.Player import Player
from Utils.Writer import Writer
from Database.DatabaseManager import DataBase
from Files.CsvLogic.Cards import Cards
class ForceSendBattleEnd(Writer):

	def __init__(self, device, player):
		super().__init__(device)
		self.device = device
		self.player = player

	def decode(self):
		db = DataBase(self.player)
		battleInfo = db.getBattleInfo([self.player.battleID])[0]
		self.plrs = {}
		self.plrs["BattleEndType"] = 1 if len(battleInfo["gameObjects"]["gameObjects"]["heroes"]) == 6 else 5 # battle result
		self.plrs["BattleTime"] = 1 # time played ?

		self.plrs["BattleRank"] = 0 # rank so basically is won/lose/draw for 3v3 and the rank for sd
		self.plrs["CsvID0"] = 15
		self.plrs["Location"] = 0 # location or the map if you prefer
		self.plrs["PlayersAmount"] = len(battleInfo["gameObjects"]["gameObjects"]["heroes"]) # Battle End Players
		self.plrs["Brawlers"] = []
		for x, array in battleInfo["gameObjects"]["gameObjects"]["heroes"].items():
		# HeroDataEntry::encode
			powerLevel = 0
			if x== "1":
				team = 1
				isPlayer = True
				for card, amount in self.player.unlocked_brawlers[str(battleInfo["gameObjects"]["csvIDArray"][x]["instanceID"])]["Cards"].items():
					if not Cards().isUnlock(card):
						powerLevel += amount
				Name = self.player.name
			else:
				if x in ["2", "3"]:
					team = 1
				else:
					team = 2

				isPlayer = False
				Name = f"Bot {x}"
			
			self.plrs["Brawlers"].append({
				"CharacterID": [16, battleInfo["gameObjects"]["csvIDArray"][x]["instanceID"]],
				"SkinID": [0, 0],
				"Team": team,
				"IsPlayer": isPlayer, 
				"Name": Name,
				"powerLevel": powerLevel,
    			"trophies": 0
			})
		self.plrs["isInRealGame"] = False
		self.plrs["Gamemode"] = "LaserBall"
	def process(self):
		BattleEndMessage(self.device, self.player, self.plrs).Send()
		