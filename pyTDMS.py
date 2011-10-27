from ctypes import *
import os, copy

class TDMSChannel:
    def __init__(self, name, type, values):
        self.name = str(name)
        self.type = type
        self.values = values
    def getData(self):
        return self.values
    def getName(self):
        return self.name
        
class TDMSGroup:
    def __init__(self, name):
        self.name = str(name)
        self.channels = []
        
    def addChannel(self, channel):        
        self.channels.append(channel)
    
    def getChannels(self):
        return self.channels
    
    def getName(self):
        return self.name
        
class TDMSFile:
    def __init__(self, name):
        self.name = name
        self.groups = []
        
    def addGroup(self, group):        
        self.groups.append(group)
        
    def show(self):
        for group in self.groups:
            print "[[ Group " + group.getName() + " ]]"
            for channel in group.getChannels():
                print "[Channel " + channel.getName() + "]" 
                for data in channel.getData():
                    print data
    def getGroups(self):
        return self.groups

class badReturnCode(Exception):
    def __init__(self, value):
        self.value = value
        self.errorCodes = {
            0:"DDC_NoError                                    =     // No error",
            -6201:"DDC_OutOfMemory                                =     // The library could not allocate memory.",
            -6202:"DDC_InvalidArgument                            =     // An invalid argument was passed to the library.",
            -6203:"DDC_InvalidDataType                            =     // An invalid data type was passed to the library.",
            -6204:"DDC_UnexpectedError                            =     // An unexpected error occurred in the library.",
            -6205:"DDC_UsiCouldNotBeLoaded                        =     // The USI engine could not be loaded.",
            -6206:"DDC_InvalidFileHandle                        =     // An invalid file handle was passed to the library.",
            -6207:"DDC_InvalidChannelGroupHandle                =     // An invalid channel group handle was passed to the library.",
            -6208:"DDC_InvalidChannelHandle                    =     // An invalid channel handle was passed to the library.",
            -6209:"DDC_FileDoesNotExist                        =     // The file passed to the library does not exist.",
            -6210:"DDC_CannotWriteToReadOnlyFile                =     // The file passed to the library is read only and cannot be modified.",
            -6211:"DDC_StorageCouldNotBeOpened                    =     // The storage could not be opened.",
            -6212:"DDC_FileAlreadyExists                        =     // The file passed to the library already exists and cannot be created.",
            -6213:"DDC_PropertyDoesNotExist                    =     // The property passed to the library does not exist.",
            -6214:"DDC_PropertyDoesNotContainData                =     // The property passed to the library does not have a value.",
            -6215:"DDC_PropertyIsNotAScalar                    =     // The value of the property passed to the library is an array and not a scalar.",
            -6216:"DDC_DataObjectTypeNotFound                    =     // The object type passed to the library does not exist.",
            -6217:"DDC_NotImplemented                            =     // The current implementation does not support this operation.",
            -6218:"DDC_CouldNotSaveFile                        =     // The file could not be saved.",
            -6219:"DDC_MaximumNumberOfDataValuesExceeded        =     // The request would exceed the maximum number of data values for a channel.",
            -6220:"DDC_InvalidChannelName                        =     // An invalid channel name was passed to the library.",
            -6221:"DDC_DuplicateChannelName                    =     // The channel group already contains a channel with this name.",
            -6222:"DDC_DataTypeNotSupported                    =     // The current implementation does not support this data type.",
            -6224:"DDC_FileAccessDenied                        =     // File access denied.",
            -6225:"DDC_InvalidTimeValue                        =     // The specified time value is invalid.",
            -6226:"DDC_ReplaceNotSupportedForSavedTDMSData        =     // The replace operation is not supported on data that has already been saved to a TDM Streaming file.",
            -6227:"DDC_PropertyDataTypeMismatch                =     // The data type of the property does not match the expected data type.",
            -6228:"DDC_ChannelDataTypeMismatch                    =     // The data type of the channel does not match the expected data type."
        }
        
    def __str__(self):
        return repr(self.errorCodes[self.value])
    
#Checks the return code and make sure it's 0
def c(n):
    if (n!=0):
        raise badReturnCode(n)

def readTMDS(filepath):
    
    tdmsfile = TDMSFile(filepath)
    os.environ['PATH'] = "C:\\Documents and Settings\\pgarcia\\git\\RTU-EMC\\dll" + ";" + os.environ['PATH']
    dll = WinDLL(r"C:\Documents and Settings\pgarcia\git\RTU-EMC\dll\nilibddc.dll")
    
    fileH = c_long(0)
    numGroups = c_uint(0)
    
    c(dll.DDC_OpenFile(filepath, "TDMS", byref(fileH)))
    c(dll.DDC_GetNumChannelGroups(fileH, byref(numGroups)))
    
    groupsType = c_long * numGroups.value
    groups = groupsType()
    
    c(dll.DDC_GetChannelGroups(fileH, byref(groups), numGroups.value))
    length = c_int()
    
    for group in groups:
        c(dll.DDC_GetChannelGroupStringPropertyLength(group, "name", byref(length))) 
        prop = c_char_p(" " * length.value)
        c(dll.DDC_GetChannelGroupProperty (group, "name", prop, length.value+ 1))
        tdmsgroup = TDMSGroup(prop.value)
        numChannels = c_uint(0)
        c(dll.DDC_GetNumChannels(group, byref(numChannels)))
        channelsType = c_long * numChannels.value
        channels = channelsType()
        c(dll.DDC_GetChannels (group, channels, numChannels))
        
        for channel in channels:
            c(dll.DDC_GetChannelStringPropertyLength (channel, "name", byref(length)))
            prop = c_char_p(" " * length.value)
            c(dll.DDC_GetChannelProperty (channel, "name", prop, length.value + 1))
            tdmschannel_name = copy.deepcopy(prop.value)
    #        c(dll.DDC_GetChannelStringPropertyLength (channel, "unit_string", byref(length)))
    #        prop = c_char_p(" " * length.value)
    #        c(dll.DDC_GetChannelProperty (channel, "name", prop, length.value + 1))
    #        print prop.value
            numDataValues = c_ulonglong()
            c(dll.DDC_GetNumDataValues (channel, byref(numDataValues)))
            
            dataType = c_uint()
            c(dll.DDC_GetDataType(channel, byref(dataType)))
            tdmschannel_type = copy.deepcopy(dataType)
             
            dataType = c_char_p * numDataValues.value
            data = dataType()
                        
            c(dll.DDC_GetDataValues(channel, 0, numDataValues.value, data))
            tdmschannel_data = data
            
            tmdschannel = TDMSChannel(tdmschannel_name, tdmschannel_type, tdmschannel_data)
            
            tdmsgroup.addChannel(tmdschannel)
        
        tdmsfile.addGroup(tdmsgroup)
    return tdmsfile