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
    def __init__(self,arg_query,upperIncome="20",lowerIncome="8",fallIncome="5"):
        self.s = requests.session()
        self.config=json.load(file("./config/strategy.json"))
        self.s.headers.update(self.config["headers"])
        self.query=self.config[arg_query]
        self.stockHoldCount=self.config['transaction_params']['stockHoldCount']
        self.hold_days=arg_query.split("_")[1]
        self.upperIncome=str(upperIncome)
        self.lowerIncome=str(lowerIncome)
        self.fallIncome=str(fallIncome)
        print '\n{0:-^60}'.format('')
        print u"[策略]: %s days \t   [止损止盈]：%s|%s|%s \t [满仓]：%s 只" % (self.hold_days,self.upperIncome,self.lowerIncome,self.fallIncome,self.stockHoldCount)
        print '{0:-^60}\n'.format('')
        self.success= True

    #即时选股
    def pickstock(self):
        pickstock_params=self.config["pickstock_params"]
        pickstock_params.update({"w":self.query})
        r=self.s.get(self.config["PICKSTOCK_URL"],params=pickstock_params)
        #print r.json()["data"]["result"]["result"][0][1]
        return r.json()["data"]["result"]["result"]

    #回测选股
    def traceback(self):
        traceback_params=self.config["traceback_params"]
        traceback_params.update({"query":self.query,
                                "daysForSaleStrategy":self.hold_days,
                                "upperIncome":self.upperIncome,
                                "lowerIncome":self.lowerIncome,
                                "fallIncome":self.fallIncome})        
        while True:
            try:
                r=self.s.post(self.config["STRATEGY_URL"],data=traceback_params,timeout=5)
            except Exception as e:
                print e;time.sleep(2)
            else:       
                if r.json()['success']==False:
                    print r.json()['data']['crmMessage']
                    print u"抱歉，服务器繁忙，请稍后再试！"
                    continue
                #print r.json()['data']['stockData']['list']['data'][0]['codeName']               
                if r.json()['data']['stockData']['list']['stockNum']!=0:
                    return r.json()['data']['stockData']['list']
                else:
                    return False
    
    #策略回测   
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
                          
        r=self.s.post(self.config["TRANSACTION_URL"],data=transaction_params)

        if r.json()['success']!=False:
            return r.json()["data"]
        else:
            print r.json()['data']['crmMessage']  #请求超时
            return False
    
 
 
        
if __name__=="__main__":
    test=Strategy("QUERY_2_DAYS",25,5,10) # 2天策略： 25|5|10
   
    result=test.pickstock()
    print u"即时选股: %s" % (result[0][1] if len(result)!=0 else "[]")
    result= test.traceback()
    if result!=False:
        print result["stockDate"] + " 选出: "+ result["data"][0]["codeName"] + " < "+result["data"][0]["code"]+" >"
    else:
        print "[]"
    
    r=test.transaction(stime='2017-01-01',etime='2017-12-31')
    print '\n{0:-^60}'.format('Portfolie Value ')
    if r is not False:
        portfolio=1
        for i in xrange(len(r)-1,-1,-1):
            result=r[i]
            print "%s  %s %8s  %6s %6s %6s   %1.3f" % (result["stock_name"], \
                  result["bought_at"], result["sold_at"], \
                  result["buying_price"],result["selling_price"], \
                  result["signal_return_rate"], \
                  (1+float(result["signal_return_rate"])/100)*portfolio)                       
            portfolio *= 1+float(result["signal_return_rate"])/100





