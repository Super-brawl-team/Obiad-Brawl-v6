
import random
from Files.CsvLogic.Cards import Cards
from Utils.Writer import Writer
from Database.DatabaseManager import DataBase
from datetime import datetime


class LogicGiveDeliveryItemsCommand(Writer):
    def __init__(self, device, player):
        super().__init__(device)
        self.player = player
        self.device = device
    def getBoxID(self, boxID):
       db = DataBase(self.player)
       if boxID == 1:
          if self.player.gold < 100:
                return "no cheating lol"
          self.player.gold -= 100
          db.replaceValue("gold", self.player.gold)
          return 10
       elif boxID == 2:
          if self.player.gems < 10:
                return "no cheating lol"
          self.player.gems -= 10
          db.replaceValue("gems", self.player.gems)
          return 10
       elif boxID == 3:
          if self.player.gems < 80:
                return "no cheating lol"
          self.player.gems -= 80
          db.replaceValue("gems", self.player.gems)
          return 11
       else:
          return boxID
    def rarityByID(self, rarity):
       if rarity == 0:
          return "common"
       elif rarity == 1:
          return "rare"
       elif rarity == 2:
          return "super_rare"
       elif rarity == 3:
          return "epic"
       elif rarity == 4:
          return "mega_epic"
       else:
          return "legendary"
       
    def generateRewardsForBrawlerBox(self, boxID):
       db = DataBase(self.player)
       self.rewards = {}
       self.rewards["boxID"] = boxID
       if boxID == 1:
          if self.player.gems < 30:
                return "no cheating lol"
          self.player.gems -= 30
          db.replaceValue("gems", self.player.gems)
       elif boxID == 2:
          if self.player.gems < 80:
                return "no cheating lol"
          self.player.gems -= 80
          db.replaceValue("gems", self.player.gems)
       elif boxID == 3:
          if self.player.gems < 170:
                return "no cheating lol"
          self.player.gems -= 170
          db.replaceValue("gems", self.player.gems)
       elif boxID == 4:
          if self.player.gems < 350:
                return "no cheating lol"
          self.player.gems -= 350
          db.replaceValue("gems", self.player.gems)
       self.rewards["rewards"] = {}
       for reward in range(1):
          self.rewards["rewards"][reward] = {}
          self.rewards["rewards"][reward]["upgrade"] = 0
          self.rewards["rewards"][reward]["rarity"] = boxID
          print(Cards().getBrawlersWithRarity(self.rarityByID(boxID)))
          selectedCharacters = [char for char in Cards().getBrawlersWithRarity(self.rarityByID(boxID)) if str(Cards().getbrawlerID(char)) not in self.player.unlocked_brawlers]

          selectedCharacter =random.choice(selectedCharacters)
          self.rewards["rewards"][reward]["amount"] = 1
          self.rewards["rewards"][reward]["dataref"] = [16, Cards().getbrawlerID(selectedCharacter)]
          self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
            'Cards': {selectedCharacter: 1},
            'Skins': [0],

            'selectedSkin': 0,
            'Trophies': 0,
            'HighestTrophies': 0,
            'PowerLevel': 0,
            'PowerPoints': 0,
            'State': 0,
            'StarPower': 0
         }
          db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
          print(len(self.player.unlocked_brawlers))
          self.rewards["rewards"][reward]["rewardID"] = 1
       return self.rewards
    def generateRewards(self, boxID):
       db = DataBase(self.player)
       self.rewards = {}
       self.rewards["boxID"] = self.getBoxID(boxID)
       if self.rewards["boxID"] == 11:
          rewardsAmount = 10
       else:
          rewardsAmount = 1
       hasBonus =random.choices([0, 1], weights=[90, 10], k=1)[0]
       self.rewards["rewards"] = {}
       for reward in range(rewardsAmount):
          self.rewards["rewards"][reward] = {}
          self.rewards["rewards"][reward]["upgrade"] = 0
          self.rewards["rewards"][reward]["rarity"] = random.choices([0, 1, 2, 3, 4, 5], weights=[50, 25, 12, 6, 3, 1] , k=1)[0]
          rarityList = ["common", "rare", "super_rare", "epic", "mega_epic", "legendary"]
          brawlersListByRarity = []
          for rarity in rarityList:
             brawlersListByRarity.append([char for char in Cards().getBrawlersWithRarity(rarity) if str(Cards().getbrawlerID(char)) not in self.player.unlocked_brawlers])
          selectedCharacters = brawlersListByRarity[self.rewards["rewards"][reward]["rarity"]]
          if len(selectedCharacters) == 0 and self.rewards["rewards"][reward]["rarity"] == 5:
             self.rewards["rewards"][reward]["rarity"] = 4
          if self.rewards["rewards"][reward]["rarity"] == 0:
             rewardList = ["Brawler", "Upgrades"]
             selectedReward = random.choices(rewardList, weights= [5, 95], k=1)[0]
             if len(self.player.unlocked_brawlers) == 1:
                selectedReward = "Brawler"
             if selectedReward == "Upgrades" or len(selectedCharacters) ==0:
                pins = [100, 101, 102, 200, 201, 202, 300, 301, 302] 
                rewardBrawler = random.choice(list(self.player.unlocked_brawlers.keys()))
                selectedPin = random.choice(pins) + int(rewardBrawler)*1000
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, int(rewardBrawler)]
                self.rewards["rewards"][reward]["rewardID"] = 7
                self.rewards["rewards"][reward]["upgrade"] = selectedPin
                if selectedPin in self.player.playerUpgrades:
                   self.rewards["rewards"][reward]["amount"] = 10
                   self.rewards["rewards"][reward]["rewardID"] = 8
                   self.player.upgradeTokens += 10
                   db.replaceValue("upgradeTokens", self.player.upgradeTokens)
                else:
                  self.player.playerUpgrades.append(selectedPin)
                  db.replaceValue("playerUpgrades", self.player.playerUpgrades)
                  self.player.unlocked_brawlers[rewardBrawler]["PowerLevel"]+=1
                  db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
             else:
                selectedCharacter = random.choice(selectedCharacters)
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, Cards().getbrawlerID(selectedCharacter)]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                   
          elif self.rewards["rewards"][reward]["rarity"] == 1:
             rewardList = ["Brawler", "Upgrades"]
             selectedReward = random.choices(rewardList, weights= [5, 95], k=1)[0]
             if selectedReward == "Upgrades" or len(selectedCharacters) ==0:
                pins = [110, 111, 210, 211, 310, 311]
                rewardBrawler = random.choice(list(self.player.unlocked_brawlers.keys()))
                selectedPin = random.choice(pins) + int(rewardBrawler)*1000
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, int(rewardBrawler)]
                self.rewards["rewards"][reward]["rewardID"] = 7
                self.rewards["rewards"][reward]["upgrade"] = selectedPin
                if selectedPin in self.player.playerUpgrades:
                   self.rewards["rewards"][reward]["amount"] = 20
                   self.rewards["rewards"][reward]["rewardID"] = 8
                   self.player.upgradeTokens += 20
                   db.replaceValue("upgradeTokens", self.player.upgradeTokens)
                else:
                  self.player.playerUpgrades.append(selectedPin)
                  db.replaceValue("playerUpgrades", self.player.playerUpgrades)
                  self.player.unlocked_brawlers[rewardBrawler]["PowerLevel"]+=2
                  db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
             else:
                selectedCharacter = random.choice(selectedCharacters)
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, Cards().getbrawlerID(selectedCharacter)]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter:1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                   
          elif self.rewards["rewards"][reward]["rarity"] == 2:
             rewardList = ["Brawler", "Upgrades", "Doubler", "Booster"]
             selectedReward = random.choices(rewardList, weights= [5, 25, 25, 45], k=1)[0]
             if selectedReward == "Upgrades" or len(selectedCharacters) ==0:
                pins = [120, 220, 320]
                rewardBrawler = random.choice(list(self.player.unlocked_brawlers.keys()))
                selectedPin = random.choice(pins) + int(rewardBrawler)*1000
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, int(rewardBrawler)]
                self.rewards["rewards"][reward]["rewardID"] = 7
                self.rewards["rewards"][reward]["upgrade"] = selectedPin
                if selectedPin in self.player.playerUpgrades:
                   self.rewards["rewards"][reward]["amount"] = 40
                   self.rewards["rewards"][reward]["rewardID"] = 8
                   self.player.upgradeTokens += 40
                   db.replaceValue("upgradeTokens", self.player.upgradeTokens)
                else:
                  self.player.playerUpgrades.append(selectedPin)
                  db.replaceValue("playerUpgrades", self.player.playerUpgrades)
                  self.player.unlocked_brawlers[rewardBrawler]["PowerLevel"]+=3
                  db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
             elif selectedReward == "Doubler":
                self.rewards["rewards"][reward]["amount"] = 200
                self.rewards["rewards"][reward]["dataref"] = [16, 0]
                self.rewards["rewards"][reward]["rewardID"] = 4
                self.player.coinsdoubler += 200
                db.replaceValue("coinsdoubler", self.player.coinsdoubler)
             elif selectedReward == "Booster":
                self.rewards["rewards"][reward]["amount"] = 259200
                self.rewards["rewards"][reward]["dataref"] = [16, 0]
                self.rewards["rewards"][reward]["rewardID"] = 5
                current_booster = self.player.coinsbooster
                if (int(datetime.timestamp(datetime.now())) - current_booster) <= 0:
                    self.player.coinsbooster = int(datetime.timestamp(datetime.now())) + 259200
                    db.replaceValue('coinsbooster', self.player.coinsbooster)
                else:
                    self.player.coinsbooster += 259200
                    db.replaceValue('coinsbooster', self.player.coinsbooster)
             else:
                selectedCharacter = random.choice(selectedCharacters)
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, Cards().getbrawlerID(selectedCharacter)]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
          elif self.rewards["rewards"][reward]["rarity"] == 3:
             rewardList = ["Brawler", "Upgrades"]
             selectedReward = random.choices(rewardList, weights= [5, 95], k=1)[0]
             if selectedReward == "Upgrades" or len(selectedCharacters) ==0:
                pins = [430, 431, 432]
                rewardBrawler = random.choice(list(self.player.unlocked_brawlers.keys()))
                selectedPin = random.choice(pins) + int(rewardBrawler)*1000
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, int(rewardBrawler)]
                self.rewards["rewards"][reward]["rewardID"] = 7
                self.rewards["rewards"][reward]["upgrade"] = selectedPin
                if selectedPin in self.player.playerUpgrades:
                   self.rewards["rewards"][reward]["amount"] = 80
                   self.rewards["rewards"][reward]["rewardID"] = 8
                   self.player.upgradeTokens += 80
                   db.replaceValue("upgradeTokens", self.player.upgradeTokens)
                else:
                  self.player.playerUpgrades.append(selectedPin)
                  db.replaceValue("playerUpgrades", self.player.playerUpgrades)
                  self.player.unlocked_brawlers[rewardBrawler]["PowerLevel"]+=4
                  db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
             else:
                selectedCharacter = random.choice(selectedCharacters)
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, Cards().getbrawlerID(selectedCharacter)]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
          elif self.rewards["rewards"][reward]["rarity"] == 4:
             rewardList = ["Brawler", "Upgrades"]
             selectedReward = random.choices(rewardList, weights= [5, 95], k=1)[0]
             if selectedReward == "Upgrades" or len(selectedCharacters) ==0:
                rewardBrawler = random.choice(list(self.player.unlocked_brawlers.keys()))
                selectedPin = 540 + int(rewardBrawler)*1000
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, int(rewardBrawler)]
                self.rewards["rewards"][reward]["rewardID"] = 7
                self.rewards["rewards"][reward]["upgrade"] = selectedPin
                if selectedPin in self.player.playerUpgrades:
                   self.rewards["rewards"][reward]["amount"] = 160
                   self.rewards["rewards"][reward]["rewardID"] = 8
                   self.player.upgradeTokens += 160
                   db.replaceValue("upgradeTokens", self.player.upgradeTokens)
                else:
                  self.player.playerUpgrades.append(selectedPin)
                  db.replaceValue("playerUpgrades", self.player.playerUpgrades)
                  self.player.unlocked_brawlers[rewardBrawler]["PowerLevel"]+=8
                  db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
             else:
                selectedCharacter = random.choice(selectedCharacters)
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [16, Cards().getbrawlerID(selectedCharacter)]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
          elif self.rewards["rewards"][reward]["rarity"] == 5:
            selectedCharacter = random.choice(selectedCharacters)
            self.rewards["rewards"][reward]["amount"] = 1
            self.rewards["rewards"][reward]["dataref"] = [16, Cards().getbrawlerID(selectedCharacter)]
            if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
               self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
               'Cards': {selectedCharacter: 1},
               'Skins': [0],

               'selectedSkin': 0,
               'Trophies': 0,
               'HighestTrophies': 0,
               'PowerLevel': 0,
               'PowerPoints': 0,
               'State': 0,
               'StarPower': 0
            }
               db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
               self.rewards["rewards"][reward]["rewardID"] = 1
          db.loadAccount()
       if hasBonus:
          reward =  rewardsAmount
          amount = random.choices([0, 1, 2, 3], weights=[50, 25, 19, 6], k=1)[0]
          self.rewards["rewards"][reward] = {}
          self.rewards["rewards"][reward]["rarity"] = amount
          self.rewards["rewards"][reward]["amount"] = amount+1
          self.rewards["rewards"][reward]["dataref"] = [16, 0]
          self.rewards["rewards"][reward]["rewardID"] = 6
          self.rewards["rewards"][reward]["upgrade"] = 0
          self.player.tickets += 1
          db.replaceValue("tickets", self.player.tickets)
       return self.rewards
    def encode(self, rewards):
          self.rewards = rewards
          self.writeVInt(self.rewards["boxID"]) # box id
          self.writeVInt(len(self.rewards["rewards"])) # reward amount
          for reward in self.rewards["rewards"]:
            self.writeVInt(self.rewards["rewards"][reward]["rarity"]) # rarity
            self.writeVInt(self.rewards["rewards"][reward]["amount"]) # amount
            self.writeDataReference(self.rewards["rewards"][reward]["dataref"][0], self.rewards["rewards"][reward]["dataref"][1]) # item type
            self.writeVInt(self.rewards["rewards"][reward]["rewardID"]) # item given
            self.writeVInt(self.rewards["rewards"][reward]["upgrade"]) # skull
            

"""
    def decode(self):
        logicGiveDeliveryItemsPayload = {}
        logicGiveDeliveryItemsPayload["rarityID"] = self.readVInt()
        logicGiveDeliveryItemsPayload["itemTypeID"] = self.readDataReference()
        logicGiveDeliveryItemsPayload["rewardAmount"] = self.readVInt()
        logicGiveDeliveryItemsPayload["itemClassID"] = self.readDataReference()
    def process(self):
        pass
"""
