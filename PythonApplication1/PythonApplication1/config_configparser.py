#!/usr/bin/python3 
#-*- coding:utf-8 -*-
__author__ = 'chaochao'
__date__ = '2019/9/27'
# config_configparser.py 


import configparser
import re


config_str = '''
[DEFAULT]
version = 1.0.0
server action = logs.txt
disk_info_save=disk_info.txt
scan_info_save=scan_info.txt
scan_filter=.avi,.mp4,.rmvb,.flv
copy_dir = 1

[chao.me]
user = chao

# This is a comments.
[mysql]
ip = 127.0.0.1
port = 3306

# This is a comments.
[redis]
ip2 = 127.0.0.1
port2 = 6380
pwd2 = Chaochao
db=0
chan1 = cc_cmd_py_rec
chan2 = cc_cmd_py_rep
key_disk = disk_info
key_disk_info = disk_info_files
'''

def config_write():
    

    config = configparser.ConfigParser()

    config['DEFAULT'] = {'version': '1.0.0',
                         'server action': 'logs.txt',
                         'disk_info_save': 'disk_info.txt',
                         'scan_info_save': 'scan_info.txt',
                          'scan_filter': '.avi,.mp4,.rmvb,.flv',
                          'copy_dir': '1'}

    config['chao.me'] = {}
    config['chao.me']['user'] = 'chao'

    config['mysql'] = {}
    topsecret = config['mysql']
    topsecret['ip'] = '127.0.0.1'
    topsecret['port'] = '3306'

    config['redis'] = {}
    topsecret = config['redis']
    topsecret['ip2'] = '127.0.0.1'
    topsecret['port2'] = '6380'
    topsecret['pwd2'] = 'Chaochao'
    topsecret['chan1'] = 'cc_cmd_py_rec'
    topsecret['db'] = '0'
    topsecret['chan2'] = 'cc_cmd_py_rep'
    topsecret['key_disk'] = 'disk_info'
    topsecret['key_disk_info'] = 'disk_info_files'


    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def config_read():
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    print("config type:" + str(type(config)))

    lists_header = config.sections()  
    print(lists_header)

    boolean = 'chao.me' in config 
    boolean = config.has_section("chao.me")
    print(boolean)

    user = config['chao.me']['user']
    print(user)
    mysql = config['mysql']
    mysql_ip = mysql['ip']
    mysql_port = mysql['port']
    print(mysql_ip, ":", mysql_port)

    redisstr = config['redis']
    redis_ip = redisstr['ip2']
    redis_port = redisstr['port2']
    redis_pwd = redisstr['pwd2']
    redis_chan1 = redisstr['chan1']
    redis_chan1 = redisstr['chan2']
    redis_db = redisstr['db']
    print(redis_port, ":", redis_pwd)

    for key in config['chao.me']:  
        print(key)

    return config

    ##
    #sec = config.remove_section("chao.me")  
    #config.write(open("config.ini", "w")) 

    ##
    #config.add_section("web.server")
    #config.write(open("config.ini", "w"))

    ##
    #config.set("web.server", "http", "http://chao.me")
    #config.write(open("config.ini", "w"))

    ##
    #config.remove_option("mysql", "ip")
    #config.write(open("config.ini", "w"))


