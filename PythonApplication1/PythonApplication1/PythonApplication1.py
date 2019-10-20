#Author by 050chao
#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import os
import sys
import config_configparser
import json
import time
import disk_info
import FileHelper

from os.path import join, getsize
from FileInfo import FileInfo
from RedisHelper import RedisHelper
from LogHelper import LogHelper
from Result_info import Result_info
from command_info import command_info



#def formatTime(longtime):
#    
#    import time
#    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(localtime


#fileinfo = os.stat("mr.png")  
#print("find file ",os.path.abspath("mr.png"))  

#print("file index:",fileinfo.st_ino)
#print(type(fileinfo.st_ino))
#print("file device:",fileinfo.st_dev)
#print("file size:",formatByte(fileinfo.st_size))
#print("file  time:",formatTime(fileinfo.st_atime))
#print("file adit time:",fileinfo.st_mtime)
#print("file create time:",fileinfo.st_ctime)


def search_file_by_str2(rootdir,strs,obj_result,o_redis,str_id):
    for root,dirs,files in os.walk(rootdir):     
        #for i in range(0,len(dirs)):
        #    str_dir_temp = os.path.join(root, dirs[i]) + "\\"
        #    #str_dir_temp = root + dirs[i] + "\\"
        #    search_file_by_str2(str_dir_temp,strs,obj_result,o_redis,str_id)
        
        for i in range(0,len(files)):
            for j in range(0,len(strs)):
                if files[i].endswith(strs[j]):
                    p = FileInfo()
                    p.fileDir = root
                    p.fileRoot = p.fileDir.split('\\')[0]
                    p.fileName = files[i]
                    p.fileFullPath = os.path.join(root,files[i])
                    p.fileExtension = strs[j]
                    fi = os.stat(p.fileFullPath)
                    p.fileIndex = fi.st_ino
                    p.fileSize = int(fi.st_size) /1024/1024/1024
                    p.fileRootID = str_id
                    #封装消息
                    obj_result.code = 1
                    obj_result.msg = json_dict_to_str(p.__dict__)
                    str_result = json_dict_to_str(obj_result.__dict__)
                    redis_public(o_redis,str_result)   
                   

