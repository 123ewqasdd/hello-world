#Author by 050chao
#-*- coding:utf-8 -*-

import wmi



def get_disk_info(): 
     """ 
     获取物理磁盘信息。 
     """
     tmplist = [] 
     c = wmi.WMI () 
     for physical_disk in c.Win32_DiskDrive (): 
         tmpdict = {} 
         tmpdict["Caption"] = physical_disk.Caption 
         tmpdict["Size"] = int(physical_disk.Size)/1024/1024/1024
         tmpdict["Name"] = physical_disk.Name
         tmplist.append(tmpdict) 
     return tmplist 
def get_fs_info() : 
     """ 
     获取文件系统信息。 
     包含分区的大小、已用量、可用量、使用率、挂载点信息。 
     """
     tmplist = [] 
     c = wmi.WMI () 
     for physical_disk in c.Win32_DiskDrive (): 
         for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"): 
             for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"): 
                 tmpdict = {}
                 tmpdict["disk"] = physical_disk.Caption 
                 tmpdict["Caption"] = logical_disk.Caption 
                 tmpdict["Name"] = logical_disk.Name
                 tmpdict["DiskTotal"] = int(logical_disk.Size)/1024/1024/1024
                 tmpdict["UseSpace"] = (int(logical_disk.Size)-int(logical_disk.FreeSpace))/1024/1024/1024
                 tmpdict["FreeSpace"] = int(logical_disk.FreeSpace)/1024/1024/1024
                 tmpdict["Percent"] = int(100.0*(int(logical_disk.Size)-int(logical_disk.FreeSpace))/int(logical_disk.Size)) 
                 tmpdict["Description"] = logical_disk.Description
                 tmpdict["VolumeName"] = logical_disk.VolumeName
                 tmplist.append(tmpdict) 
     return tmplist
