# -*- coding: utf-8 -*-
from Packets.Messages.Server.AvatarNameCheckResponseMessage import AvatarNameCheckResponseMessage
from Utils.Reader import ByteStream
from Logic.Player import Player
from Database.DatabaseManager import DataBase

class AvatarNameCheckRequestMessage(ByteStream):

    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player

    def decode(self):
        self.player.name = self.readString()

    def process(self):
        AvatarNameCheckResponseMessage(self.device, self.player).Send()
