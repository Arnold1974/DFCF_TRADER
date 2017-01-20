#-*- coding:utf-8 -*-

import requests




    
STRATEGY_4_DAYS="http://www.iwencai.com/stockpick/load-data"



class Strategy(object):
    
    def __init__(self):
        self.s = requests.session()
        headers={
                "Host": "www.iwencai.com",
                "Connection": "keep-alive",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36",
                "Referer": "http://www.iwencai.com",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8"
                }
        self.s.headers.update(headers)
    def pickstock(self):
        params={
                "typed":"0",
                "preParams":"",
                "ts":"1",
                "f":"1",
                "qs":"result_original",
                "selfsectsn":"",
                "querytype":"",
                "searchfilter":"",
                "tid":"stockpick",
                "w":"非st; 收盘价在5元至30元之间; 总市值小于6000000000; 涨幅0%-6%; 15日区间涨跌幅<6%; 换手率<3.5%; 量比小于1.5; 市盈率(pe)<400;  boll突破中轨; dde大单净额流入; 一阳三线; a股市值(不含限售股)从小到大排列",
                "queryarea":"" 
               }
        r=self.s.get(STRATEGY_4_DAYS,params=params)
        #print r.json()["data"]["result"]["result"][0][1]
        print r.json()["data"]["result"]["result"][0][1]
if __name__=="__main__":
    pickstock=Strategy()
    pickstock.pickstock()


'''
STRATEGY_4_DAYS="http://www.iwencai.com/stockpick/load-data?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E8%82%A1%E7%A5%A8%E7%AE%80%E7%A7%B0%E9%9D%9Est%3B+%E6%94%B6%E7%9B%98%E4%BB%B7%E5%9C%A85%E5%85%83%E8%87%B330%E5%85%83%E4%B9%8B%E9%97%B4%3B+%E6%80%BB%E5%B8%82%E5%80%BC%E5%B0%8F%E4%BA%8E6000000000%3B+%E6%B6%A8%E5%B9%850%25-6%25%3B+15%E6%97%A5%E5%8C%BA%E9%97%B4%E6%B6%A8%E8%B7%8C%E5%B9%85%3C6%25%3B+%E6%8D%A2%E6%89%8B%E7%8E%87%3C3.5%25%3B+%E9%87%8F%E6%AF%94%E5%B0%8F%E4%BA%8E1.5%3B+%E5%B8%82%E7%9B%88%E7%8E%87(pe)%3C400%3B++boll%E7%AA%81%E7%A0%B4%E4%B8%AD%E8%BD%A8%3B+dde%E5%A4%A7%E5%8D%95%E5%87%80%E9%A2%9D%E6%B5%81%E5%85%A5%3B+%E4%B8%80%E9%98%B3%E4%B8%89%E7%BA%BF%3B+a%E8%82%A1%E5%B8%82%E5%80%BC(%E4%B8%8D%E5%90%AB%E9%99%90%E5%94%AE%E8%82%A1)%E4%BB%8E%E5%B0%8F%E5%88%B0%E5%A4%A7%E6%8E%92%E5%88%97&queryarea="
STRATEGY_URL='http://www.iwencai.com/traceback/strategy/submit'
TRANSACTION_URL='http://www.iwencai.com/traceback/strategy/transaction'
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'X-Requested-With':'XMLHttpRequest',
                  }
params_1={
        "query":"DDE大单净量大于0.25；涨跌幅大于10%；市盈率小于45；非st股；非创业板；总市值从小到大排列",
        "daysforSalestrategy":"2",
        "startDate":"2017-01-01", 
        "endDate":"2016-01-09",  
        "fell":"0.001", 
        "upperIncome":"20",  
        "lowerIncome":"10",        
        "fallIncome":"3",
        "stockHoldCount":"1"
       }
       
s = requests.session()
s.get('http://www.iwencai.com/traceback/strategy')
s.headers.update(headers)
print s.headers
#r=s.post(TRANSACTION_URL,data=params_1);
r=s.get(STRATEGY_URL)

print r.json()
'''
'''
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
print s.cookies     
#r=s.post('http://www.iwencai.com/traceback/strategy/submit',data=params_1,headers=headers)
s.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'X-Requested-With':'XMLHttpRequest',
                  })


mycookie={'cid':'p09r4qlvriir6une3g5unjtoi51484061014','ComputerID':'p09r4qlvriir6une3g5unjtoi5170110+231014','Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1':'1484061068,1484105103','Hm_lvt_57a0e026e5e0e1e90bcea3f298e48e74':'1484061068,1484105103','PHPSESSID':'i006a7vf37vdjgh0cr8lngkg47','Hm_lpvt_57a0e026e5e0e1e90bcea3f298e48e74':'1484105250', 'Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1':'1484105249','guideState':'1'}
print s.cookies
r=s.post('http://www.iwencai.com/traceback/strategy/transaction',data=json.dumps(params_2),headers=headers);
print s.cookies

print r.text
#print s.cookies
if r.json()["success"]==False:
    print "获取失败"
print r.json()["data"]

'''