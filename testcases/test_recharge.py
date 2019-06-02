#coding:utf-8
#@time : 2019/4/17 21:50
# @Author : apple
#@file : test_recharge.py

import unittest
from homework.api_http.common import do_excel,contants,http_request
from homework.api_http.common.do_mysql import DoMysql
from ddt import ddt,data
from homework.api_http.common import context
from homework.api_http.common import logger

logger = logger.get_logger(__name__)
@ddt
class RechargeTest(unittest.TestCase):
    excel = do_excel.DoExcel(contants.case_file, 'recharge')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        logger.info('准备测试前置！')
        cls.http_request = http_request.HttpRequest2()
        cls.mysql = DoMysql()
    # @classmethod
    # def setUp(cls):
    #     cls.mysql = DoMysql()

    @data(*cases)
    def test_recharge(self,case):
        logger.info('开始测试：{0}'.format(case.title))
        # 请求之前，判断是否需要执行SQL
        if case.sql is not None:
            sql = eval(case.sql)['sql1']
            member = self.mysql.fetch_one(sql)
            before = member['leaveamount']
            logger.debug('充值前余额：{0}'.format(before))

        # 在请求之前替换参数化的值
        case.data = context.replace(case.data)
        resp = self.http_request.request(case.method,case.url,eval(case.data))
        print(resp.text)
        actual_code = resp.json()['code']
        # 断言
        try:
            if case.expected:
                self.assertEqual(str(case.expected), actual_code)
            else:
                self.assertEqual(case.expected, actual_code)
            self.excel.write_result(case.case_id + 1, resp.text, 'PASS')

        except Exception as e:
            self.excel.write_result(case.case_id + 1, resp.text, 'FAIL')
            logger.error('断言出错:{0}'.format(e))
            raise e
        # 成功之后，判断是否需要执行SQL
        if case.sql is not None:
            sql = eval(case.sql)['sql1']
            member = self.mysql.fetch_one(sql)
            after = member['leaveamount']
            logger.debug('充值后余额：{0}'.format(after))
            recharge_amount = int(eval(case.data)["amount"])# 充值金额
            logger.debug('充值金额：{0}'.format(recharge_amount))
            #数据库校验
            self.assertEqual(before + recharge_amount, after)
        logger.info('结束测试：{0}'.format(case.title))
    # @classmethod
    # def tearDown(cls):
    #     cls.mysql.close()
    @classmethod
    def tearDownClass(cls):
        logger.info('测试后置处理！')
        cls.mysql.close()
        cls.http_request.close()
