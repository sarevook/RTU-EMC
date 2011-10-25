from ctypes import *
import os

os.environ['PATH'] = "C:\\Documents and Settings\\pgarcia\\git\\RTU-EMC\\dll" + ";" + os.environ['PATH']
dll = WinDLL(r"C:\Documents and Settings\pgarcia\git\RTU-EMC\dll\nilibddc.dll")


file = c_long()

print dll.DDC_OpenFile("c:\\TEMP\\1.tdms", "TDMS", byref(file))
print file

numGroups = c_uint(0)
print dll.DDC_GetNumChannelGroups(file, byref(numGroups))
print numGroups

groupsType = c_long * 2

groups = groupsType(0,0)

print dll.DDC_GetChannelGroups(file, byref(groups), 2)

print groups[0]
print groups[1]

gr = c_long(groups[0])

length = c_int()

for group in groups:
    print dll.DDC_GetChannelGroupStringPropertyLength(gr, "name", byref(length)) 
    print length
    prop = c_char_p("HOLA      ")
    print dll.DDC_GetChannelGroupProperty (gr, "name", prop, 11)
    print prop
    
    
    






