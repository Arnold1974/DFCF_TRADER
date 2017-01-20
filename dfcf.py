# -*- coding:utf-8 -*-

import requests
import json,re
import threading,time
from winsound import Beep

class DFCF_Trader(object):
    def __init__(self):
        self.s = requests.session()
        
        self.login_flag=False        
        thread_1 = threading.Thread(target=self.login,name='Thread-login')
        thread_1.setDaemon(True)
        thread_1.start()

#登陆
    def login(self):
        print '[%s] : %s start' % (time.strftime('%H:%M:%S'),threading.current_thread().name)
        while True:
            if not self.login_flag:
                print  '[%s] : %s' % (time.strftime('%H:%M:%S') ,'Logging...')
                try:
                    self.__authorization()
                    print  '[%s] : %s' % (time.strftime('%H:%M:%S') ,'Login Success!')
                except Exception:
                    Beep(300,150)
                    print "\n login connection lost!"
            time.sleep(1)
    def __authorization(self):
        headers = {'Host': 'jy.xzsec.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding':'gzip, deflate, br',
                   'Referer':'https://jy.xzsec.com/Trade/Buy',
                   'Connection':'keep-alive',
                   'Upgrade-Insecure-Requests':'1'         
                   } 
        self.s.headers.update(headers) 
        res=self.s.post('https://jy.xzsec.com//Login/Authentication',json.load(file("./config/dfcf.json")))
        
        self.login_flag=True if res.json()["Status"]==0 else False         
        self.login_message=res.json()
        '''
        self.login_message= "message(%s), Status(%s)" % (res.json()["Message"], res.json()["Status"])
        for i in xrange(len(res.json()["Data"])):
            for key  in res.json()["Data"][i]:
                    self.login_message += key +" %s" % res.json()["Data"][i][key]
        '''        
        return self.login_message
        
#资产列表
    def getassets(self):
        try:
            Assets=self.s.post('https://jy.xzsec.com/Com/GetAssets',{'moneyType':'RMB'},timeout=3);
        except Exception:
            print "\n getassets connection lost!"
            self.login_flag=False
            return False
        if Assets.json()["Status"]!=0:
            self.login_flag=False
            return False
        return Assets.json()["Data"][0]
        

#持仓列表
    def getstocklist(self):    
        self.stocklist_message=""
        StockList=self.s.post('https://jy.xzsec.com/Search/GetStockList',{'qqhs':'1000','dwc':''});
        if len(StockList.json()["Data"])==0:
            print "Stock Position:  0"
        else:
            for i in xrange(len(StockList.json()["Data"])):
                for key  in StockList.json()["Data"][i]:
                    self.stocklist_message += key +":%s  " % StockList.json()["Data"][i][key]

#当日委托
    def getordersdata(self):
        self.ordersdata_message=""
        OrdersData=self.s.post('https://jy.xzsec.com/Search/GetOrdersData',{'qqhs':'20','dwc':''});
        if len(OrdersData.json()["Data"])==0:
            print "Orders:  0"
        else:
            for i in xrange(len(OrdersData.json()["Data"])):
                for key  in OrdersData.json()["Data"][i]:
                    self.ordersdata_message += key +":%s \n" % OrdersData.json()["Data"][i][key]

#当日成交
    def getdealdata(self):
        self.dealdata_message=""
        DealData=self.s.post('https://jy.xzsec.com/Search/GetDealData',{'qqhs':'20','dwc':''});
        if len(DealData.json()["Data"])==0:
            print "Deals:  0"
        else:
            for i in xrange(len(DealData.json()["Data"])):
                for key  in DealData.json()["Data"][i]:
                    self.dealdata_message += key +":%s \n" % DealData.json()["Data"][i][key]
       
       
#撤单列表
    def getrevokelist(self):
        try:
            RevokeList=self.s.post('https://jy.xzsec.com/Trade/GetRevokeList',timeout=3)
        except Exception:
            self.login_flag=False
        list=[]
        if len(RevokeList.json()["Data"])==0:
            print "Revoke List: %2d" % (0)
        else:           
            for i in xrange(len(RevokeList.json()["Data"])):
                list.append(RevokeList.json()["Data"][i]["Wtrq"]+"_"+ \
                            RevokeList.json()["Data"][i]["Wtbh"])                    
        return list

