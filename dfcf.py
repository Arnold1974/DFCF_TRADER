# -*- coding:utf-8 -*-

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
print "可用资金：" + str(Assets.json()["Data"][0]["Kyzj"])
print "可取资金：" + str(Assets.json()["Data"][0]["Kqzj"])
print "人民币总资产：" + str(Assets.json()["Data"][0]["RMBZzc"])
print "总资产：" + str(Assets.json()["Data"][0]["Zzc"])
print "冻结资金：" + str(Assets.json()["Data"][0]["Djzj"])
print "资金余额：" + str(Assets.json()["Data"][0]["Zjye"])
print "总市值：" + str(Assets.json()["Data"][0]["Zxsz"])

StockList=s.post('https://jy.xzsec.com/Search/GetStockList',{'qqhs':'1000','dwc':''});
if len(StockList.json()["Data"])==0:
    print "Stock Position:  0"

GetOrdersData=s.post('https://jy.xzsec.com/Search/GetOrdersData',{'qqhs':'20','dwc':''});
if len(GetOrdersData.json()["Data"])==0:
    print "Orders:  0"
else:
    print len(GetOrdersData.json()["Data"])
    print GetOrdersData.json()["Data"][0]["Wtsj"]
    
  
GetKyzjAndKml=s.post('https://jy.xzsec.com/Trade/GetKyzjAndKml', {'stockCode':'601666','price':'5.01','tradeType':'B','stockName':'平煤股份'});
print GetKyzjAndKml.json()["Data"]["Kmml"]
Kmml=GetKyzjAndKml.json()["Data"]["Kmml"]
print Kmml, type(Kmml)

SubmitTrade=s.post('https://jy.xzsec.com/Trade/SubmitTrade', \
                   {'stockCode':'601666','price':'5.01','amount':'100','tradeType':'B','stockName':'平煤股份'}
                   )
                  

GetRevokeList=s.post('https://jy.xzsec.com/Trade/GetRevokeList')
if len(GetRevokeList.json()["Data"])==0:
    print "Orders:  0"
else:
    print len(GetRevokeList.json()["Data"])
    print GetRevokeList.json()["Data"][0]["Zqdm"]
    print GetRevokeList.json()["Data"][0]["Zqmc"]
    print GetRevokeList.json()["Data"][0]["Mmsm"]
    print GetRevokeList.json()["Data"][0]["Wtzt"]
    print GetRevokeList.json()["Data"][0]["Wtjq"]
    print GetRevokeList.json()["Data"][0]["Wtsl"]
    print GetRevokeList.json()["Data"][0]["Cjjq"]
    print GetRevokeList.json()["Data"][0]["Cjsl"]
    print GetRevokeList.json()["Data"][0]["Wtbh"] #委托编号
    print GetRevokeList.json()["Data"][0]["Cdsl"] #撤单价格
    print GetRevokeList.json()["Data"][0]["Gddm"] #股东代码
    print GetRevokeList.json()["Data"][0]["Market"]
    print GetRevokeList.json()["Data"][0]["Wtsj"] #委托时间
    print GetRevokeList.json()["Data"][0]["Dwc"] 
    print GetRevokeList.json()["Data"][0]["Cjje"]
    print GetRevokeList.json()["Data"][0]["Wtrq"]
    print GetRevokeList.json()["Data"][0]["Khdm"] #客户代码
    print GetRevokeList.json()["Data"][0]["Khxm"]
    print GetRevokeList.json()["Data"][0]["Zjzh"]
    print GetRevokeList.json()["Data"][0]["Hb"]
    print GetRevokeList.json()["Data"][0]["Jgbm"]
    print GetRevokeList.json()["Data"][0]["Htxh"]
    print GetRevokeList.json()["Data"][0]["Bpsj"] 
    print GetRevokeList.json()["Data"][0]["Cpbm"] 
    print GetRevokeList.json()["Data"][0]["Cpmc"]
    print GetRevokeList.json()["Data"][0]["Djje"]
    print GetRevokeList.json()["Data"][0]["Jyxw"] 
    print GetRevokeList.json()["Data"][0]["Cdbs"] 
    print GetRevokeList.json()["Data"][0]["Czrq"] #操作日期
    print GetRevokeList.json()["Data"][0]["Yjlx"]
    print GetRevokeList.json()["Data"][0]["Wtqd"]
    print GetRevokeList.json()["Data"][0]["Bzxx"]
    print GetRevokeList.json()["Data"][0]["Mmbz"] 

RevokeOrders=s.post('https://jy.xzsec.com/Trade/RevokeOrders',{'revokes':'20170110_209948'})
print RevokeOrders.json()["20170110"]


#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#r.encoding = 'GBK'
#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#print r.encoding

