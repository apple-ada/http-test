#coding:utf-8
#@time : 2019/4/17 22:28
# @Author : apple
#@file : config.py

import configparser
from homework.api_http.common import contants

class ReadConfig:
    '''完成配置文件的读取'''

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(contants.global_file,encoding='utf-8')  # 先加载global
        switch = self.config.getboolean('switch', 'on')
        if switch:  # 开关打开的时候，使用online的配置
            self.config.read(contants.online_file,encoding='utf-8')
        else:  # 开关关闭的时候，使用test的配置
            self.config.read(contants.test_file,encoding='utf-8')

    def get(self, section, option):
        return self.config.get(section, option)
config = ReadConfig()
if __name__ == '__main__':
    config = ReadConfig()
    print(config.get('switch','on'))
    pre_url = config.get('api', 'pre_url')
    print(pre_url)