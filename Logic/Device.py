# -*- coding: utf-8 -*-
import traceback
import json
from Cryptography.rc4 import CryptoRc4
from Packets.Factory import *
from Cryptography.nacl import NaCl

class Device:

    AndroidID = None
    DeviceModel = None
    OpenUDID = None
    OSVersion = None
    IsAndroid = False
    Language = None

    Player = None
    ClientDict = {}

    def __init__(self, socket=None):
        self.socket_crashed = False
        self.socket = socket
        self.crypto = CryptoRc4()
        self.nacl = NaCl()
        self.settings = json.load(open('Settings.json'))
        self.usedCryptography = self.settings["usedCryptography"]

    def SendData(self, ID, data, version=None):
        if self.usedCryptography == "RC4":
         encrypted = self.crypto.encrypt(data)
        elif self.usedCryptography == "NACL":
         encrypted = self.nacl.encrypt(ID, data)
        else:
         encrypted = data
        packetID   = ID.to_bytes(2, 'big')

        if version:
            packetVersion = version.to_bytes(2, 'big')

        else:
            packetVersion = (0).to_bytes(2, 'big')

        if self.socket is None:
            self.transport.write(packetID + len(encrypted).to_bytes(3, 'big') + packetVersion + encrypted)

        else:
            try:
                self.socket.send(packetID + len(encrypted).to_bytes(3, 'big') + packetVersion + encrypted)
            except:
                if not self.socket_crashed:
                    print("Client crashed")
                    self.socket_crashed = True
            
    def SendDataTo(self, ID, data, target, version=None):
        if str(target) in self.ClientDict["Clients"]:
            targetDevice = self.ClientDict["Clients"][str(target)]["Device"]
        else:
            return
        try:
            if self.usedCryptography == "RC4":
                encrypted = targetDevice.crypto.encrypt(data)
            elif self.usedCryptography == "NACL":
                encrypted = targetDevice.nacl.encrypt(ID, data)
            else:
                encrypted = data


            packetID = ID.to_bytes(2, 'big')
            packetLength = len(encrypted).to_bytes(3, 'big')
            packetVersion = (version if version else 0).to_bytes(2, 'big')
            fullPacket = packetID + packetLength + packetVersion + encrypted

            if str(target) not in self.ClientDict["Clients"]:
                return

            PlayerSocket = self.ClientDict["Clients"][str(target)]["SocketInfo"]
            if self.ClientDict["Clients"][str(target)]["SocketInfo"] != None:
                PlayerSocket.send(fullPacket)


        except Exception as e:
            print(f"[ERROR] Failed to send data to {target}: {e}")

    def SendDataUdp(self, ID, data, target, client_address, version=None):
        if self.usedCryptography == "RC4":
            encrypted = self.crypto.encrypt(data)
        elif self.usedCryptography == "NACL":
            encrypted = self.nacl.encrypt(ID, data)
        else:
            encrypted = data

        packetID = ID.to_bytes(2, 'big')
        packetVersion = (version if version else 0).to_bytes(2, 'big')

        # Debug: Check if target exists

        # Get the player's socket
        PlayerSocket = target
        
        try:
            # Send the data
            PlayerSocket.sendto(packetID + len(encrypted).to_bytes(3, 'big') + packetVersion + encrypted, client_address)
        except Exception as e:
            print(f"[ERROR] Failed to send data to {target}: {e}")

    def decrypt(self, data):
        return self.crypto.decrypt(data)

    def processPacket(self, packetID, payload):

        print('[*] {} received'.format(packetID))

        try:
            decrypted = self.decrypt(payload)

            if packetID in availablePackets:

                Message = availablePackets[packetID](decrypted, self)
                Message.decode()
                Message.process()

            else:
                print('[*] {} not handled'.format(packetID))

        except:
            print('[*] Error while decrypting / handling {}'.format(packetID))
            traceback.print_exc()