def config_func():
    '''
    写入的值均为字符串
    配合文件的节名称区分大小写, 键不区分大小写(可任意缩进), 注释用'#'和';'(用作整行前缀,可缩进,不推荐行内注释), 值可以跨越多行(要缩进,慎用), 键值分隔符'='和':'
    DEFAULT无法移除,试图删除将引发ValueError, clear()保持原样, popitem()不返回
    '''

    # --- ConfigParser 对象 ---
    # 配置解析器, defaults:DEFAULT字典, dict_type:字典类型(默认:有序字典), allow_no_value:True是否接收不带值的选项(值为None),(默认False), delimiters:键值分隔符, comment_prefixes:整行注释符, inline_comment_prefixes:行内注释符(值之后), strict:是否去重:True(默认), empty_lines_in_values:值是否可以多行;(默认True),False(行标记选项的结尾), default_section:默认节的名称'DEFAULT', interpolation:插值, converters:转换器{类型转换器的名称, 从字符串转换所需数据的类型}{'dicimal': decimal.Decimal}
    # class configparser.ConfigParser(defaults=None, dict_type=collections.OrderedDict, allow_no_value=False, delimiters=('=', ':'), comment_prefixes=('#', ';'), inline_comment_prefixes=None, strict=True, empty_lines_in_values=True, default_section=configparser.DEFAULTSECT, interpolation=BasicInterpolation(), converters={})
    config = configparser.ConfigParser()

    # items(raw=False, vars=None)  # 所有节(含DEFAULT) ItemsView(section_name, section_proxy)(可遍历对象)
    ItemsView = config.items()
    dicts = config.defaults()  # DEFAULT字典
    lists = config.sections()  # 可用的节列表(不含DEFAULT)
    # has_section(section)  # 是否存在该节
    boolean = config.has_section("mysql")
    lists = config.options("mysql")  # 指定节的选项列表(含DEFAULT)
    boolean = config.has_option("mysql", "ip")  # 是否存在指定节的选项

    # read(filenames, encoding=None)  # 尝试读取和解析文件名列表(不存在则忽略), 加载初始值调用read_file()要在read()之前调用
    config.read("config.ini", encoding="utf-8-sig")  # windows下用记事本保存utf8格式要用utf-8-sig编码集
    # read_file(f, source=None)  # 从f读取和解析配置数据, source:文件名
    config.read_file(open('config.ini', encoding="utf-8-sig"))
    # read_string(string, source='<string>')  # 从字符串解析配置数据
    config.read_string(config_str)
    # read_dict(dictionary, source='<dict>')  # 读取字典
    config.read_dict({'section1': {'key1': 'value1',
                                   'key2': 'value2'},
                      'section2': {'key3': 'value3',
                                   'key4': 'value4'}
    })

    # get(section, option, *, raw=False, vars=None[, fallback])  # 获取指定节的选项值, fallback:为找到选项时的返回值
    data_str = config.get("mysql", "ip", fallback=None)
    # getint(section, option, *, raw=False, vars=None[, fallback])  #  获取整数(选项的值强转为整数)
    data_int = config.getint("mysql", "port", fallback=-1)
    # getfloat(section, option, *, raw=False, vars=None[, fallback])
    data = float = config.getfloat("mysql", "port", fallback=-1)
    # getboolean(section, option, *, raw=False, vars=None[, fallback])
    data_bool = config.getboolean("DEFAULT", "server action", fallback=False)  # 获取布尔值,不区分大小写,识别'yes'/'no','on'/'off','true'/'false','1'/'0'

    # write(fileobject, space_around_delimiters=True)  # 将配置写入文件, space_around_delimiters:是否用空格分隔键值之间
    config.write(open("config.ini", "w", encoding="utf-8"))
    # add_section(section)  # 添加节, 节重复DuplicateSectionError, 与默认节重复ValueError, 不是字符串TypeError
    config.add_section("server.luzhuo.me")
    # remove_section(section) # 删除节, 存在True,不存在False
    boolean = config.remove_section("server.luzhuo.me")
    # set(section, option, value)  # 给指定的节设置值, 节不存在NoSectionError, option和value:选项和值为字符串,否则TypeError
    config.set("server.luzhuo.me", "ip", "127.0.0.1")
    # remove_option(section, option)  # 删除选型, 不存在节NoSectionError, 选项存在True,不存在False
    boolean = config.remove_option("server.luzhuo.me", "ip")

    # optionxform(option)  # 子类重写该方法, 或 config.optionxform = str(str区分大小写) 修改, 用于选项名称转为在内部结构中使用的实现

    configparser.MAX_INTERPOLATION_DEPTH  # 使用默认插值时,  当raw=false，get()递归插值的最大深度

    config.clear()  # 所有节都包含'DEFAULT'值,对节的清空不会删除'DEFAULT'值
    config.BOOLEAN_STATES.update({'enabled': True, 'disabled': False})  # 自定义boolean的判断
    config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")  # 自定义节头的编译与解析的正则表达式(去除左右空格)



    # --- 异常 ---
    try: pass
    except configparser.Error: pass  # configparser异常的基类
    except configparser.NoSectionError: pass  # 未找到指定节
    except configparser.DuplicateSectionError: pass  # 节重复
    except configparser.DuplicateOptionError: pass  # 选项重复
    except configparser.NoOptionError: pass  # 未找到指定选项
    except configparser.InterpolationError: pass  # 插值异常的基类
    except configparser.InterpolationDepthError: pass  # 迭代次数超过MAX_INTERPOLATION_DEPTH
    except configparser.InterpolationMissingOptionError: pass  # 选项不存在
    except configparser.InterpolationSyntaxError: pass  # 替换源文本不符合语法
    except configparser.MissingSectionHeaderError: pass  # 没有节头
    except configparser.ParsingError: pass  # 解析文件错误




#if __name__ == "__main__":
#    config_write()
#    config_read()

    # config_func()