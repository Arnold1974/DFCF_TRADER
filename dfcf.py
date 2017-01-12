#-*- coding:utf-8 -*-

import requests
import json


s = requests.session()
headers = {'Host': 'jy.xzsec.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding':'gzip, deflate, br',
           'Referer':'https://jy.xzsec.com/Trade/Buy',
           'Connection':'keep-alive',
           'Upgrade-Insecure-Requests':'1'         
           }       
s.headers.update(headers)           
res=s.post('https://jy.xzsec.com//Login/Authentication',json.load(file("./config/dfcf.json")));
r=s.get('https://jy.xzsec.com/Search/Position');
print r.url
print "---------------------"
#print r.text

s.headers.update({'Content-Type': 'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'})
Assets=s.post('https://jy.xzsec.com/Com/GetAssets',{'moneyType':'RMB'});

print "可用资金：%s" % str(Assets.json()["Data"][0]["Kyzj"])
print "可取资金：" + str(Assets.json()["Data"][0]["Kqzj"])
print "人民币总资产：" + str(Assets.json()["Data"][0]["RMBZzc"])
print "总资产：" + str(Assets.json()["Data"][0]["Zzc"])
print "冻结资金：" + str(Assets.json()["Data"][0]["Djzj"])
print "资金余额：" + str(Assets.json()["Data"][0]["Zjye"])
print "总市值：" + str(Assets.json()["Data"][0]["Zxsz"])

StockList=s.post('https://jy.xzsec.com/Search/GetStockList',{'qqhs':'1000','dwc':''});
if len(StockList.json()["Data"])==0:
    print "Stock Position:  0"
print 'Done!'

from log import TestRotating
TestRotating()

#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#r.encoding = 'GBK'
#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#print r.encoding

