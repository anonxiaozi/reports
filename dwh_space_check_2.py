# coding=utf-8

import win32com.client as com
# import sys

# sys.path.insert(0, r'C:\Python27\Lib\site-packages\win32')

def TotalSize(drive):
    """ Return the TotalSize of a shared drive [GB]"""
    try:
        fso = com.Dispatch("Scripting.FileSystemObject")
        drv = fso.GetDrive(drive)
        return drv.TotalSize/2**30
    except:
        return 0
 
def FreeSpace(drive):
    """ Return the FreeSpace of a shared drive [GB]"""
    try:
        fso = com.Dispatch("Scripting.FileSystemObject")
        drv = fso.GetDrive(drive)
        return drv.FreeSpace/2**30
    except:
        return 0

def disk_run():
    drive = 'D:'
    result = '%0.2f' % (FreeSpace(drive) * 1000)
    return result

print(disk_run())

