# -*- coding: utf-8 -*-
import json

class Player:
    settings = json.load(open("Settings.json"))
    homeNotifications = {}
    high_id = 0
    low_id = 1
    token = None
    usedVersion = 1
    name = "Brawler"
    eventCount = 4
    bestTimeBoss = 0
    bestTimeSurvival = 0
    highest_trophies = 0
    teamID = 0
    playerUpgrades = []
    teamStatus = 0
    tutorialState = settings["startingTutorialState"]
    isReady = False
    selectedCard = [16, 0]
    isTeamInPracticeMode = False
    teamEventIndex = 0
    teamType = 0
    teamStreamMessageCount = 0
    isAdvertiseToBand = False
    matchmakeStartTime = 0
    battleTicks = 0
    club_id = 0
    wifi = 0
    region = "CAT"
    player_status = 3
    last_connection_time = 0
    friends = {}
    room_id = 0
    unlocked_brawlers = {
        0: {'Cards': {"0": 1}, 'Skins': [0], 'selectedSkin': 0, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 0, 'PowerPoints': 0, 'State': 2}}
    player_experience = 0
    profile_icon = 0
    trophies = 0
    solo_wins = 0
    trophieRank = 1
    duo_wins = 0
    ThreeVSThree_wins = 0
    gems = 0
    ticketEventTimestamp = 0
    gold = 92
    battleID = 0
    upgradeTokens = 0
    tickets = 0
    coinsdoubler = 0
    coinsbooster = 0
    coins_reward = 0
    map_id = 7
    skin_id = 0
    brawler_id = 0
    team = 0
    x = 1950
    y = 9750
    control_mode = 0
    has_battle_hints = False
    def __init__(self, device):
        self.device = device

    def encode(self):
        return None
