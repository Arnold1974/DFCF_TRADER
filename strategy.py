#-*- coding:utf-8 -*-

import requests


s = requests.session()
headers = {'Host': 'www.iwencai.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
           'Accept':'application/json, text/javascript, */*; q=0.01',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding':'gzip, deflate',
           'Referer':'http://www.iwencai.com/traceback/strategy',
           'Connection':'keep-alive',
           'Upgrade-Insecure-Requests':'1'         
           }       
s.headers.update(headers)     

#r=s.get('http://www.iwencai.com/traceback/strategy');


params_1={
        "query":"DDE大单净量大于0.25；涨跌幅大于10%；市盈率小于45；非st股；非创业板；总市值从小到大排列",
        "daysforSalestrategy":"2",
        "startDate":"2017-01-01", 
        "endDate":"2016-01-09",  
        "fell":"0.001", 
        "upperIncome":"20",  
        "lowerIncome":"10",        
        "fallIncome":"3",
        "stockHoldCount":"1",
       }
       
params_2={
        "stime":"2016-01-01",
        "etime":"2017-01-09",
        "hold_for":"2",
        "sort":"desc",
        "title":"bought_at",
        "stockHoldCount":"1",
        "fallIncome":"3",
        "lowerIncome":"10",
        "upperIncome":"20",
        "fell":"0.001",
        "endDate":"2016-01-09",
        "startDate":"2017-01-01",
        "daysforSalestrategy":"2",
        "query":"DDE大单净量大于0.25；涨跌幅大于10%；市盈率小于45；非st股；非创业板；总市值从小到大排列",
        "newType":"0"
       }
s.get('http://www.iwencai.com/log/my?info=ts|1、qs|backtest_myquery_start、w|query:DDE>3@holdDay:2@date:2015-06-15-2016-12-13@upperIncome:20@lowerIncome:10@fallIncome:3@stockHoldCount:1、tid|stockpick、DestinationURL|http://www.iwencai.com/traceback/strategy#DDE%3E3/2/2015-06-15/2016-12-13/0.001/20/10/3/1&logName=pick&qid=')       
#r=s.post('http://www.iwencai.com/traceback/strategy/submit',data=params_1,headers=headers)
s.headers.update({'Content-Type': 'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest', \
                  'charset':'UTF-8',
                   'Cookie':' PHPSESSID=p09r4qlvriir6une3g5unjtoi5; cid=p09r4qlvriir6une3g5unjtoi51484061014; ComputerID=p09r4qlvriir6une3g5unjtoi5170110+231014; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1484061068; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1484064205; Hm_lvt_57a0e026e5e0e1e90bcea3f298e48e74=1484061068; Hm_lpvt_57a0e026e5e0e1e90bcea3f298e48e74=1484064205'
                 })


r=s.post('http://www.iwencai.com/traceback/strategy/transaction',data=params_2,headers=headers);

print r.text
#print s.cookies
if r.json()["success"]==False:
    print "获取失败"
print r.json()["data"]

#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#r.encoding = 'GBK'
#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#print r.encoding
