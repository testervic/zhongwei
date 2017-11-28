#coding:utf-8
from common import *
import requests
import json
import warnings
import random
import sys
warnings.filterwarnings('ignore')

for i in range(0,len(username_password)):
    print '-' * 50
    login(username_password[i]["username"],username_password[i]["password"])    
    print '当前账号：',username_password[i]["username"]
    if key_member_id != {}:
      print 'member_id：',key_member_id['member_id'],'  ','key:',key_member_id['key']
    else:
      print '登录失败,停止运行'.decode('utf-8')
      break
    qd(key_member_id['member_id'],key_member_id['key'])
    get_hashkey(key_member_id['member_id'],key_member_id['key'])
    plan_a(key_member_id['member_id'],key_member_id['key'])
    get_seller_id(key_member_id['member_id'],key_member_id['key'])
    get_bk()
    #print retu_get_bk_name
    question(i)
 
