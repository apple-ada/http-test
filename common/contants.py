#coding:utf-8
#@time : 2019/4/14 21:36
# @Author : apple
#@file : contants.py

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # date_0413
print(base_dir)

case_file = os.path.join(base_dir, 'data', 'cases.xlsx')#用例数据文件
print(case_file)

global_file = os.path.join(base_dir, 'config', 'global.conf')
print(global_file)

online_file = os.path.join(base_dir, 'config', 'online.conf')
print(online_file)

test_file = os.path.join(base_dir, 'config', 'test.conf')
print(test_file)

log_dir = os.path.join(base_dir, 'logs')
print(log_dir)

case_dir = os.path.join(base_dir, 'testcases')

report_dir = os.path.join(base_dir, 'reports')
