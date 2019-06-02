#coding:utf-8
#@time : 2019/5/4 21:26
# @Author : apple
#@file : logger.py

import logging

from homework.api_http.common import contants
from homework.api_http.common.config import config


def get_logger(name):
    logger = logging.getLogger(name)
    logger_level = config.get('log','logger_level')
    logger.setLevel(logger_level)

    fmt = "%(asctime)s -  %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d ]"
    formatter = logging.Formatter(fmt=fmt)

    console_handler = logging.StreamHandler()  # 控制台
    # 把日志级别放到配置文件里面配置--优化
    console_handler_level = config.get('log','console_handler_level')
    console_handler.setLevel(console_handler_level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(contants.log_dir + '/case.logs')
    # 把日志级别放到配置文件里面配置
    file_handler_level = config.get('log','file_handler_level')
    file_handler.setLevel(file_handler_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

if __name__ == '__main__':
    logger = get_logger('case')
    logger.info('测试开始啦')
    logger.error('测试报错')
    logger.debug('测试数据')
    logger.info('测试结束')
