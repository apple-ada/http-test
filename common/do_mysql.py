#coding:utf-8
#@time : 2019/4/19 20:46
# @Author : apple
#@file : do_mysql.py

import pymysql
from homework.api_http.common.config import config

class  DoMysql:
    """
    封装与mysql数据库的一个交互
    """
    def __init__(self):

        host = config.get("database", "host")
        user = config.get("database", "user")
        password = config.get("database", "password")
        port = config.get("database", "port")
        self.mysql = pymysql.connect(host=host, user=user, password=password, port=int(port), charset='utf8')
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)#创建游标（字典格式）

    def fetch_one(self,sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchone()#  返回一条数据，元组格式

    def fetch_all(self,sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchall()#返回所有数据，元组格式，每条数据一个子元组

    def close(self):
        self.cursor.close()#关闭游标
        self.mysql.close()#关闭数据库

if __name__ == '__main__':
    mysql = DoMysql()
    result = mysql.fetch_one('select max(mobilephone) from future.member')
    print(result)


