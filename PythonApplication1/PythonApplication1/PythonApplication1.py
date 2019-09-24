#Author by 050chao
#-*- coding:utf-8 -*-
import os
import sys
import FileInfo



#def formatTime(longtime):
#    #'''��ʽ��ʱ��ĺ���'''
#    import time
#    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(localtime))
#def formatByte(number):
#    #'''��ʽ���ļ���С�ĺ���'''
#    for (scale.label) in [(1024*1024*1024,"GB"),(1024*1024,"MB"),(1024,"KB")]:
#        if number>=scale:
#            return  "%.2f %s" %(number*1.0/scale,lable)
#        elif number ==1:
#            return  r"1�ֽ�"
#        else:#С��1�ֽ�
#            byte = "%.2f" % (number or 0)
#    return (byte[:-3])    #(if byte.endswith(".00") else byte)+"�ֽ�"


#fileinfo = os.stat("mr.png")  #��ȡ�ļ��Ļ�����Ϣ
#print("�ļ�����·����",os.path.abspath("mr.png"))  #��ȡ�ļ�������·��
##����ļ��Ļ�����Ϣ
#print("������:",fileinfo.st_ino)
#print(type(fileinfo.st_ino))
#print("�豸��:",fileinfo.st_dev)
#print("�ļ���С:",formatByte(fileinfo.st_size))
#print("���һ�η���ʱ��:",formatTime(fileinfo.st_atime))
#print("���һ���޸�ʱ��:",fileinfo.st_mtime)
#print("���һ��״̬�仯��ʱ��:",fileinfo.st_ctime)



#����Ŀ¼�����ļ�
def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #�г��ļ��������е�Ŀ¼���ļ�
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i]) #�ϲ�·��
        if os.path.isdir(path):
            _files.extend(list_all_files(path)) #�ݹ���ú���
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
            flag = 1 #�ж��Ƿ��ҵ��ļ�
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
#path = input(r'��������Ҫ�����ĸ�·��(��:D:\\\)')
#print('��������Ҫ���ҵ��ļ�����')
#name = sys.stdin.readline().rstrip() #��׼���룬����restrip()�������ַ�����β�Ŀհ׺ͻس�ɾ��
#answer = search_file(path,name)
#if answer == -1:
#    print('���޴��ļ�')
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
    


##print(os.getcwd())  #����·��

