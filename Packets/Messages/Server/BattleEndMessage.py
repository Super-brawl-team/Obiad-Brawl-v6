# -*- coding: utf-8 -*-
from Utils.Writer import Writer
from Logic.Milestones import Milestones
from Database.DatabaseManager import DataBase
import json
from datetime import datetime
import time
class BattleEndMessage(Writer):
	def __init__(self, device, player, plrs):
		self.id = 23456
		self.device = device
		self.player = player
		self.plrs = plrs
		self.settings = json.load(open('Settings.json'))
		super().__init__(self.device)
  
	def getGamemodeType(self, type):
		if type == "BattleRoyaleTeam" or type == "BattleRoyale":
			return 2
		if type == "Survival":
			return 3
		if type == "BossFight":
			return 4
		else:
			return 1
	def encode(self):
		self.notrophies=False
		def get_trophies(rang, trophies, is_trio):
			if is_trio:
				trophy_ranges = [
					(0, 29, [6, 0, 0]),
					(30, 59, [6, -1, 0]),
					(60, 99, [6, -2, 0]),
					(100, 139, [5, -2, 0]),
					(140, 219, [5, -3, 0]),
					(220, 299, [5, -4, 0]),
					(300, 499, [5, -5, 0]),
					(500, 599, [4, -6, 0]),
					(600, 699, [3, -6, 0]),
					(700, 799, [3, -7, 0]),
					(800, 899, [2, -7, 0]),
					(900, float("inf"), [2, -8, 0]),
				]
				return next((r[rang] for l, h, r in trophy_ranges if l <= trophies <= h), 0)
			if is_event:
				self.plrs["isInRealGame"] = False
				return 0
			else:
				trophy_ranges = [
					(0, 29, [8, 7, 6, 5, 5, 4, 3, 2, 1, 0]),
					(30, 59, [8, 7, 6, 4, 3, 2, 0, -1, -2, -4]),
					(60, 99, [8, 7, 5, 4, 3, 1, 0, -2, -3, -4]),
					(100, 139, [7, 6, 5, 3, 2, 1, -1, -2, -3, -4]),
					(140, 219, [7, 6, 4, 3, 2, 0, -1, -3, -4, -5]),
					(220, 299, [7, 6, 4, 3, 1, 0, -2, -3, -5, -6]),
					(300, 419, [7, 6, 4, 2, 1, -1, -2, -4, -6, -7]),
					(420, 499, [5, 4, 3, 1, 0, -2, -3, -4, -6, -7]),
					(500, 599, [5, 3, 2, 1, -1, -2, -3, -4, -6, -7]),
					(600, 699, [4, 3, 1, 0, -1, -1, -3, -5, -6, -7]),
					(700, 799, [4, 2, 1, -1, -2, -3, -4, -5, -6, -8]),
					(800, 899, [3, 2, 0, -1, -2, -3, -4, -5, -7, -8]),
					(900, float("inf"), [3, 1, -1, -2, -3, -4, -5, -6, -7, -8]),
				]
				return next((r[rang-1] for l, h, r in trophy_ranges if l <= trophies <= h), 0)

		def get_coins(rang, is_trio, is_event):
			if not is_event:
				return [20, 15, 10][rang] if is_trio else [34, 28, 22, 16, 12, 8, 6, 4, 2, 1, 1][rang]
			else:
				duration = int(time.time() - self.player.ticketEventTimestamp) - 5
				if duration <= 19:
					return 12 * self.settings["ticketsPrice"]
				else:
					increase = (duration - 20) // 9 + 1
					return min(12 + increase, 32) * self.settings["ticketsPrice"]

		def get_exp(rang, is_trio, is_event):
			if not is_event:
				return [10, 5, 0][rang] if is_trio else [15, 12, 9, 6, 5, 4, 2, 1, 0, 0, 0][rang]
			else:
				duration = int(time.time() - self.player.ticketEventTimestamp) - 5
				if duration <= 19:
					return 12
				else:
					increase = (duration - 20) // 9 + 1
					return min(12 + increase, 32)


		db = DataBase(self.player)
		is_trio = self.plrs["Gamemode"] not in ("BattleRoyale", "Survival", "BattleRoyaleTeam", "BossFight")
		is_event = self.plrs["Gamemode"] in ("Survival", "BossFight")
		rank = self.plrs["BattleRank"] if not is_trio else self.plrs["BattleEndType"]

		if not self.plrs["isInRealGame"] or self.player.tutorialState < 2:
			trophies = coins = exp = star_exp = doubler = booster = 0
		else:
			brawler_id = str(self.plrs["Brawlers"][0]["CharacterID"][1])
			brawler_data = self.player.unlocked_brawlers[brawler_id]
			trophies = get_trophies(rank, brawler_data["Trophies"], is_trio)
			coins = get_coins(rank, is_trio, is_event)
			exp = get_exp(rank, is_trio, is_event)
			star_exp = 10

			# Coin doubler logic
			doubler = min(coins, self.player.coinsdoubler)
			self.player.coinsdoubler -= doubler
			db.replaceValue("coinsdoubler", self.player.coinsdoubler)

			# Add notification if doubler runs out
			if coins > self.player.coinsdoubler and self.player.coinsdoubler > 0:
				if not any(n["ID"] == 97 and n["type"] == 2 for n in self.player.homeNotifications.values()):
					key = str(len(self.player.homeNotifications))
					self.player.homeNotifications[key] = {"ID": 97, "type": 2, "seen": False}
					db.replaceValue("homeNotifications", self.player.homeNotifications)

			# Booster logic
			booster = coins if self.player.coinsbooster - int(datetime.now().timestamp()) > 0 else 0
		self.writeVInt(self.getGamemodeType(self.plrs["Gamemode"])) # Battle End Game Mode (5 = Showdown. Else is 3vs3)
		self.writeVInt(0) # Related To Coins Gained. If the Value is 1+, "All Coins collected"
		self.writeVInt(coins) # Coins Gained
		self.writeVInt(6969) # "All Coins collected" if 0, its basically coins left
		self.writeVInt(0) # First Win Coins Gained
		self.writeBoolean(False) # "All event experience collected" if True
		self.writeVInt(self.plrs["BattleRank"] if self.plrs["Gamemode"] in ("BattleRoyaleTeam", "BattleRoyale") else self.plrs["BattleEndType"]) # Result (Victory/Defeat/Draw/Rank Score)

		self.writeVInt(trophies) # Trophies Result
		self.writeDataReference(28, self.player.profile_icon)  # Player Profile Icon
		self.writeBoolean(False) # idk
		self.writeBoolean(self.plrs["isInRealGame"]) # is in real game
		self.writeBoolean(self.player.tutorialState < 2) # tutorial
		self.writeVInt(50) # Coin Booster %
		self.writeVInt(booster) # Coin Booster Coins Gained
		self.writeVInt(doubler) # Coin Doubler Coins Gained
		self.writeVInt(int(time.time() - self.player.ticketEventTimestamp)-5) # weekend event time

		# Players Array

		self.writeVInt(self.plrs["PlayersAmount"]) # Battle End Screen Players
		for Players in self.plrs["Brawlers"]:
			self.writeString(Players["Name"]) # Player Name
			self.writeBoolean(Players["IsPlayer"]) # is player
			self.writeBoolean(Players["Team"] is not self.plrs["Brawlers"][0]["Team"]) # is ennemy?
			self.writeBoolean(Players["IsPlayer"]) # is star player
			self.writeDataReference(Players["CharacterID"][0], Players["CharacterID"][1]) # Player Brawler
			self.writeDataReference(Players["SkinID"][0], Players["SkinID"][1]) # Player Brawler Skin!
			self.writeVInt(Players["trophies"]+6974) # Brawler Trophies
			self.writeVInt(Players["powerLevel"]) # Brawler power level
		# Experience Array
		self.writeVInt(2) # Count
		self.writeVInt(0) # Normal Experience ID
		self.writeVInt(exp) # Normal Experience Gained
		self.writeVInt(8) # Star Player Experience ID
		self.writeVInt(star_exp) # Star Player Experience Gained

		# Rank Up and Level Up Bonus Array
		milestonesTrophies = 0
		
		self.maximumRank = self.settings["MaximumRank"]
		Goal0Index = self.maximumRank - 1
		trophiesList = Milestones.ProgressStartTrophies
		for MilestoneIndex in range(Goal0Index):
			if MilestoneIndex >= 34:
				trophiesList.append(trophiesList[33]+50*(MilestoneIndex - 33))
		for x in range(len(trophiesList) - 1):
			if trophiesList[x] <= self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"] < trophiesList[x + 1]:
				if trophiesList[x+1 ] <= self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]+trophies < trophiesList[x + 2]:
					if self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]+trophies < self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"]:
						milestonesTrophies += 1
						self.player.gold += 10
						db.replaceValue("gold", self.player.gold)
				break
		milestonesExp = 0
		expList = Milestones.ProgressStartExp
		for x in range(len(expList) - 1):
			if expList[x] <= self.player.player_experience < expList[x + 1]:
				if expList[x+1 ] <= self.player.player_experience + exp+star_exp < expList[x + 2]:
					milestonesExp += 1
					self.player.gold +=20
					db.replaceValue("gold", self.player.gold)
				break
		milestoneslevel = 0
		selectedIndex = 0
		expList = Milestones.ProgressStart
		for x in range(len(expList) - 1):
			if expList[x] <= self.player.trophies < expList[x + 1]:
				if expList[x+1 ] <= self.player.trophies + trophies < expList[x + 2]:
					if x == self.player.trophieRank+1:
						milestoneslevel += 1
						self.player.trophieRank += 1
						db.replaceValue("trophieRank", self.player.trophieRank)
						selectedIndex = x+1
						self.player.gold += Milestones.PrimaryLvlUpRewardCount[selectedIndex]
						db.replaceValue("gold", self.player.gold)
				break
		self.writeVInt(milestonesExp + milestonesTrophies + milestoneslevel) # Count
		for milestone in range(milestonesExp):
			self.writeVInt(5) 
			self.writeVInt(0) 
			self.writeVInt(0) 
			self.writeVInt(0)
			self.writeVInt(0) 
			self.writeVInt(1) 
			self.writeVInt(12) 
			self.writeVInt(20) 
			self.writeDataReference(5, 1)
			self.writeVInt(0)
		for milestone in range(milestonesTrophies):
			self.writeVInt(1)
			self.writeVInt(0)
			self.writeVInt(0) # Progress Start
			self.writeVInt(0) # Progress
			self.writeVInt(0)
			self.writeVInt(1)
			self.writeVInt(1)
			self.writeVInt(10)
			self.writeDataReference(5,1)
			self.writeVInt(0)
		for milestone in range(milestoneslevel):
			self.writeVInt(6) # Type
			self.writeVInt(0) # Index
			self.writeVInt(0) # Progress Start
			self.writeVInt(0) # Progress
			self.writeVInt(0) # Data Reference
			self.writeVInt(1) # Primary Level Up Reward Count
			for x in range(1):
				self.writeVInt(13) # Primary Level Up Reward Type
				self.writeVInt(Milestones.PrimaryLvlUpRewardCount[selectedIndex]) # Primary Level Up Reward Count
				self.writeDataReference(5, 1) # Primary Level Up Reward Resource
			self.writeVInt(1) # Secondary Level Up Reward Count
			for x in range(1):
				self.writeVInt(13) # Secondary Level Up Reward Type
				self.writeVInt(Milestones.SecondaryLvlUpRewardCount[selectedIndex]) # Secondary Level Up Reward Count
				self.writeDataReference(5, 1) # Secondary Level Up Reward Resource
				self.player.gold += Milestones.SecondaryLvlUpRewardCount[selectedIndex]
				db.replaceValue("gold", self.player.gold)

        


		# Trophies and Experience Bars Array
		self.writeVInt(2) # Count
		self.writeVInt(1) # Trophies Bar Milestone ID
		self.writeVInt(self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]) # Brawler Trophies
		self.writeVInt(self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"]) # Brawler Trophies for Rank
		self.writeVInt(5) # Experience Bar Milestone ID
		self.writeVInt(self.player.player_experience) # Player Experience
		self.writeVInt(self.player.player_experience) # Player Experience for Level

		# Milestones Array
		self.writeBoolean(True) # Bool

		Milestones.MilestonesArray(self)
		self.player.trophies += trophies
		db.replaceValue("trophies", self.player.trophies)
		self.player.trophies_reward = trophies
		db.replaceValue("trophies_reward", self.player.trophies_reward)
		self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"] += trophies
		if self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"] > self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"]:
			self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"] = self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]
		db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
		self.player.player_experience += exp + star_exp
		db.replaceValue("player_experience", self.player.player_experience)
		self.player.gold += coins+booster+doubler
		db.replaceValue("gold", self.player.gold)
		self.player.coins_reward = coins+doubler+booster 
		db.replaceValue("coins_reward", self.player.coins_reward)
		if is_trio:
			self.player.three_vs_three_wins += 1
			db.replaceValue("three_vs_three_wins", self.player.three_vs_three_wins)
		elif self.plrs["Gamemode"] == "Survival":
			timer = int(time.time() - self.player.ticketEventTimestamp)-5
			if timer > self.player.bestTimeSurvival:
				self.player.bestTimeSurvival = timer
				db.replaceValue("bestTimeSurvival", self.player.bestTimeSurvival)
		elif self.plrs["Gamemode"] == "BossFight":
			timer = int(time.time() - self.player.ticketEventTimestamp)-5
			if timer > self.player.bestTimeBoss:
				self.player.bestTimeBoss = timer
			db.replaceValue("bestTimeBoss", self.player.bestTimeBoss)
		else:
			self.player.solo_wins += 1
			db.replaceValue("solo_wins", self.player.solo_wins)
		if self.player.trophies > self.player.highest_trophies:
			self.player.highest_trophies = self.player.trophies
			db.replaceValue("highest_trophies", self.player.highest_trophies)
		if is_event:
			self.player.tickets -= self.settings["ticketsPrice"]