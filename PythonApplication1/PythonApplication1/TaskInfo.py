#!/usr/bin/python3 
# -*- coding:utf-8 -*-

class TaskInfo:    
    id = ''             #任务ID，GUID
    copy_type = ''      #待复制电影类型，以,.,分隔   0 复制目录，1复制当个文件
    arr_source = []     #待复制电影路径，以,.,分隔
    target = ''         #目标路径
    source_size = 0     #源电影总和大小GB
    target_size = 0     #目标目录总大小
    target_free_size = 0#目标目录剩余空间
    count_copy_files =0 #复制目录数量