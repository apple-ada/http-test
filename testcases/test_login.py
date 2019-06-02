#coding:utf-8
#@time : 2019/4/16 20:18
# @Author : apple
#@file : test_login.py

import unittest
from homework.api_http.common import do_excel,contants,http_request
from ddt import ddt,data
from homework.api_http.common import logger

logger = logger.get_logger(__name__)
@ddt
class LoginTest(unittest.TestCase):
    excel = do_excel.DoExcel(contants.case_file, 'login')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        logger.info('准备测试前置！')
        cls.http_request = http_request.HttpRequest2()

    @data(*cases)
    def test_login(self,case):
        logger.info('开始测试：{0}'.format(case.title))
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
        logger.info('结束测试：{0}'.format(case.title))

    @classmethod
    def tearDownClass(cls):
        logger.info('测试后置处理！')
        cls.http_request.close()
