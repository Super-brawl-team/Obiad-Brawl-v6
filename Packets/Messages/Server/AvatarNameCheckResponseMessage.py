# -*- coding: utf-8 -*-
from Utils.Writer import Writer


class AvatarNameCheckResponseMessage(Writer):

    def __init__(self, device, player):
        self.id = 20300
        self.device = device
        self.player = player
        super().__init__(self.device)

    def encode(self):
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeString(self.player.name)
