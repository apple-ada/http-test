#coding:utf-8
#@time : 2019/4/18 23:03
# @Author : apple
#@file : test_audit.py

import unittest
from homework.api_http.common import do_excel,contants,http_request,context,do_mysql
from ddt import ddt,data
from homework.api_http.common.context import Context
from homework.api_http.common import logger

logger = logger.get_logger(__name__)
@ddt
class AuditTest(unittest.TestCase):
    excel = do_excel.DoExcel(contants.case_file, 'audit')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        logger.info('准备测试前置！')
        cls.http_request = http_request.HttpRequest2()
        cls.mysql = do_mysql.DoMysql()
    @data(*cases)
    def test_audit(self,case):
        logger.info('开始测试：{0}'.format(case.title))
        # 在请求之前替换参数化的值
        case.data = context.replace(case.data)
        resp = self.http_request.request(case.method,case.url,eval(case.data))
        #print(resp.text)
        actual_code = resp.json()['code']
        # 断言
        try:
            if case.expected:
                self.assertEqual(str(case.expected), actual_code)
            else:
                self.assertEqual(case.expected, actual_code)
            self.excel.write_result(case.case_id + 1, resp.text, 'PASS')
            # 判断加标成功之后，查询数据库，取到loan_id
            if resp.json()['msg'] == "加标成功":
                sql = "SELECT id from future.loan WHERE MemberID = 635 ORDER BY CreateTime DESC LIMIT 1"
                loan_id = self.mysql.fetch_one(sql)['id']
                logger.debug('新加的标的ID：{0}'.format( loan_id))
                # 保存到类属性里面
                setattr(Context, "loan_id", str(loan_id))
        except Exception as e:
            self.excel.write_result(case.case_id + 1, resp.text, 'FAIL')
            logger.error('断言出错:{0}'.format(e))
            raise e
        logger.info('结束测试：{}'.format(case.title))
    @classmethod
    def tearDownClass(cls):
        logger.info('测试后置处理！')
        cls.mysql.close()
        cls.http_request.close()