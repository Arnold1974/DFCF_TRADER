#-*- coding:utf-8 -*-

import requests
import sys

stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr  # 获取标准输入、标准输出和标准错误输出
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde  # 保持标准输入、标准输出和标准错误输出
sys.setdefaultencoding('utf8')



STRATEGY_4_DAYS="http://www.iwencai.com/stockpick/load-data"
STRATEGY_URL='http://www.iwencai.com/traceback/strategy/submit'
TRANSACTION_URL='http://www.iwencai.com/traceback/strategy/transaction'
QUERY="非st; 收盘价在5元至30元之间; 总市值小于6000000000; 涨幅0%-6%; 15日区间涨跌幅<6%; 换手率<3.5%; 量比小于1.5; 市盈率(pe)<400;  boll突破中轨; dde大单净额流入; 一阳三线; a股市值(不含限售股)从小到大排列"

class Strategy(object):
    """
    利用同花顺回测引擎获取策略所需股票.

    返回数据为JSON类型.
    """
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
                "w":QUERY,
                "queryarea":"" 
               }
        r=self.s.get(STRATEGY_4_DAYS,params=params)
        #print r.json()["data"]["result"]["result"][0][1]
        return r.json()["data"]["result"]["result"]


    def traceback(self):
        url="http://www.iwencai.com/traceback/strategy/submit"
        params={
                "query":QUERY,
                "daysForSaleStrategy":"4",
                "startDate":"2017-01-01",
                "endDate":"2017-01-20",
                "fell":"0.001",
                "upperIncome":"20",
                "lowerIncome":"8",
                "fallIncome":"5",
                "stockHoldCount":"1"               
               }
        r=self.s.post(url,data=params)
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
        params_2={
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
                "query":QUERY,
                "newType":"0"
                 }
        r=self.s.post(TRANSACTION_URL,data=params_2)
        if r.json()['success']!='false':
            return r.json()["data"]

        else:
           return False
    
    def trade_cal(self):
        '''
                交易日历
        isOpen=1是交易日，isOpen=0为休市
        '''
        import pandas as pd
        df= pd.read_csv("http://218.244.146.57/static/calAll.csv")
        buy_date='2017/01/26'
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
    
    test=Strategy()
    print test.pickstock()[0][1]
    #print test.traceback()
    r=test.transaction()
    if r is not False:
        for i in xrange(len(r)):        
            result=r[i]
            print "%s %s %8s %s %s %s" % (result["stock_name"], \
                  result["bought_at"], result["sold_at"], \
                  result["buying_price"],result["selling_price"], \
                  result["signal_return_rate"]) 






