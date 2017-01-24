#-*- coding:utf-8 -*-

import requests
import sys
import json


stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr  # 获取标准输入、标准输出和标准错误输出
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde  # 保持标准输入、标准输出和标准错误输出
sys.setdefaultencoding('utf8')


{
"PICKSTOCK_URL":"http://www.iwencai.com/stockpick/load-data",
"STRATEGY_URL":"http://www.iwencai.com/traceback/strategy/submit",
"TRANSACTION_URL":"http://www.iwencai.com/traceback/strategy/transaction",
"QUERY_4_DAYS":"非st; 收盘价在5元至30元之间; 总市值小于6000000000; 涨幅0%-6%; 15日区间涨跌幅<6%; 换手率<3.5%; 量比小于1.5; 市盈率(pe)<400;  boll突破中轨; dde大单净额流入; 一阳三线; a股市值(不含限售股)从小到大排列",
"QUERY_2_DAYS":"DDE大单净量大于0.25；涨跌幅大于10%；市盈率小于45；非st股；非创业板；上市日期>30；总市值从小到大排列",

"headers":{
                "Host": "www.iwencai.com",
                "Connection": "keep-alive",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36",
                "Referer": "http://www.iwencai.com",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8"
                },

"pickstock_params":{
                "typed":"0",
                "preParams":"",
                "ts":"1",
                "f":"1",
                "qs":"result_original",
                "selfsectsn":"",
                "querytype":"",
                "searchfilter":"",
                "tid":"stockpick",
                "w":"",
                "queryarea":"" 
                 },

"tracback_params":{
                "query":"",
                "daysForSaleStrategy":"4",
                "startDate":" ",
                "endDate":" ",
                "fell":"0.001",
                "upperIncome":"20",
                "lowerIncome":"8",
                "fallIncome":"5",
                "stockHoldCount":"1"
                 },
  
"transaction_params":{
                "stime":"2017-01-01",
                "etime":"2027-10-20",
                "hold_for":"4",
                "sort":"desc",
                "title":"bought_at",
                "stockHoldCount":"1",
                "fallIncome":"5",
                "lowerIncome":"8",
                "upperIncome":"20",
                "fell":"0.001",
                "endDate":" ",
                "startDate":" ",
                "daysForSaleStrategy":"4",
                "query":"",
                "newType":"0"
                 },

"income_control":{
                "upperIncome":"20",
                "lowerIncome":"8",
                "fallIncome":"5"
                }
                 
}


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
        print "策略持股天数: %s days \t 止损止盈：%s|%s|%s" % (self.hold_days,self.upperIncome,self.lowerIncome,self.fallIncome)
        
    def pickstock(self):
        pickstock_params=self.config["pickstock_params"]
        pickstock_params.update({"w":self.query})
        r=self.s.get(self.config["PICKSTOCK_URL"],params=pickstock_params)
        #print r.json()["data"]["result"]["result"][0][1]
        return r.json()["data"]["result"]["result"]


    def traceback(self):
        tracback_params=self.config["tracback_params"]
        tracback_params.update({"query":self.query,"daysForSaleStrategy":self.hold_days})
        tracback_params.update({"upperIncome":self.upperIncome,
                                "lowerIncome":self.lowerIncome,
                                "fallIncome":self.fallIncome}) 
        r=self.s.post(self.config["STRATEGY_URL"],data=tracback_params)
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
        transaction_params.update({"query":self.query})
        transaction_params.update({"upperIncome":self.upperIncome,
                                   "lowerIncome":self.lowerIncome,
                                    "fallIncome":self.fallIncome}) 
        r=self.s.post(self.config["TRANSACTION_URL"],data=transaction_params)
        if r.json()['success']!='false':
            return r.json()["data"]

        else:
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
            print "%s 买入后, 应该卖出的第四个交易日为: %s" % (buy_date, df.ix[index,'calendarDate'])   
        test()

if __name__=="__main__":
    #pickstock=Strategy()
    #pickstock.pickstock()
    
    test=Strategy("QUERY_4_DAYS")
    print "即时选股: %s \n" % test.pickstock()[0][1] if len(test.pickstock())!=0 else "[]"
    
    if test.traceback()!=False:
        print test.traceback()["stockDate"] + "选出: "+ test.traceback()["data"][0]["codeName"]
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






