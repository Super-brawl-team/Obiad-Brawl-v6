from Logic.Player import Player
from Packets.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage
from Database.DatabaseManager import DataBase
from Utils.Reader import ByteStream
from Packets.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand
class LogicGatchaCommand(ByteStream):
    def __init__(self, device, player, data):
        super().__init__(data)
        self.player = player
        self.device = device

    def decode(self):
        self.readCommandHeader()
        self.boxType = self.readVInt() # 1 = coin bocs, 2 = gem smol bocs, 3 = big bocs

    def process(self):
        db = DataBase(self.player)
        self.rewards = LogicGiveDeliveryItemsCommand(self.device, self.player).generateRewards(self.boxType)
        AvailableServerCommandMessage(self.device, self.player, 203, self.rewards).Send()