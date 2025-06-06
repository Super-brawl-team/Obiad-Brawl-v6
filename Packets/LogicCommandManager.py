from Packets.Commands.Client.LogicGatchaCommand import LogicGatchaCommand
from Packets.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand
from Packets.Commands.Client.LogicBuyCard import LogicBuyCardCommand
from Packets.Commands.Client.LogicSelectBattleHints import LogicSelectBattleHintsCommand
from Packets.Commands.Client.LogicSelectControlMode import LogicSelectControlModeCommand
from Packets.Commands.Client.LogicSetPlayerThumbnailCommand import LogicSetPlayerThumbnailCommand
from Packets.Commands.Client.LogicBuyBrawlerCommand import LogicBuyBrawlerCommand
from Packets.Commands.Client.LogicBuyCoinsBoosterCommand import LogicBuyCoinsBoosterCommand
from Packets.Commands.Client.LogicBuyCoinsDoublerCommand import LogicBuyCoinsDoublerCommand
from Packets.Commands.Client.LogicUnlockSkinCommand import LogicUnlockSkinCommand
from Packets.Commands.Client.LogicHandleNotificationCommand import LogicHandleNotificationCommand
from Packets.Commands.Client.LogicUpgradeBrawler import UpgradeBrawler
from Packets.Commands.Client.LogicSelectSkinCommand import LogicSelectSkinCommand
commands = {
    #203: LogicGiveDeliveryItemsCommand,
    500: LogicGatchaCommand,
    502: LogicBuyCardCommand,
    505: LogicSetPlayerThumbnailCommand,
    506: LogicSelectSkinCommand,
    507: LogicUnlockSkinCommand,
    508: LogicSelectControlModeCommand,
    509: LogicBuyCoinsDoublerCommand,
    510: LogicBuyCoinsBoosterCommand,
    #512: LogicSelectBattleHintsCommand, scrapped
    513: LogicBuyBrawlerCommand,
    514: LogicHandleNotificationCommand,
    516: UpgradeBrawler
}