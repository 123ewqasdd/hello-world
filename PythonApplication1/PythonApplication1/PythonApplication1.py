#Author by 050chao
#-*- coding:utf-8 -*-
import os
import sys
import FileInfo



#def formatTime(longtime):
#    #'''格式化时间的函数'''
#    import time
#    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(localtime))
#def formatByte(number):
#    #'''格式化文件大小的函数'''
#    for (scale.label) in [(1024*1024*1024,"GB"),(1024*1024,"MB"),(1024,"KB")]:
#        if number>=scale:
#            return  "%.2f %s" %(number*1.0/scale,lable)
#        elif number ==1:
#            return  r"1字节"
#        else:#小于1字节
#            byte = "%.2f" % (number or 0)
#    return (byte[:-3])    #(if byte.endswith(".00") else byte)+"字节"


#fileinfo = os.stat("mr.png")  #获取文件的基本信息
#print("文件完整路径：",os.path.abspath("mr.png"))  #获取文件的完整路径
##输出文件的基本信息
#print("索引号:",fileinfo.st_ino)
#print(type(fileinfo.st_ino))
#print("设备名:",fileinfo.st_dev)
#print("文件大小:",formatByte(fileinfo.st_size))
#print("最后一次访问时间:",formatTime(fileinfo.st_atime))
#print("最后一次修改时间:",fileinfo.st_mtime)
#print("最后一次状态变化的时间:",fileinfo.st_ctime)



#根据目录搜索文件
def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i]) #合并路径
        if os.path.isdir(path):
            _files.extend(list_all_files(path)) #递归调用函数
        if os.path.isfile(path):
            _files.append(path)
    return _files

def search_file_by_str(rootdir,strs):
    _files = []
    for root,dirs,files in os.walk(rootdir):
        for i in range(0,len(dirs)):
            _files.extend( search_file_by_str(dirs[i],strs))
        
        for i in range(0,len(files)):
            for j in range(0,len(strs)):
                if files[i].endswith(strs[j]):
                    p = FileInfo.FileInfo()
                    p.fileRoot = rootdir
                    p.fileName = files[i]
                    p.fileFullPath = os.path.join(rootdir,files[i])
                    p.fileExtension = strs[j]
                    fi = os.stat(p.fileFullPath)
                    p.fileIndex = fi.st_ino
                    p.fileSize = fi.st_size
                    _files.append(p)
    return _files         
           
    


def search_file(path,name):
    for root,dirs,files in os.walk(path):
        if name in dirs or name in files:
            flag = 1 #判断是否找到文件
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root,dirs)
    return -1




#========list_all_files
rootdir = 'E:\OceanTestData'
file = list_all_files(rootdir)

print(len(file))
print(file)



##=======search_file
#path = input(r'请输入您要查找哪个路径(如:D:\\\)')
#print('请输入您要查找的文件名：')
#name = sys.stdin.readline().rstrip() #标准输入，其中restrip()函数把字符串结尾的空白和回车删除
#answer = search_file(path,name)
#if answer == -1:
#    print('查无此文件')
#else:
#    print(answer)


#==========search_file_by_str
strs = ['.txt','.png']
file =  search_file_by_str(rootdir,strs)

for i in range(0,len(file)):
    print(file[i].fileIndex)
    print(file[i].fileRoot)
    print(file[i].fileName)
    print(file[i].fileExtension)
    print(file[i].fileFullPath)
    print(file[i].fileSize)
    


##print(os.getcwd())  #运行路径

