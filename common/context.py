#coding:utf-8
#@time : 2019/4/25 20:27
# @Author : apple
#@file : context.py

import re

from homework.api_http.common.config import config
import configparser

class Context:
    loan_id = None

def replace(data):
    p = "#(.*?)#"  # 正则表达式
    while re.search(p, data):
        # print(data)
        m = re.search(p, data)  # 从任意位置开始找，找第一个就返回Match object, 如果没有找None
        g = m.group(1)  # 拿到参数化的KEY
        try:
            v = config.get('data', g)  # 根据KEY取配置文件里面的值
        except configparser.NoOptionError as e:  # 如果配置文件里面没有的时候，去Context里面取
            if hasattr(Context, g):#如果Context里存在
                v = getattr(Context, g)
            else:#如果Context里不存在
                print('找不到参数化的值')
                raise e
        # 记得替换后的内容，继续用data接收
        data = re.sub(p, v, data, count=1)  # 查找替换,count查找替换的次数

    return data
