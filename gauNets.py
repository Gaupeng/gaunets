import subprocess as sp
import os


class gauNetsError(Exception):
    # raised if not posix or nt
    pass


class gn1:

    def __init__(self):
        self.fnull = open(os.devnull, 'w')
        self.system = os.name
        self.privateAddress = ''
        self.subnetMask = ''
        self.defaultGateway = ''
        self.publicAddress = ''
        self.getInformation()

    def cleanNT(self, dPA, dSM, dDG):
        dPA = dPA.stdout.read().decode().splitlines()
        dSM = dSM.stdout.read().decode().splitlines()
        dDG = dDG.stdout.read().decode().splitlines()
        if(dPA):
            self.privateAddress = dPA[0].split(": ")[1]
        else:
            raise gauNetsError("Empty Private Address")
        if(dSM):
            self.subnetMask = dSM[0].split(": ")[1]
        else:
            raise gauNetsError("Empty Subnet Mask")
        if(dDG):
            self.defaultGateway = dDG[0].split(": ")[1]
        else:
            raise gauNetsError("Empty Default Gateway")

    def cleanPOSIX(self, dI):
        print(dI)

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
            dirtyInformation = sp.call("ifconfig | grep -w  inet")
            self.cleanPOSIX(dirtyInformation)
        else:
            raise gauNetsError("Program could not detect your OS Version.")

    def computerInf(self):
        return (self.privateAddress, self.subnetMask, self.defaultGateway)
