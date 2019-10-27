#Author by 050chao
#-*- coding:utf-8 -*-
import os,shutil
import wmi
from LogHelper import LogHelper



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
                 tmpdict["DiskTotal"] = int(physical_disk.Size)/1024/1024/1024
                 tmpdict["Caption"] = logical_disk.Caption 
                 tmpdict["Name"] = logical_disk.Name
                 tmpdict["LogicalTotal"] = int(logical_disk.Size)/1024/1024/1024
                 tmpdict["UseSpace"] = (int(logical_disk.Size)-int(logical_disk.FreeSpace))/1024/1024/1024
                 tmpdict["FreeSpace"] = int(logical_disk.FreeSpace)/1024/1024/1024
                 tmpdict["Percent"] = int(100.0*(int(logical_disk.Size)-int(logical_disk.FreeSpace))/int(logical_disk.Size)) 
                 tmpdict["Description"] = logical_disk.Description
                 tmpdict["VolumeName"] = logical_disk.VolumeName
                 tmplist.append(tmpdict) 
     return tmplist

 #获取文件夹下所有的文件，并复制文件到目标地址
 #如果是文件则获取文件的上级目录
def my_copy_file(source_file,target):
    i_file_count = 0
    try:
        str_dir = source_file
        if os.path.isfile(str_dir):
            str_dir = os.path.dirname(str_dir)
        arr_files = get_dir_files(str_dir)
        i_file_count = len(arr_files)
        for name in arr_files:
            copy_file(str_dir,name,target)
        return i_file_count + ",.,"
    except Exception as e:
        LogHelper.error("CopyError1:" + e.message)
        return i_file_count + ",.," + "CopyError1:" + e.message
    

#获取文件夹下所有的文件
def get_dir_files(rootdir):    
    result = []
    if os.path.isdir(rootdir):
        for root,dirs,files in os.walk(rootdir,followlinks=True):
            for name in files:
                result.append(os.path.join(root, name))
           
    elif os.path.isfile(rootdir):
        result.append(rootdir)
    return result

#复制文件到目标地址
def copy_file(source,source_file,target_file):
    try:
        desfilename=source_file.replace('/','\\').replace(source,target_file,1).replace('\\\\','\\')
   
        LogHelper.debug(source_file +  "  copy to   "+desfilename)
        if not os.path.exists(os.path.dirname(desfilename)):
            os.makedirs(os.path.dirname(desfilename))
        if not os.path.exists(desfilename):
            shutil.copy(source_file,desfilename)#如果要改为移动，而不是拷贝，可以将copy改为move
        return "1,.,"
    except Exception as e:
        LogHelper.error("CopyError0:" + e.message)
        return "0,.,CopyError0:" + e.message
    
    