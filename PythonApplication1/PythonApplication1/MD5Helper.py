#Author by 050chao
#!/usr/bin/python3 
# -*- coding:utf-8 -*-

from hashlib import md5
import time
import os


def calMD5(str):     #check string的MD5值
    m = md5()
    m.update(str)
    return m.hexdigest()
    
    
    
def calMD5ForFile(file):         #check文件的MD5值
    statinfo = os.stat(file)
    if int(statinfo.st_size)/(1024*1024) >= 1000 :
        print ("File size > 1000, move to big file...")
        return calMD5ForBigFile(file)
    m = md5()
    f = open(file, 'rb')
    m.update(f.read())
    f.close()
    return m.hexdigest()
    
    
    
def calMD5ForFolder(dir,MD5File):     #check文件夹的MD5值
    outfile = open(MD5File,'w')
    for root, subdirs, files in os.walk(dir):
        for file in files:
            filefullpath = os.path.join(root, file)
            """print filefullpath"""
            filerelpath = os.path.relpath(filefullpath, dir)
            md5 = calMD5ForFile(filefullpath)
            print(md5)
            outfile.write(filerelpath+"\t\t******-----------******\t\t"+md5+"\n")
    outfile.close()
    
    
    
def calMD5ForBigFile(file):    #check大文件的MD5值
    m = md5()
    f = open(file, 'rb')
    buffer = 8192    # why is 8192 | 8192 is fast than 2048
    while 1:
        chunk = f.read(buffer)
        if not chunk : break
        m.update(chunk)
    f.close()
    return m.hexdigest()
    
    
    
#checkmd5 = calMD5ForFolder(r'D:\software',r'C:\Users\Desktop\a.txt')
#print(checkmd5)