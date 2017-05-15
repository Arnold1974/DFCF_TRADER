#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests
import sys,time
import json


stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr  # 获取标准输入、标准输出和标准错误输出
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde  # 保持标准输入、标准输出和标准错误输出
sys.setdefaultencoding('utf8')


class Strategy(object):
    """
    利用同花顺回测引擎获取策略所需股票.

    返回数据为JSON类型.
    """
    def __init__(self,arg_query,upperIncome="20",fallIncome="5",lowerIncome="8"):
        self.s = requests.session()
        self.config=json.load(file("./config/strategy.json"))
        self.s.headers.update(self.config["headers"])
        self.query=self.config[arg_query]
        self.stockHoldCount=self.config['transaction_params']['stockHoldCount']
        self.hold_days=arg_query.split("_")[1]
        self.upperIncome=str(upperIncome)
        self.lowerIncome=str(lowerIncome)
        self.fallIncome=str(fallIncome)
        self.proxie=self.config["proxie"]
        print '\n{0:-^70}'.format('')
        print u"[策略]:  %s   [止盈回撤止损]: %s|%s|%s   [满仓]: %s 只" % (arg_query,self.upperIncome,self.fallIncome,self.lowerIncome,self.stockHoldCount)
        print '{0:-^70}\n'.format('')
        self.success= True

    #即时选股-----------------------------------------
    def pickstock(self):
        pickstock_params=self.config["pickstock_params"]
        pickstock_params.update({"w":self.query})

        while True:
            try:
                r=self.s.get(self.config["PICKSTOCK_URL"],params=pickstock_params,proxies=self.proxie)
            except Exception as e:
                print e;time.sleep(1)
            else:
                try:
                    return r.json()["data"]["result"]["result"]
                except ValueError as e: #ValueError: No JSON object could be decoded
                    print '<pickstock>',e;time.sleep(2)
    #回测选股--------------------------------------------
    def traceback(self):
        traceback_params=self.config["traceback_params"]
        traceback_params.update({"query":self.query,
                                "daysForSaleStrategy":self.hold_days,
                                "upperIncome":self.upperIncome,
                                "lowerIncome":self.lowerIncome,
                                "fallIncome":self.fallIncome,
                                "startDate":" ",
                                "endDate":" "})        
        while True:
            try:
                r=self.s.post(self.config["STRATEGY_URL"],data=traceback_params,timeout=10,proxies=self.proxie)
            except Exception as e:
                print e;time.sleep(2)
            else:       
                if r.json()['success']==False:
                    print "<traceback>: %s" % r.json()['data']['crmMessage']
                    #print u"抱歉，服务器繁忙，请稍后再试！"
                    time.sleep(1)
                    continue
                #print r.json()['data']['stockData']['list']['data'][0]['codeName']   
                #print  r.json()['data']['stockData'] #{u'errorCode': 100002, u'errorMsg': u'\u672a\u67e5\u8be2\u5230\u63a8\u8350\u80a1\u7968\u4ee3\u7801', u'list': []}
                try:
                    num=r.json()['data']['stockData']['list']['stockNum']
                except Exception as e: #TypeError as e:
                    print '<traceback>',e
                    time.sleep(1)
                    continue
                if num!=0:
                    return r.json()['data']['stockData']['list']
                else:
                    return False
    
    #策略回测----------------------------------------------
    def transaction(self,stime='2015-01-01',etime='2027-01-01'):
        '''
        return: (JSON)
        stock_code, bought_at,sold_at,buying_price,selling_price
        hold_for, signal_return_rate,stock_name               
        '''
        transaction_params=self.config["transaction_params"]
        transaction_params.update({"query":self.query,
                                   "hold_for":self.hold_days,
                                   "daysForSaleStrategy":self.hold_days})
        transaction_params.update({"upperIncome":self.upperIncome,
                                   "lowerIncome":self.lowerIncome,
                                   "fallIncome":self.fallIncome,
                                   "stime":stime,
                                   "startDate":stime,
                                   "etime":etime}) 
                          
        while True:
            try:
                r=self.s.post(self.config["TRANSACTION_URL"],data=transaction_params,proxies=self.proxie)
            except Exception as e:
                print '<transaction>',e;time.sleep(2)
            else:    
                try:
                    if r.json()['success']==False:
                        print r.json()['data']['crmMessage']
                        print u"抱歉，服务器繁忙，请稍后再试！"
                        time.sleep(1)
                        continue
                    else:
                        try:
                            return r.json()['data'] 
                        except TypeError as e:
                            print '<transaction>',e
                            time.sleep(1)
                            continue
                        else:
                            return False
                except ValueError as e: # NO JSON object could be decoded
                    print '<transaction>',e;time.sleep(2)
                        

        
if __name__=="__main__":
    
    test=Strategy("QUERY_2_DAYS_HARD",25,5,10) # 2天策略： 25|5|10
    test=Strategy("QUERY_4_DAYS",20,5,8) # 2天策略： 25|5|10
    from trade_calendar import TradeCalendar
    calendar=TradeCalendar()

#-----------------------
    result=test.pickstock()
    print u"即时选股:  @%s  %s [%s]" % ((time.strftime('%X',time.localtime()),result[0][1],result[0][0][:6])if len(result)!=0 else (" ","[]"," "))

    for i in xrange(len(result)):
        print result[i][1] 
#------------------------
    result= test.traceback()
    if result!=False:
        print u"策略选股: %s  %s [%s] ---> 购买日:%s\n" %((result["stockDate"], result["data"][0]["codeName"], \
             result["data"][0]["code"], calendar.trade_calendar(result["stockDate"].replace("-","/"),2)) if result!=False else (" ","[]"," "," "))
    else:
        print u"回测选股: []"
   
##--------------------------------
    stime='2017-01-01'
    etime='2018-01-01'
    r=test.transaction(stime=stime,etime=etime)
    print '{0:-^70}'.format('Portfolie Value ')
    if r is not False:
        portfolio=1
        for i in xrange(len(r)-1,-1,-1):
            show=r[i]
            if len(show["stock_name"])==3:
                show["stock_name"]=show["stock_name"]+'  '
            print "%s  %s  %8s  %6s %6s %6s   %d  %1.3f" % \
                 (show["stock_name"], 
                  show["bought_at"],
                  show["sold_at"], 
                  show["buying_price"],show["selling_price"], 
                  show["signal_return_rate"], 
                  time.strptime(show["bought_at"],'%Y-%m-%d').tm_wday+1,
                  (1+float(show["signal_return_rate"])/100)*portfolio)                       
            portfolio *= 1+float(show["signal_return_rate"])/100

        print '%s        --->  %s' % (show["stock_name"], calendar.trade_calendar(show["bought_at"].replace("-","/"),int(test.hold_days)))
    print '{0:-^70}\n'.format('End')

    #import os
    #os.system('pause')
    #import random
    #test.query = "DDE大单净量大于0.25；涨跌幅大于2%小于10.5%；市盈率小于45；非st股；非创业板；总市值从小到大排列"
    '''
    while True:
        result=test.pickstock()
        sys.stdout.write( "\r即时选股:  @%s  %s [%s]" % ((time.strftime('%X',time.localtime()),result[0][1],result[0][0][:6])if len(result)!=0 else (" ","[]"," ")))
        time.sleep(random.randint(20,100))
    '''