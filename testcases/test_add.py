#coding:utf-8
#@time : 2019/4/18 22:53
# @Author : apple
#@file : test_add.py

import unittest
from homework.api_http.common import do_excel,contants,http_request
from ddt import ddt,data
from homework.api_http.common.config import config
from homework.api_http.common import context
from homework.api_http.common.do_mysql import DoMysql
from homework.api_http.common import logger

logger = logger.get_logger(__name__)


@ddt
class AddTest(unittest.TestCase):
    excel = do_excel.DoExcel(contants.case_file, 'add')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        logger.info('准备测试前置！')
        cls.http_request = http_request.HttpRequest2()
        cls.mysql = DoMysql()

    @data(*cases)
    def test_add(self,case):
        logger.info('开始测试：{0}'.format(case.title))
        # 数据库校验，注册之前查询member表用户个数
        if case.sql is not None:
            sql = case.sql
            member = self.mysql.fetch_one(sql)
            before = member['count(*)']
            logger.debug("before:{0}".format(before))

        # #参数化方式二，结合配置文件进行参数化
        # case.data = eval(case.data)#转成字典
        # if  case.data.__contains__('mobilephone') and case.data['mobilephone']== 'normal_user':
        #     case.data['mobilephone']=config.get('data','normal_user')
        # if case.data.__contains__('pwd') and case.data['pwd']== 'normal_pwd':
        #     case.data['pwd']=config.get('data','normal_pwd')
        # if case.data.__contains__('memberId') and case.data['memberId']== 'loan_memberId':
        #     case.data['memberId']=config.get('data','loan_memberId')

        #参数化方式三：正则表达式替换
        case.data = eval(context.replace(case.data))

        resp = self.http_request.request(case.method,case.url,case.data)

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
            # 数据库校验
            # 成功之后，判断是否需要执行SQL
        if case.sql is not None:
            sql = case.sql
            member = self.mysql.fetch_one(sql)
            after = member['count(*)']
            logger.debug('after:{0}'.format(after))
            self.assertEqual(before + 1, after)
        logger.info('结束测试：{0}'.format(case.title))
    @classmethod
    def tearDownClass(cls):
        logger.info('测试后置处理！')
        cls.mysql.close()
        cls.http_request.close()