#撤单
    def revoke(self,wtbh):    
        RevokeOrders=self.s.post('https://jy.xzsec.com/Trade/RevokeOrders',{'revokes':wtbh})
        return RevokeOrders

#下单
    def deal(self,stockcode,stockname,price,tradetype):
        GetKyzjAndKml=self.s.post('https://jy.xzsec.com/Trade/GetKyzjAndKml', \
                             {'stockCode':stockcode,'stockName':stockname,'price':price,'tradeType':tradetype});
        Kmml=GetKyzjAndKml.json()["Data"]["Kmml"]
        print Kmml, type(Kmml)
        
        SubmitTrade=self.s.post('https://jy.xzsec.com/Trade/SubmitTrade', \
                           {'stockCode':stockcode,'price':price, \
                           'amount':GetKyzjAndKml.json()["Data"]["Kmml"], \
                           'tradeType':tradetype} #,'stockName':stockname
                           )       
        print "委托编号: [%s]" %  SubmitTrade.json()["Data"][0]["Wtbh"],

#获取实时行情
    def getquote(self,stockcode):
        params={
                'id':stockcode,
                'callback':'',#'jQuery18302588442438663068_1484803703313',
                '_':'' # repr(time.time()).replace(".","")
               }
        quote=self.s.get('https://hsmarket.eastmoney.com/api/SHSZQuoteSnapshot',params = params)
        return eval(re.search(r'{.*}',quote.text).group())
        
if __name__=="__main__":
    import sys
    import pandas as pd    

    stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr  # 获取标准输入、标准输出和标准错误输出
    reload(sys)
    sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde  # 保持标准输入、标准输出和标准错误输出
    sys.setdefaultencoding('utf8')

    print "Active Threading: %d" % threading.active_count()
    
    user=DFCF_Trader()

    if user.login_flag==True:
        print "begin buy"
        user.deal("000619","海螺型材","13.4","B")
    while True:
        if user.login_flag==True:
            assets=user.getassets()
            if assets:
                assets.update(user.login_message['Data'][0])
                sys.stdout.write( "\r%(khmc)s <%(Syspm1)s>\tLogged at: %(Date)s-%(Time)s \
                                    **************************************************** \
                                   总资产:%(Zzc)s\t可用资金:%(Kyzj)s\t可取资金:%(Kqzj)s\t \
                                   冻结资金:%(Djzj)s\t资金余额: %(Zjye)s \t总市值: %(Zxsz)s " % assets)
              
            df=pd.DataFrame(user.login_message['Data'])            
            df=df.ix[:,[0,5,1,6]]
            df.columns = ['Date', 'Time','Account','Name']       
            #print user.login_message['Data']
            #print "qiwsir is in %(khmc)r"%user.login_message['Data']
            #sys.stdout.write( "\r %(khmc)s <%(Syspm1)s> Logged at: %(Date)s-%(Time)s "  \
            #                  % user.login_message['Data'][0])
        time.sleep(1)

    
'''     import time,sys
    for i in xrange(10):
        user.getstocklist()
        
        sys.stdout.write("\r [%r] %200s" % (time.ctime(), user.stocklist_message))
        #sys.stdout.write( "\rFile transfer progress :[%3d] percent complete!" % i )
        #sys.stdout.write ("\rProcessing: [%2d%%]" % i)      
        sys.stdout.flush()
        time.sleep(.1)


    user.getrevokelist()
    print user.revokelist_message
    print "-----------"    
    user.getordersdata()
    print user.ordersdata_message
    print "***********"
    user.getdealdata()
    print user.dealdata_message

    user.deal('600692','亚通股份','18.6','S')
    #user.revoke('20170116_132537')
'''           
#----华丽的分割线 ：)  ---------------
'''        
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
print "--------------------- \n"

StockList=s.post('https://jy.xzsec.com/Search/GetStockList',{'qqhs':'1000','dwc':''});
if len(StockList.json()["Data"])==0:
    print "Stock Position:  0"
else:
    for _ in xrange(len(StockList.json()["Data"])):
        print "证券代码：%s" % str(StockList.json()["Data"][0]["Zqdm"])


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


from log import TestRotating
TestRotating()

#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#r.encoding = 'GBK'
#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#print r.encoding
'''
