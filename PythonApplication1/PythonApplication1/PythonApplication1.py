#Author by 050chao
#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import os
import sys
import FileInfo
import config_configparser
import disk_info
import FileHelper
import json
import time
import pickle
# 调用shelper
from RedisHelper import RedisHelper
from LogHelper import LogHelper



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

lists_header = config.sections()  
str_config = ""
for secs in lists_header:
    for key in config[secs]:  
        str_config = str_config + " " + key + ":" + config[secs][key]

LogHelper.info(str_config)



obj = RedisHelper(str_r_ip,str_r_pwd,str_r_port,str_r_db,str_r_chan)
# 赋值订阅变量
redis_sub = obj.subscribe()


while b_loop:
    msg = redis_sub.parse_response()
    print(msg)
    time.sleep(1)

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