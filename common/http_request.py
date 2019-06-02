#coding:utf-8
#@time : 2019/4/14 21:42
# @Author : apple
#@file : http_request.py

import requests
from homework.api_http.common.config import config
from homework.api_http.common import logger

logger = logger.get_logger(__name__)
class HttpRequest:
    """
    独立session，cookies需要自己传递
    使用这类的request方法去完成不同的HTTP请求，并且返回响应结果
    """

    def request(self, method, url, data=None, json=None, cookies=None):

        method = method.upper()  # 将method强制转成全大写

        if type(data) == str:
            data = eval(data)  # str转成字典
        # url拼接

        url = config.get("api","pre_url")+url
        print('url:',url)
        print('data:', data)
        if method == 'GET':
            resp = requests.get(url=url, params=data, cookies=cookies)  # resp 是Response对象
        elif method == 'POST':
            if json:
                resp = requests.post(url=url, json=json, cookies=cookies)
            else:
                resp = requests.post(url=url, data=data, cookies=cookies)
        else:
            resp = None
            print('UN-support method')

        return resp


class HttpRequest2:
    """
        公共使用一个session, cookies自动传递
       使用这类的request方法去完成不同的HTTP请求，并且返回响应结果
    """

    def __init__(self):
        # 打开一个session
        self.session = requests.sessions.session()

    def request(self, method, url, data=None, json=None):
        # url拼接
        url = config.get("api","pre_url")+url
        logger.debug('请求url：{0}'.format(url))
        logger.debug('请求data：{0}'.format(data))
        method = method.upper()  # 将method强制转成全大写
        if method == 'GET':
            resp = self.session.request(method=method, url=url, params=data)
        elif method == 'POST':
            if json:
                resp = self.session.request(method=method, url=url, json=json)
            else:
                resp = self.session.request(method=method, url=url, data=data)
        else:
            resp = None
            logger.error('UN-support method')
        logger.debug('请求response：{0}'.format(resp.text))
        return resp

    def close(self):
        self.session.close()  # 用完记得关闭


if __name__ == '__main__':
    http_request = HttpRequest2()
    # 注册
    resp = http_request.request('get','/member/register',
                                data={'mobilephone': '18041365973',
                                      'pwd': '123456789012345678','regname':'18位密码'}
)
    print(resp.text)

    #登录
    resp = http_request.request('get','/member/login',
                                data={'mobilephone': '18756340012',
                                      'pwd': '123456'})
    print(resp.text)
    # #充值
    # resp= http_request.request('post','/member/recharge',data={'mobilephone': '18041365972',
    #                                   'amount': '1000'})
    # print(resp.text)
    # #新建项目
    # resp = http_request.request('post',
    #                              '/loan/add',
    #                              data={'memberId':412,'title':'apple测试','amount':5000,
    #                                    'loanRate':10.0,'loanTerm':30,'loanDateType':2,
    #                                    'repaymemtWay':4,'biddingDays':10})
    # print(resp.text)
    #创建满标的情况
    # resp = http_request.request('post','/loan/add',data={'memberId':635,'title':'apple测试满标','amount':2000,
    #                                     'loanRate':10.0,'loanTerm':30,'loanDateType':2,
    #                                     'repaymemtWay':4,'biddingDays':10})
    # print(resp.text)
    # # 审核项目
    # resp = http_request.request('post','/loan/audit',data ={'id':520,'status':4})
    # print(resp.text)
    # #
    # #投标
    # resp = http_request.request('post', '/member/bidLoan', data={'memberId':577,'password':'123456',
    #                                                              'loanId':520,'amount':1000})
    print(resp.text)
