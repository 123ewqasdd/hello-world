#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import redis

class RedisHelper:

    def __init__(self,host_str = "127.0.0.1",pwd='123',port=6379,db=0,chan_sub = "cc_cmd",chan_pub= "rep"):
        # 链接服务端
        pool = redis.ConnectionPool(host=host_str, password = pwd, port=port, db=db)
        self.__conn = redis.Redis(connection_pool=pool)

        # 加入两个频道
        self.chan_sub = chan_sub
        self.chan_pub = chan_pub

    def public(self, msg):
        #发消息订阅方
        # publish发消息加入频道chan_pub
        self.__conn.publish(self.chan_pub, msg)
        return True

    def subscribe(self):
        # 开始订阅pubsub()
        # 打开收音机
        pub = self.__conn.pubsub()

        # 调频道 subscribe
        pub.subscribe(self.chan_sub)

        # 准备接收parse_response()
        # 在次调用parse_response() 开始接收
        pub.parse_response()

        # 返回订阅变量
        return pub


##订阅者
'''
# -*- coding:utf-8 -*-
# 调用shelper
from redis_shelper import RedisHelper

# 实例化RedisHelper类对象
obj = RedisHelper()

# 赋值订阅变量
redis_sub = obj.subscribe()

# 循环执行如下命令
while True:
    # 二次调用parse_response() 开始接收
    msg= redis_sub.parse_response()
    print(msg)
'''


'''
#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
#调用逻辑模块
from redis_shelper import RedisHelper
 
# 实例化对象
obj = RedisHelper()

# 发消息加入频道
obj.public('hello')
'''