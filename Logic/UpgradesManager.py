from Files.CsvLogic.Characters import Characters

class UpgradesManager:
	def getUpgrades(self=None):
		Brawlers = Characters.getBrawlers(self)
        
		upgrades = [100,101,102,110,111,120,200,201,202,210,211,220,300,301,302,310,311,320,430,431,432,540]
		upgradesID = []
		for brawlers in Brawlers:
			for base in upgrades:
				upgradesID.append(base + brawlers * 1000)
		return upgradesID