#获取文件夹下的文件和文件夹的大小，(size / 1024 / 1024), 'Mbytes
def get_dir_file_size(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return (size / 1024 / 1024 / 1024)

def get_file_size(fileFullPath):
    size = 0
    fi = os.stat(fileFullPath)
    size = fi.st_size   
    return (size / 1024 / 1024 / 1024)

def json_dict_to_str(dict):
    str_result = ""
    str_result =json.dumps(dict,sort_keys=True,ensure_ascii=False)
    return str_result

def redis_public(o_redis,msg):
    #写入redis并发出消息
    o_redis.public(msg)

print(sys.getdefaultencoding())

#file_m = "D:\\迅雷下载\\BT\\新建文件夹"

#arr_files = disk_info.my_copy_file(file_m,"E:\\")
#print(arr_files)



print('--------------------------------------read config')
#print(config_configparser.config_write())
config = config_configparser.config_read()
print(config)
log_file = (config['DEFAULT']['server action'])

b_loop= True
log = LogHelper(log_file)

# 实例化RedisHelper类对象
str_r_ip=config['redis']['ip2']
str_r_port=config['redis']['port2']
str_r_pwd = config['redis']['pwd2']
str_r_chan = config['redis']['chan1']
str_r_db = config['redis']['db']
str_r_chan2 = config['redis']['chan2']

#打印配置文件
lists_header = config.sections()  
str_config = ""
for secs in lists_header:
    for key in config[secs]:  
        str_config = str_config + " " + key + ":" + config[secs][key]

LogHelper.info(str_config)



obj = RedisHelper(str_r_ip,str_r_pwd,str_r_port,str_r_db,str_r_chan,str_r_chan2)
# 赋值订阅变量
redis_sub = obj.subscribe()

for item in redis_sub.listen():
    LogHelper.info(item)
    if item['type'] == "message":       
        if bytes.decode(item['channel']) == str_r_chan:
            #新建一个新的command_info对象
            obj_msg=command_info()
            #将字典转化为对象
            obj_msg.__dict__=json.loads(item['data'])   
            LogHelper.debug(obj_msg.__dict__)        
            obj_result = Result_info()
            obj_result.type = obj_msg.type 
            if obj_msg.type == 1:       #1、获取所有硬盘基本信息
                obj_result.flag =True        
                tmplist = disk_info.get_fs_info()
                LogHelper.debug(tmplist)  
                obj_result.code = len(tmplist)
                obj_result.msg = json_dict_to_str(tmplist)
                LogHelper.debug(obj_result.msg)  
                str_result = json_dict_to_str(obj_result.__dict__)
                redis_public(obj,str_result)

            elif obj_msg.type == 2:     #2、扫描硬盘
                obj_result.flag =True               
                dirs = obj_msg.msg.split(',.,')       #多个目录扫描，   C:,D:,E:
                args = obj_msg.msg2.split(',')      #多个条件搜索，    .txt,.png
                ids = obj_msg.tag.split(',.,')      #多个盘符的ID，    6,7
                for i in range(0,len(dirs)):
                    search_file_by_str2(dirs[i],args,obj_result,obj,ids[i])

                #for dir in dirs:                    
                #    search_file_by_str2(dir,args,obj_result,obj)                       
            elif obj_msg.type ==3:      #获取文件夹大小
                obj_result.flag =True        
                dirs = obj_msg.msg.split(',.,')       #多个目录扫描，   C:,D:,E:
                if obj_msg.msg2 == "1":   #获取文件夹大小
                    for i in range(0,len(dirs)):
                        obj_result.code += get_dir_file_size(dirs[i])    
                else:
                    for i in range(0,len(dirs)):
                       obj_result.code += get_file_size(dirs[i])           
                obj_result.msg = obj_msg.msg
                str_result = json_dict_to_str(obj_result.__dict__)
                LogHelper.debug(str_result)
                #写入redis并发出消息
                obj.public(str_result.encode("utf-8"))
            elif obj_msg.type == 4:     #拷贝任务，   拷贝文件/目录——》目标硬盘根目录
                obj_result.flag =True        
                dirs = obj_msg.msg.split(',.,')       #多个拷贝任务，   C:,D:,E:
                #obj_msg.msg2   #1 单个文件  2目录   拷贝


            else:
                obj_result.flag =False
                obj_result.code = 0
                obj_result.msg = ""
                LogHelper.info(obj_result.code)
                #写入redis并发出消息
                obj.public(json_dict_to_str(obj_result.__dict__))
            LogHelper.debug("end message")

print('--------------------------------------')


     

'''

disk = disk_info.get_disk_info() 
print(disk )
print('--------------------------------------')
fs = disk_info.get_fs_info() 
print(fs)

json_str = json.dumps(fs,indent=2,sort_keys=True)
print(type(json_str))
print(json_str)
print('--------------------------------------')
str_fileName = config['DEFAULT']['disk_info_save']
if len(str_fileName) > 0:
    #将数据序列化后存储到文件中
    f = open(str_fileName,'wb')   
    f.write(json_str.encode("utf-8"))   #dumps序列化源数据后写入文件
    f.close()
    print('--------------------------------------')
    f = open(str_fileName,'rb')
    da = json.loads(f.read())   #使用loads反序列化
    print(da)
    print('--------------------------------------')


'''


'''
# -*- coding: UTF-8 -*-
import json

#自定义类
class MyClass:
  #初始化
  def __init__(self):
    self.a=2
    self.b='bb'

##########################
#创建MyClass对象
myClass=MyClass()
#添加数据c
myClass.c=123
myClass.a=3
#对象转化为字典
myClassDict = myClass.__dict__
#打印字典
print (myClassDict)
#字典转化为json
myClassJson = json.dumps(myClassDict)
#打印json数据
print (myClassJson)

##########################
#json转化为字典
myClassReBuild = json.loads(myClassJson)
#打印重建的字典
print (myClassReBuild)
#新建一个新的MyClass对象
myClass2=MyClass()
#将字典转化为对象
myClass2.__dict__=myClassReBuild;
#打印重建的对象
print (myClass2.a)

'''