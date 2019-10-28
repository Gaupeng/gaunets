import subprocess as sp
import os


class gaunetsError(Exception):
    # raised from gaunets if exception found
    pass


class gaunets:

    def __init__(self):
        self.fnull = open(os.devnull, 'w')
        self.system = os.name
        self.privateAddress = ''
        self.subnetMask = ''
        self.defaultGateway = ''
        self.publicAddress = ''
        self.broadcast = ''
        self.getInformation()

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

    def cleanPOSIX(self, dI):
        dI = dI.stdout.read().decode().splitlines()
        dISplit = dI[0].split()
        if(dI):
            self.privateAddress = dISplit[1]
            self.subnetMask = dISplit[3]
            self.broadcast = dISplit[5]

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
                "ifconfig | grep -w  broadcast", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            self.cleanPOSIX(dirtyInformation)
        else:
            raise gaunetsError("Program could not detect your OS Version.")

    def computerInf(self):
        print("Private IP Address: ", self.privateAddress)
        print("Subnet Mask: ", self.subnetMask)
        print("Default Gateway: ", self.defaultGateway)
        print("Broadcast IP: ", self.broadcast)
        return ("\nProgram run successfully.")
