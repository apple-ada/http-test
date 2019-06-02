#coding:utf-8
#@time : 2019/5/7 1:02
# @Author : apple
#@file : run.py
import sys
sys.path.append('./')
import unittest
import HTMLTestRunnerNew

from homework.api_http.common import contants



discover = unittest.defaultTestLoader.discover(contants.case_dir, "test_*.py")

with open(contants.report_dir + '/report.html', 'wb+') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              title="HTTP API TEST REPORT",
                                              description="前程贷API",
                                              tester="apple")
    runner.run(discover)
