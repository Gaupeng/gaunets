import subprocess as sp
import os


class gaunetsError(Exception):
    # raised from gaunets if exception found
    pass


class gaunets:

    def __init__(self):
        self.system = os.name
        self.privateAddress = ''
        self.subnetMask = ''
        self.defaultGateway = ''
        self.publicAddress = ''
        self.broadcast = ''
        self.NeighbourIp = ''
        self.dontExit = 1

        self.getInformation()
        self.getNeighbourInfo()
        self.showMenu()

    def cleanNT(self, dPA, dSM, dDG):
        dPA = dPA.stdout.read().decode().splitlines()
        dSM = dSM.stdout.read().decode().splitlines()
        dDG = dDG.stdout.read().decode().splitlines()
        if(dPA):
            self.privateAddress = dPA[0].split(": ")[1]
        else:
            raise gaunetsError("Empty Private Address")
        if(dSM):
            self.subnetMask = dSM[0].split(": ")[1]
        else:
            raise gaunetsError("Empty Subnet Mask")
        if(dDG):
            self.defaultGateway = dDG[0].split(": ")[1]
        else:
            raise gaunetsError("Empty Default Gateway")

    def cleanPOSIX(self, dI, dN):
        dI = dI.stdout.read().decode().splitlines()
        dISplit = dI[0].split()
        if(dI):
            self.privateAddress = dISplit[1]
            self.subnetMask = dISplit[3]
            self.broadcast = dISplit[5]

        dN = dN.stdout.read().decode()

        if(dN):
            self.defaultGateway = dN.split()[2]

    def getInformation(self):
        if self.system == "nt":
            dirtyPrivateAddress = sp.Popen(
                "ipconfig | findstr IPv4", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            dirtySubnetMask = sp.Popen(
                "ipconfig | findstr Subnet", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            dirtyDefaultGateway = sp.Popen(
                "ipconfig | findstr Default", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            self.cleanNT(dirtyPrivateAddress,
                         dirtySubnetMask, dirtyDefaultGateway)
        elif self.system == "posix":
            dirtyInformation = sp.Popen(
                "ifconfig | grep -w 'broadcast\|Bcast'", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)

            dirtyDefaultGateway = sp.Popen(
                "ip route| grep default", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            self.cleanPOSIX(dirtyInformation, dirtyDefaultGateway)

        else:
            raise gaunetsError("Program could not detect your OS Version.")

    def getNeighbourInfo(self):
        if(self.system) == "posix":
            dirtyNeighbourIp = sp.Popen(
                "ip neigh show", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            dirtyNeighbourIp = dirtyNeighbourIp.stdout.read().decode().splitlines()
            for lines in dirtyNeighbourIp:
                self.NeighbourIp = self.NeighbourIp + lines.split()[0] + " "

    def allInfo(self):
        print("Private IP Address: ", self.privateAddress)
        print("Subnet Mask: ", self.subnetMask)
        print("Default Gateway: ", self.defaultGateway)
        print("Broadcast IP: ", self.broadcast)
        print("Neighbouring IPs: ", self.NeighbourIp)
        return

    def priIP(self):
        print("Private IP Address: ", self.privateAddress)
        return

    def subMask(self):
        print("Subnet Mask: ", self.subnetMask)
        return

    def defGat(self):
        print("Default Gateway: ", self.defaultGateway)
        return

    def broadIP(self):
        print("Broadcast IP: ", self.broadcast)
        return

    def neigh(self):
        print("Neighbouring IPs: ", self.NeighbourIp)
        return

    def exitMenu(self):
        self.dontExit = 0
        print("Exiting program")
        return

    def printMenu(self):
        print("Choose an option from the below, and enter the key: ")
        print("1: Private IP Address")
        print("2: Subnet Mask")
        print("3: Default Gateway")
        print("4: Broadcast IP Address")
        print("5: Neighbor IPs")
        print("6: All Information")
        print("7: Exit")
        return "\n"

    def showMenu(self):
        dictMenu = {
            1: self.priIP,
            2: self.subMask,
            3: self.defGat,
            4: self.broadIP,
            5: self.neigh,
            6: self.allInfo,
            7: self.exitMenu
        }
        while(self.dontExit):
            self.printMenu()
            index = int(input("\nEnter the key: "))
            dictMenu.get(index, lambda: "Invalid index.")()
            print()
        return ("Program run successfully.")
