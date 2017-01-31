#-*- coding:utf-8 -*-

import requests
import sys
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
    def __init__(self,arg_query,upperIncome="20",lowerIncome="8",fallIncome="5"):
        self.s = requests.session()
        self.config=json.load(file("./config/strategy.json"))
        self.s.headers.update(self.config["headers"])
        self.query=self.config[arg_query]
        self.hold_days=arg_query.split("_")[1]
        self.upperIncome=str(upperIncome)
        self.lowerIncome=str(lowerIncome)
        self.fallIncome=str(fallIncome)
        print u"策略持股天数: %s days \t 止损止盈：%s|%s|%s" % (self.hold_days,self.upperIncome,self.lowerIncome,self.fallIncome)
        
    def pickstock(self):
        pickstock_params=self.config["pickstock_params"]
        pickstock_params.update({"w":self.query})
        r=self.s.get(self.config["PICKSTOCK_URL"],params=pickstock_params)
        #print r.json()["data"]["result"]["result"][0][1]
        return r.json()["data"]["result"]["result"]


    def traceback(self):
        traceback_params=self.config["traceback_params"]
        traceback_params.update({"query":self.query,
                                "daysForSaleStrategy":self.hold_days})
        traceback_params.update({"upperIncome":self.upperIncome,
                                "lowerIncome":self.lowerIncome,
                                "fallIncome":self.fallIncome}) 
        
        r=self.s.post(self.config["STRATEGY_URL"],data=traceback_params)

        if r.json()['success']==False:
            print r.json()['data']['crmMessage']
            print u"抱歉，服务器繁忙，请稍后再试！"
            return False
        #print r.json()['data']['stockData']['list']['data'][0]['codeName']
        
        if r.json()['data']['stockData']['list']['stockNum']!=0:
            return r.json()['data']['stockData']['list']
        else:
            return False
       
    def transaction(self):
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
                                    "fallIncome":self.fallIncome}) 
                          
        r=self.s.post(self.config["TRANSACTION_URL"],data=transaction_params)

        if r.json()['success']!=False:
            return r.json()["data"]
        else:
            print r.json()['data']['crmMessage']  #请求超时
            return False
    
    def trade_calendar(self):
        '''
                交易日历
        isOpen=1是交易日，isOpen=0为休市
        '''
        import pandas as pd
        df= pd.read_csv(self.config["TRADE_CALENDAR_URL"])
        buy_date='2017/01/18'
        print df.ix[list(df['calendarDate']).index(buy_date),'isOpen']        
        
        #return pd.read_csv("http://218.244.146.57/static/calAll.csv")
        def test():
            index=df[df['calendarDate']==buy_date].index[0]
            i=0
            while i<3:
                index+=1
                if df.ix[index,'isOpen'] == 1:
                    i+=1
            print u"%s 买入后, 应该卖出的第四个交易日为: %s" % (buy_date, df.ix[index,'calendarDate'])   
        test()
 
        
if __name__=="__main__":
    test=Strategy("QUERY_4_DAYS")
   
    result=test.pickstock()
    print u"即时选股: %s \n" % (result[0][1] if len(result)!=0 else "[]")
    
    result= test.traceback()
    if result!=False:
        print result["stockDate"] + "选出: "+ result["data"][0]["codeName"]
    else:
        print "[]"
    
    r=test.transaction()
    if r is not False:
        for i in xrange(len(r)):        
            result=r[i]
            print "%s %s %8s %s %s %s" % (result["stock_name"], \
                  result["bought_at"], result["sold_at"], \
                  result["buying_price"],result["selling_price"], \
                  result["signal_return_rate"]) 

    a1=TradeCalendar()
    a1.trade_calendar("2017/01/26",2)




