#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import os
import sys
import FileInfo


def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) 
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i]) 
        if os.path.isdir(path):
            _files.extend(list_all_files(path)) 
        if os.path.isfile(path):
            _files.append(path)
    return _files

def search_file_by_str(rootdir,strs):
    _files = []
    for root,dirs,files in os.walk(rootdir):     
        #for i in range(0,len(dirs)):
        #    str_dir_temp = root + dirs[i] + "\\"
        #    _files.extend( search_file_by_str(str_dir_temp,strs))
        
        for i in range(0,len(files)):
            for j in range(0,len(strs)):
                if files[i].endswith(strs[j]):
                    p = FileInfo.FileInfo()
                    p.fileRoot = root
                    p.fileName = files[i]
                    p.fileFullPath = os.path.join(root,files[i])
                    p.fileExtension = strs[j]
                    fi = os.stat(p.fileFullPath)
                    p.fileIndex = fi.st_ino
                    p.fileSize = int(fi.st_size) /1024 /1024 /1024
                    _files.append(p)
    return _files         
           
    


def search_file(path,name):
    for root,dirs,files in os.walk(path):
        if name in dirs or name in files:
            flag = 1 
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root,dirs)
    return -1



'''



#========list_all_files
rootdir = 'E:\OceanTestData'
file = FileHelper.list_all_files(rootdir)

print(len(file))
print(file)



##=======search_file
#path = input(r'input dir(ex:D:\\\)')
#print('...')
#name = sys.stdin.readline().rstrip() #trim
#answer = search_file(path,name)
#if answer == -1:
#    print('not exist')
#else:
#    print(answer)


#==========search_file_by_str
strs = ['.txt','.png']
file =  FileHelper.search_file_by_str(rootdir,strs)

for i in range(0,len(file)):
    print(file[i].fileIndex)
    print(file[i].fileRoot)
    print(file[i].fileName)
    print(file[i].fileExtension)
    print(file[i].fileFullPath)
    print(file[i].fileSize)
    
print('--------------------------------------')

##print(os.getcwd())  #current dir


'''