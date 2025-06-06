from Database.DatabaseManager import DataBase
from Logic.UpgradesManager import UpgradesManager
from Utils.Reader import ByteStream

class UpgradeBrawler(ByteStream):
    def __init__(self, device, player, data):
        super().__init__(data)
        self.player = player
        self.device = device
        self.device = device

    def decode(self):
        self.readCommandHeader()
        self.csvID = self.readVInt()
        self.targetBrawler = self.readVInt()
        self.upgradeType = self.readVInt()
        self.upgradeTier = self.readVInt()
        self.upgradeLevel = self.readVInt()
        


    def process(self):
        "this code is from Nostalgic brawl's server, enjoy free leak xd"
        db = DataBase(self.player)
        upgradePrices = [20, 50, 120, 300, 1000]
        purchasedUpgradePrice = upgradePrices[self.upgradeTier]
        self.player.upgradeTokens -= purchasedUpgradePrice
        pins = [100, 101, 102, 200, 201, 202, 300, 301, 302]
        badges = [110, 111, 210, 211, 310, 311]
        medals = [120, 220, 320]
        crests = [430, 431, 432]
        starPower = 540
        db.replaceValue('upgradeTokens', self.player.upgradeTokens)
        brawlerUpgrade = self.targetBrawler*1000 + self.upgradeType*100 + self.upgradeTier*10 + self.upgradeLevel
        baseUpgrade = self.upgradeType*100 + self.upgradeTier*10 + self.upgradeLevel
        if brawlerUpgrade in UpgradesManager.getUpgrades():
           self.player.playerUpgrades.append(brawlerUpgrade)
           db.replaceValue("playerUpgrades", self.player.playerUpgrades)
           if baseUpgrade in pins:
            self.player.unlocked_brawlers[str(self.targetBrawler)]["PowerLevel"] += 1
           elif baseUpgrade in badges:
            self.player.unlocked_brawlers[str(self.targetBrawler)]["PowerLevel"] += 2
           elif baseUpgrade in medals:
            self.player.unlocked_brawlers[str(self.targetBrawler)]["PowerLevel"] += 3
           elif baseUpgrade in crests:
            self.player.unlocked_brawlers[str(self.targetBrawler)]["PowerLevel"] += 4
           elif baseUpgrade == starPower:
            self.player.unlocked_brawlers[str(self.targetBrawler)]["PowerLevel"] += 8
           db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
            
        else:
            return "keki"