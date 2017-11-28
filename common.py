#coding:utf-8
from config import *
import requests
import json
import warnings
import random
import sys
warnings.filterwarnings('ignore')
#发起请求
def requests_result(method= '',url = '',body = '',headers ='',verify = False):
    '''发起请求函数'''
    if method not in ('get','post'):
        print "目前只支持get以及post方法"
        return 0
    if method =='':
        print "url不能为空"
    elif method == 'get':
        RST = requests.get(url,verify=verify)
        return RST.text
    elif method == 'post':
        if body =='' and headers == '':
            RST = requests.post(url,verify = False)
        elif body != '' and headers == '':
            RST = requests.post(url,data = body,verify = False)
        elif body != '' and headers !='':
            RST = requests.post(url,data = body,headers = headers,verify = False)
        return RST.text

#登录
key_member_id = {}      
def login(user,password):
    '''登录函数'''
    url = "http://login.api.guxiansheng.cn/index.php?c=user&a=login"
    body = {"username":user,
            "password":password}
    method = 'post'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
            #"Accept": "application/json, text/javascript, */*; q=0.01",
            #"Host": "login.api.guxiansheng.cn"
            "Content-Type""application/json; charset=utf-8"
            "Content-Length": "62"
            "Connection""keep-alive"
            }
    retu_login = requests_result(method,url,body,headers)
#    return retu_login

    if json.loads(retu_login)['code'] ==1:
        key_member_id['member_id'] = json.loads(retu_login)['data']['member_id']
        key_member_id['key'] = json.loads(retu_login)['data']['key']
        print '账号登录成功'

    else:
        print '登录失败'.decode('utf-8')


#签到        
def qd(member_id,key):
    '''签到函数'''
    url = 'https://u.api.guxiansheng.cn/index.php?c=sign&a=post'
    body = {'member_id':key_member_id['member_id'],
            'key':key_member_id['key']}
    method = 'post'
    retu_qd = requests_result(method,url,body)
#    print retu_qd
    if json.loads(retu_qd) == 1:
        print '获取财币成功'.decode('utf-8')
    else:
        print '获取财币失败'.decode('utf-8')
        return 0

retu_hashkey = {}
def get_hashkey(member_id,key):
    '''获取hashkey'''
    url = 'https://trade.api.guxiansheng.cn/index.php?c=buy&a=get&v=2.1'
    body = {'object_id':85,
            'goods_type':1,
            'appId':'android',
            'member_id':key_member_id['member_id'],
            'key':key_member_id['key']}
    method = 'post'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
            "Content-Type""application/json; charset=utf-8"
            "Content-Length": "62"
            "Connection""keep-alive"
            }
    retu_get_hashkey = requests_result(method,url,body,headers)
    if json.loads(retu_get_hashkey)['code'] == 1:
        retu_hashkey['hashkey'] = json.loads(retu_get_hashkey)['data']['hashkey']
        print 'hashkey获取成功: '.decode('utf-8'),retu_hashkey['hashkey']
    else:
        print 'hashkey获取失败'.decode('utf-8')
        return 0
#    print retu_hashkey
def plan_a(member_id,key):
    '''订阅股机A'''
    url = 'https://trade.api.guxiansheng.cn/index.php?c=buy&a=nb_step2'

    body = {'channel':'tengxun',
            'goods_id':1,
            'hashkey':retu_hashkey['hashkey'],
            'appId':'android',
            'member_id':key_member_id['member_id'],
            'key':key_member_id['key']}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
            "Content-Type""application/json; charset=utf-8"
            "Content-Length": "62"
            "Connection""keep-alive"
            }    
    method = 'post'
    retu_plan_a = requests_result(method,url,body,headers)
    if json.loads(retu_plan_a)['code'] == 1:
        print '订阅股机A成功'.decode('utf-8')
        return retu_plan_a
    else:
        print '订阅股机A失败'.decode('utf-8')
        return 0

retu_seller_id = {}  #随机后的老师id
def get_seller_id(member_id,key):
    '''随机获取可提问的老师id'''
    url = 'https://clb.api.guxiansheng.cn/index.php?c=policy_new&a=policySellers'
    body = {'curpage':1,
            'pagesize':50
            }
    method = 'post'

    retu_get_list = requests_result(method,url,body)  #请求直播列表后返回结果
    i = random.randint(0,len(json.loads(retu_get_list)['data']['list'])-1) 
    retu_seller_id['seller_id'] = json.loads(retu_get_list)['data']['list'][i]['seller_id'] #随机取值seller_id
    print '被提问的老师id为：',retu_seller_id['seller_id']

retu_get_bk_name = []  #随机后的板块名称
def get_bk():
    '''随机获取板块名称'''
    url = 'https://mk2.api.guxiansheng.cn/?mod=quote&a=get&c=bk_sort&bkType=0&pageNo=1&pageSize=1000'
    method = 'get'
    retu_get_bk = requests_result(method,url)
    i = random.randint(0,len(json.loads(retu_get_bk)['data'])-1)
    retu_get_bk_name.append(json.loads(retu_get_bk)['data'][i]['NAME'])

def question(num):
    '''发起提问''' 
    question_content = '老师好，' + retu_get_bk_name[num].encode('utf-8') + random.choice(question_config)
    print retu_get_bk_name[num].encode('utf-8')
    #question_content = 'aaaaaaaaa' + str(question_config[0])
    url = 'https://clb.api.guxiansheng.cn/index.php?c=policy&a=questionsPost&v=1.1'
    body = {
      'seller_id':retu_seller_id['seller_id'] ,
      'questions':question_content,
      'answer_type':2,
      'question_way':2,
      'appId':'android',
      'member_id':key_member_id['member_id'],
      'key':key_member_id['key']
    }
    method = 'post'
#  print question_content
    retu_question = requests_result(method,url,body)
    if json.loads(retu_question)['code'] == 1:
        print '提问成功，提问内容为：',question_content
    else:
        print '提问失败'


