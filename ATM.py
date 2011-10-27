from pyTDMS import *
import os, glob

class ATMParameter:
    def __init__(self, groups, n):
        self.name = groups[0].getChannels()[0].getData()[n]
        self.values = []
        for group in groups:
            self.values.append(group.getChannels()[1].getData()[n])
    def getName(self):
        return self.name
    
    def getValues(self):
        return self.values
        
class ATMGroup:
    def __init__(self, groups):
        self.name = groups[0].getChannels()[1].getName()
        self.parameters = []
        n = len(groups[0].getChannels()[0].getData())
        for i in range(0,n):
            self.parameters.append(ATMParameter(groups,i))
    def getParam(self, n):
        return self.parameters[n]

class ATMTest:
    def __init__(self, path):
        self.atmgroups = []
        files = glob.glob(path + "\\*.tdms")
        
        file = files[0]
        tdmsfile = readTMDS(file)
        groups = tdmsfile.getGroups()
        i = 0
        for group in groups:
            mygroups = []
            for file in files:
                tdmsfile = readTMDS(file)
                mygroups.append(tdmsfile.getGroups()[i])
            self.atmgroups.append(ATMGroup(mygroups))
            i += 1
    
    def getParam(self, n):
        return self.atmgroups[1].getParam(n)       
    

tdmsFile = readTMDS("c:\\TEMP\\1.tdms")

test = ATMTest(r"\\thor\GalileoFOC\RTU\EMC\EMC Test Results\RS\RS1GHz-1_7GHz\Hpol_18Vppm\All CH1\ATM")

print(test.getParam(4).getValues())