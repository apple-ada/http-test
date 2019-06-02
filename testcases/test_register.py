#coding:utf-8
#@time : 2019/4/17 21:15
# @Author : apple
#@file : test_register.py

import unittest
from homework.api_http.common import do_excel,contants,http_request
from ddt import ddt,data
from homework.api_http.common import do_mysql
import random
import string
from homework.api_http.common import logger

logger = logger.get_logger(__name__)
@ddt
class RegisterTest(unittest.TestCase):
    excel = do_excel.DoExcel(contants.case_file, 'register')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        logger.info('准备测试前置！')
        cls.http_request = http_request.HttpRequest2()
        cls.mysql = do_mysql.DoMysql()

    @data(*cases)
    def test_register(self,case):
        logger.info('开始测试：{0}'.format(case.title))

        #参数化方式一：使用动态值进行参数化
        if case.data.find('register_mobile')> -1:
            #self.mysql = do_mysql.DoMysql()
            # #使用手机号最大号码+1获取登录手机号码
            # sql = 'select max(mobilephone) from future.member;'
            # max_phone = self.mysql.fetch_one(sql)[0]
            # max_phone = int(max_phone)+1
            # print("最大手机号码",max_phone)
            # case.data=case.data.replace('register_mobile',str(max_phone))#替换参数值
            #使用随机数生成电话号码
            num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182',
                         '187', '188',
                         '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
            start = random.choice(num_start)
            end = ''.join(random.sample(string.digits, 8))
            random_phone = start + end
            logger.debug('注册号码：{0}'.format(random_phone))

            case.data = case.data.replace('register_mobile', str(random_phone))  # 替换参数值
            #self.mysql.close()#关闭数据库
            # 数据库校验，注册之前查询member表用户个数
            if case.sql is not None:
                sql = case.sql
                member = self.mysql.fetch_one(sql)
                before = member['count(*)']
                logger.debug('注册前用户数：{0}'.format(before))

        resp = self.http_request.request(case.method,case.url,eval(case.data))
        actual = resp.text
        # 断言
        try:
            self.assertEqual((case.expected), actual)
            self.excel.write_result(case.case_id + 1, actual, 'PASS')

        except Exception as e:
            self.excel.write_result(case.case_id + 1, actual, 'FAIL')
            logger.error('断言出错:{0}'.format(e))
            raise e
        #数据库校验
        # 成功之后，判断是否需要执行SQL
        if case.sql is not None:
            sql = case.sql
            member = self.mysql.fetch_one(sql)
            after = member['count(*)']
            logger.debug('注册后用户数：{0}'.format(after))
            self.assertEqual(before + 1, after)
        logger.info('结束测试：{0}'.format(case.title))

    @classmethod
    def tearDownClass(cls):
        logger.info('测试后置处理！')
        cls.mysql.close()
        cls.http_request.close()
